import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

from src.kpi_engine import KPIEngine
from src.anomaly_detection import AnomalyDetector

def generate_report():
    os.makedirs('reports', exist_ok=True)
    filename = f"reports/Executive_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("Integrated Intelligence Platform", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Executive Summary Report", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    # 1. KPI Engine Summary
    try:
        engine = KPIEngine()
        summary = engine.get_executive_summary()
        
        kpi_data = [
            ["Metric", "Value"],
            ["Total Revenue", f"${summary['total_revenue']:,.2f}"],
            ["Total Net Profit", f"${summary['total_net_profit']:,.2f}"],
            ["Total Ad Spend", f"${summary['total_ad_spend']:,.2f}"],
            ["Total Conversions", f"{summary['total_conversions']:,.0f}"],
            ["Profit Adjusted ROAS", f"{summary['profit_adjusted_roas']:.2f}x"],
            ["Cost per Acquisition (CPA)", f"${summary['cost_per_acquisition']:,.2f}"]
        ]
        
        t = Table(kpi_data, colWidths=[200, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        story.append(t)
    except Exception as e:
        story.append(Paragraph(f"Error fetching data: {e}", styles['Normal']))
        
    story.append(Spacer(1, 24))
    
    # 2. Anomaly Detection
    story.append(Paragraph("Monitoring & Anomalies", styles['Heading2']))
    story.append(Spacer(1, 12))
    try:
        detector = AnomalyDetector()
        fin_anom = len(detector.detect_financial_anomalies())
        mkt_anom = len(detector.detect_marketing_anomalies())
        story.append(Paragraph(f"Detected {fin_anom} significant financial anomalies and {mkt_anom} marketing anomalies.", styles['Normal']))
    except Exception as e:
        story.append(Paragraph(f"Error running anomaly detection: {e}", styles['Normal']))
        
    doc.build(story)
    print(f"Report generated successfully: {filename}")
    return filename

if __name__ == "__main__":
    generate_report()
