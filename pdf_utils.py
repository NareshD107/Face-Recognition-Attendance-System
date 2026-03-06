from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os

def generate_attendance_pdf(logs, output_path):
    """
    Generates a professional PDF report from attendance logs.
    logs: list of (name, date, time, subject)
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("Face Recognition Attendance Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Subtitle
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subtitle = Paragraph(f"Generated on: {generated_at}", styles['Normal'])
    elements.append(subtitle)
    elements.append(Spacer(1, 24))

    # Table Data
    data = [["Student Name", "Date", "Time", "Session/Subject"]]
    for log in logs:
        # Clean underscores from names for better readability
        clean_name = log[0].replace("_", " ")
        data.append([clean_name, log[1], log[2], log[3] if log[3] else "General"])

    # Table Styling
    table = Table(data, hAlign='LEFT', colWidths=[150, 100, 100, 150])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1f538d")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements.append(table)

    # Build PDF
    doc.build(elements)
    return True
