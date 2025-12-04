
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

text = """
John Doe
john.doe@example.com
123-456-7890

SUMMARY
Highly skilled Senior Software Engineer with 7 years of experience in Python, AI, and Machine Learning.
Proven track record of delivering scalable solutions and leading engineering teams.

EXPERIENCE
Senior Software Engineer | Tech Solutions Inc. | Jan 2020 - Present
- Led a team of 5 engineers to build a distributed recommendation system.
- Optimized data pipelines using Apache Spark and Kafka, reducing latency by 40%.
- Implemented LLM-based features using OpenAI and LangChain.

Software Engineer | Data Corp | Jun 2016 - Dec 2019
- Developed RESTful APIs using FastAPI and Django.
- Built machine learning models for customer churn prediction using Scikit-learn.
- Collaborated with product managers to define feature requirements.

EDUCATION
Master of Science in Computer Science | Stanford University | 2016
Bachelor of Science in Computer Science | UC Berkeley | 2014

SKILLS
Languages: Python, Java, SQL, JavaScript
Frameworks: FastAPI, Django, React, TensorFlow, PyTorch
Tools: Docker, Kubernetes, AWS, Git
"""

pdf.multi_cell(0, 10, text)
pdf.output("sample_resume.pdf")
print("✅ Created sample_resume.pdf")
