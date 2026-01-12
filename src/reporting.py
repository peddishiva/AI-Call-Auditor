import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, output_dir="customer_auditor/data/reports"):
        self.output_dir = output_dir
        self.sender_email = "hamsajoshua55@gmail.com"
        self.sender_pass = "myjn fwkq lyjo gopn"

    def generate_pdf(self, audit_data, filename="audit_report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Customer Support Audit Report", ln=True, align="C")
        
        # Score
        pdf.set_font("Arial", "B", 14)
        score = audit_data.get("score", "N/A")
        pdf.cell(0, 10, f"Overall Score: {score}/100", ln=True)
        
        # Breakdown
        pdf.set_font("Arial", "", 12)
        breakdown = audit_data.get("breakdown", {})
        for key, val in breakdown.items():
            pdf.cell(0, 10, f"{key.capitalize()}: {val}", ln=True)
            
        # Summary
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Summary:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, audit_data.get("summary", "No summary provided."))
        
        # Violations
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Violations Detected:", ln=True)
        pdf.set_font("Arial", "I", 11)
        pdf.set_text_color(255, 0, 0) # Red
        violations = audit_data.get("violations", [])
        if violations:
            for v in violations:
                pdf.cell(0, 10, f"- {v}", ln=True)
        else:
            pdf.set_text_color(0, 128, 0) # Green
            pdf.cell(0, 10, "None", ln=True)
            
        pdf.set_text_color(0, 0, 0) # Reset color
        
        filepath = os.path.join(self.output_dir, filename)
        pdf.output(filepath)
        return filepath

    def send_email_alert(self, recipient_email, report_path, audit_summary, subject="Compliance Alert - Low Score or Violation"):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject

            body_text = f"""
            URGENT: Customer Support Interaction Flagged.

            Summary:
            {audit_summary}

            Please find the attached PDF report.
            """
            msg.attach(MIMEText(body_text, "plain"))

            # Attach PDF
            if report_path and os.path.exists(report_path):
                with open(report_path, "rb") as f:
                    pdf = MIMEApplication(f.read(), _subtype="pdf")
                    pdf.add_header("Content-Disposition", "attachment", filename=os.path.basename(report_path))
                    msg.attach(pdf)

            # Send via Gmail SMTP
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(self.sender_email, self.sender_pass)
            server.send_message(msg)
            server.quit()
            
            print(f"Alert email sent successfully to {recipient_email}!")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
