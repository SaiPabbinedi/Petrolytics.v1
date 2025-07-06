import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

def generate_reportlab_pdf(dfs_dict, chart_images_dict=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['h1'], fontSize=26, spaceAfter=30,
        alignment=1, textColor=colors.darkblue
    )
    section_header_style = ParagraphStyle(
        'SectionHeaderStyle', parent=styles['h2'], fontSize=20,
        spaceBefore=20, spaceAfter=14, alignment=0, textColor=colors.black
    )
    file_subheader_style = ParagraphStyle(
        'FileSubheaderStyle', parent=styles['h3'], fontSize=14,
        spaceBefore=12, spaceAfter=10, alignment=0, textColor=colors.HexColor("#555555")
    )
    chart_title_style = ParagraphStyle(
        'ChartTitleStyle', parent=styles['h4'], fontSize=12,
        spaceBefore=8, spaceAfter=4, alignment=1, textColor=colors.black
    )
    normal_text_style = styles['Normal']
    normal_text_style.fontSize = 10
    normal_text_style.leading = 13

    story = [Paragraph("Data Analysis Report", title_style), Spacer(1, 0.25 * inch)]

    if dfs_dict:
        story.append(Paragraph("Data Summaries (Top 5 Unique Values)", section_header_style))
        story.append(Spacer(1, 0.1 * inch))
        for file_name, df in dfs_dict.items():
            story.append(Paragraph(f"Summary for: {file_name}", file_subheader_style))
            story.append(Spacer(1, 0.05 * inch))
            data = [["Column Name", "Top 5 Unique Values"]]
            for col in df.columns:
                top_values = ", ".join(map(str, df[col].value_counts().head(5).index.tolist()))
                data.append([col, top_values])
            table = Table(data, colWidths=[doc.width*0.3, doc.width*0.7])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            story.append(table)
            story.append(Spacer(1, 0.3 * inch))

    if chart_images_dict:
        story.append(PageBreak())
        story.append(Paragraph("Visualizations", section_header_style))
        story.append(Spacer(1, 0.2 * inch))
        for title, img_buffer in chart_images_dict.items():
            story.append(Paragraph(title, chart_title_style))
            story.append(Spacer(1, 0.05 * inch))
            img_buffer.seek(0)
            story.append(Image(img_buffer, width=6.5*inch))
            story.append(Spacer(1, 0.25 * inch))
            story.append(Paragraph(f"Figure: {title}", normal_text_style))
            story.append(Spacer(1, 0.4 * inch))

    if not dfs_dict and not chart_images_dict:
        story.append(Paragraph("No data or charts available for reporting.", normal_text_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
