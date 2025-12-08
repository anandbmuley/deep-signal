import requests
import sys
import os
import time
import subprocess
import signal

def run_server():
    """Starts the uvicorn server in a subprocess."""
    # We use the python executable that is running this script
    cmd = [sys.executable, "-m", "uvicorn", "deep_signal.api.main:app", "--port", "8000"]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.getcwd(), "src")
    env["DEEP_SIGNAL_API_KEY"] = "test_secret_key"
    
    print(f"Starting server with command: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def test_upload():
    """Tests the upload endpoint."""
    url = "http://localhost:8000/resumes/file"
    headers = {"X-API-Key": "test_secret_key"}
    
    # Use the sample resume from local directory
    sample_pdf_path = os.path.join(os.getcwd(), "local", "sample_resume.pdf")
    
    if os.path.exists(sample_pdf_path):
        print(f"Using sample PDF from: {sample_pdf_path}")
        with open(sample_pdf_path, "rb") as f:
            pdf_content = f.read()
    else:
        print("Sample PDF not found, creating a minimal one...")
        # Minimal PDF creation fallback
        pdf_content = (
            b"%PDF-1.4\n"
            b"1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
            b"2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n"
            b"3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Resources <<\n/Font <<\n/F1 <<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\n>>\n>>\n/Contents 4 0 R\n>>\nendobj\n"
            b"4 0 obj\n<<\n/Length 55\n>>\nstream\nBT\n/F1 12 Tf\n72 712 Td\n(Hello World from PDF!) Tj\nET\nendstream\nendobj\n"
            b"xref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000117 00000 n \n0000000288 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n393\n%%EOF\n"
        )
    
    files = {
        'file': ('test.pdf', pdf_content, 'application/pdf')
    }
    
    # Wait for server to start
    max_retries = 10
    for i in range(max_retries):
        try:
            requests.get("http://localhost:8000/")
            print("Server is up!")
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                print("Server failed to start.")
                return False
            time.sleep(1)
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, headers=headers, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200 and len(response.json().get("text_preview", "")) > 10:
            print("✅ TEST PASSED")
            return True
        else:
            print("❌ TEST FAILED: Content mismatch or bad status")
            return False
            
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    # Ensure necessary packages are available (mock check)
    try:
        import fastapi
        import uvicorn
        import pdfplumber
        import python_multipart
    except ImportError as e:
        print(f"Missing dependency: {e}")
        # In a real environment we would install them, but here we might rely on the user to install.
        # However, for verification to work, we need them.
        sys.exit(1)

    server_process = run_server()
    try:
        success = test_upload()
    finally:
        server_process.terminate()
        server_process.wait()
        
    if not success:
        sys.exit(1)
