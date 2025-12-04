from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Demetrio Atra', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'demetrio.atra@example.com | 555-0199 | https://github.com/demetrioatra', 0, 1, 'C')
        self.ln(10)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def section_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln(5)

pdf = PDF()
pdf.add_page()

# Summary
pdf.section_title('SUMMARY')
pdf.section_body(
    "Senior Software Engineer with over 8 years of experience specializing in Python, Artificial Intelligence, and Machine Learning. "
    "Passionate about building scalable AI-driven solutions and open source contributions. "
    "Proven track record in developing distributed systems and optimizing data pipelines."
)

# Skills
pdf.section_title('SKILLS')
pdf.section_body(
    "Languages: Python, JavaScript, SQL, Go\n"
    "AI/ML: TensorFlow, PyTorch, Scikit-learn, NLP, Computer Vision\n"
    "Tools: Docker, Kubernetes, AWS, Git, Apache Spark, Kafka"
)

# Experience
pdf.section_title('EXPERIENCE')

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, 'Senior AI Engineer | Tech Innovations Labs', 0, 1)
pdf.set_font('Arial', 'I', 10)
pdf.cell(0, 5, 'Jan 2021 - Present', 0, 1)
pdf.set_font('Arial', '', 10)
pdf.multi_cell(0, 5, 
    "- Architected and deployed a real-time recommendation engine using Python and TensorFlow, serving 1M+ users.\n"
    "- Led the migration of legacy monoliths to microservices using Docker and Kubernetes.\n"
    "- Mentored junior developers and established best practices for code quality and CI/CD pipelines.\n"
    "- Actively contributed to internal AI tools and libraries."
)
pdf.ln(3)

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, 'Software Engineer | DataCorp Solutions', 0, 1)
pdf.set_font('Arial', 'I', 10)
pdf.cell(0, 5, 'Jun 2017 - Dec 2020', 0, 1)
pdf.set_font('Arial', '', 10)
pdf.multi_cell(0, 5, 
    "- Developed data processing pipelines using Apache Spark and Python, reducing processing time by 60%.\n"
    "- Implemented machine learning models for customer churn prediction using Scikit-learn.\n"
    "- Collaborated with product teams to define requirements and deliver features on time."
)
pdf.ln(3)

# Education
pdf.section_title('EDUCATION')
pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 5, 'Master of Science in Computer Science', 0, 1)
pdf.set_font('Arial', '', 10)
pdf.cell(0, 5, 'University of Tech, 2017', 0, 1)

pdf.output('sample_resume.pdf', 'F')
print("✅ sample_resume.pdf generated successfully.")
