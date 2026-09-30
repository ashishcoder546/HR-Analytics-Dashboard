import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def build_pdf(filename="HR_Analytics_Complete_Interview_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    PRIMARY = colors.HexColor("#1E3A8A")     # Deep Navy
    SECONDARY = colors.HexColor("#2563EB")   # Royal Blue
    ACCENT = colors.HexColor("#D97706")      # Amber/Gold
    DARK_TEXT = colors.HexColor("#1F2937")   # Off Black
    LIGHT_BG = colors.HexColor("#F3F4F6")    # Light Gray
    CODE_BG = colors.HexColor("#1F2937")     # Dark Code Box

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=DARK_TEXT,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#E5E7EB"),
        backColor=CODE_BG,
        borderColor=colors.HexColor("#374151"),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=10,
        borderRadius=4
    )

    story = []

    # Title Block
    story.append(Paragraph("HR ANALYTICS & ATTRITION INTELLIGENCE", title_style))
    story.append(Paragraph("Complete Interview Preparation Guide & Project Walkthrough (End-to-End)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=15))

    # Section 1: Overview
    story.append(Paragraph("1. Project Executive Summary (Samajhne Ke Liye Overview)", h1_style))
    story.append(Paragraph(
        "<b>Is Project Ka Main Maqsad Kya Hai?</b><br/>"
        "Yeh project ek enterprise-level HR Analytics system hai. Companies mein employees company kyun chhodte hain (ise <b>Attrition</b> ya <b>Employee Turnover</b> kehte hain), iska data analyze karke HR Management ko decision-making mein help karna is project ka main objective hai.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Key Insights Discovered from Data (Main Findings):</b>", body_style
    ))
    story.append(Paragraph("• <b>Total Employees Analyzed:</b> 1,470 records (IBM HR Dataset)", bullet_style))
    story.append(Paragraph("• <b>Overall Attrition Rate:</b> 16.12% (237 employees left the company)", bullet_style))
    story.append(Paragraph("• <b>Biggest Attrition Driver:</b> Overtime Work! Overtime karne wale employees ka attrition <b>30.53%</b> hai, jabki non-overtime employees ka sirf <b>10.44%</b> hai (Nearly 3X difference!).", bullet_style))
    story.append(Paragraph("• <b>Highest Attrition Department:</b> Sales Department (20.63% attrition rate), followed by HR (19.05%) and R&D (13.84%).", bullet_style))
    story.append(Paragraph("• <b>Machine Learning Model Accuracy:</b> Random Forest Classifier achieved <b>0.8127 ROC-AUC Score</b> (81.3% accuracy).", bullet_style))

    story.append(Spacer(1, 10))

    # Section 2: Technology Stack
    story.append(Paragraph("2. Complete Tech Stack Used & Why (Kaunsa Tool Kyun Use Hua)", h1_style))
    
    tech_data = [
        [Paragraph("<b>Technology / Tool</b>", body_style), Paragraph("<b>What it Does in This Project</b>", body_style), Paragraph("<b>Key Concepts Used</b>", body_style)],
        [Paragraph("<b>SQL (T-SQL)</b>", body_style), Paragraph("Data cleaning, deduplication, creating views, and advanced window functions.", body_style), Paragraph("CTEs, ROW_NUMBER(), NTILE(4), CREATE VIEW, Aggregations", body_style)],
        [Paragraph("<b>Python & Pandas</b>", body_style), Paragraph("Automated Data Pipeline, EDA, statistical checks, data formatting.", body_style), Paragraph("read_csv(), groupby(), apply(), Risk Scoring", body_style)],
        [Paragraph("<b>Scikit-Learn (ML)</b>", body_style), Paragraph("Predicting employee turnover risk using machine learning.", body_style), Paragraph("RandomForestClassifier, ROC-AUC (0.8127), Feature Importance", body_style)],
        [Paragraph("<b>Streamlit & Plotly</b>", body_style), Paragraph("Building an interactive web dashboard application (app.py).", body_style), Paragraph("px.bar(), px.scatter(), sidebar filters, live metrics", body_style)],
        [Paragraph("<b>Power BI & DAX</b>", body_style), Paragraph("Business Intelligence dashboard & dynamic filter context reporting.", body_style), Paragraph("DAX Measures, CALCULATE, DIVIDE, KPI Cards, Slicers", body_style)]
    ]

    t_tech = Table(tech_data, colWidths=[1.3*inch, 3.2*inch, 2.5*inch])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_tech)

    story.append(Spacer(1, 15))

    # Section 3: Detailed File Walkthrough
    story.append(Paragraph("3. Detailed Walkthrough of Project Files (Har File Ka Kaam)", h1_style))

    story.append(Paragraph("A. SQL Scripts Suite (sql/ folder)", h2_style))
    story.append(Paragraph("<b>1. sql/01_data_cleaning.sql:</b> Clean karta hai dataset ko. Key technique: Duplicate rows hatane ke liye CTE aur <code>ROW_NUMBER() OVER (PARTITION BY EmpID ORDER BY EmpID)</code> use kiya gaya hai. Foreign characters/typos standardise kiye gaye hain.", body_style))
    story.append(Paragraph("<b>2. sql/02_analytical_views.sql:</b> Power BI aur Reporting ke liye 6 modular views banaye gaye hain (e.g. <code>vw_Attrition_By_Age</code>, <code>vw_Attrition_By_Department</code>, <code>vw_Attrition_By_Overtime</code>).", body_style))
    story.append(Paragraph("<b>3. sql/03_advanced_queries.sql:</b> Advanced queries implement ki hain. Example: Income Quartiles divide karne ke liye <code>NTILE(4) OVER (ORDER BY MonthlyIncome ASC)</code> use kiya gaya hai.", body_style))

    story.append(Paragraph("B. Python Scripts & Machine Learning (scripts/ folder & app.py)", h2_style))
    story.append(Paragraph("<b>1. scripts/hr_analytics_pipeline.py:</b> Automated ETL script. Data quality check karta hai aur retention risk scoring compute karta hai.", body_style))
    story.append(Paragraph("<b>2. scripts/train_attrition_model.py:</b> Machine Learning model script. Random Forest Classifier train karta hai (81.3% ROC-AUC score). Output mein Feature Importance calculate karke top drivers (Age, Income, Overtime) rank karta hai.", body_style))
    story.append(Paragraph("<b>3. app.py:</b> Interactive Streamlit Web App application. User browser me sliders/dropdowns change karke live graph dekh sakta hai.", body_style))

    story.append(Paragraph("C. Reports & Technical Documentation (reports/ folder)", h2_style))
    story.append(Paragraph("<b>1. reports/DAX_Measures_Reference.md:</b> Power BI DAX formulas ka documentation (Total Employees, Attrition Rate %, Overtime Attrition %).", body_style))
    story.append(Paragraph("<b>2. reports/HR_Attrition_Executive_Report.md:</b> Executive business insights report and HR leadership retention recommendations.", body_style))
    story.append(Paragraph("<b>3. reports/Interview_Preparation_Guide.md:</b> STAR method interview Q&A guide.", body_style))

    story.append(Spacer(1, 10))

    # Section 4: Key Interview Questions & Answers
    story.append(Paragraph("4. Key Interview Questions & How to Answer (Interview Q&A)", h1_style))

    q1 = "<b>Q1. Tell me about this HR Analytics project on your resume.</b><br/>" \
         "<b>How to Answer (60-sec Pitch):</b><br/>" \
         "\"In this project, I built an end-to-end workforce intelligence solution analyzing 1,470 employee records to identify key drivers of attrition. " \
         "I used SQL (CTEs, Window Functions, Views) for data cleaning, Python (Pandas & Scikit-Learn) for an automated ETL pipeline and a Random Forest classification model (ROC-AUC 0.8127), " \
         "and Power BI / Streamlit for dynamic visualization. A major finding was that Overtime employees experienced a 30.5% attrition rate compared to 10.4% for non-overtime staff.\""
    story.append(Paragraph(q1, body_style))

    q2 = "<b>Q2. How did you handle duplicate data in SQL?</b><br/>" \
         "<b>Technical Answer:</b><br/>" \
         "\"I used a Common Table Expression (CTE) with <code>ROW_NUMBER() OVER (PARTITION BY EmpID ORDER BY EmpID)</code>. " \
         "Any row with RowNum > 1 was identified as a duplicate and safely deleted, ensuring 100% data integrity.\""
    story.append(Paragraph(q2, body_style))

    q3 = "<b>Q3. What machine learning model did you use, and how did you evaluate it?</b><br/>" \
         "<b>Technical Answer:</b><br/>" \
         "\"I trained a Random Forest Classifier using Scikit-Learn with balanced class weights to handle class imbalance (since attrition is ~16%). " \
         "I evaluated the model using ROC-AUC score (achieving 0.8127) and analyzed Feature Importances, which revealed Monthly Income, Age, and Overtime as the top predictors of employee departure.\""
    story.append(Paragraph(q3, body_style))

    q4 = "<b>Q4. How did you handle DAX measures in Power BI?</b><br/>" \
         "<b>Technical Answer:</b><br/>" \
         "\"I created explicit DAX measures using <code>CALCULATE()</code>, <code>DIVIDE()</code>, and <code>COUNT()</code>. " \
         "For example: <code>Attrition Rate % = DIVIDE([Attrition Count], [Total Employees], 0) * 100</code>. " \
         "Explicit measures allow dynamic recalculation across all dashboard slicers.\""
    story.append(Paragraph(q4, body_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=10))
    story.append(Paragraph("<i>Document generated automatically for Ashish Yadav • HR Analytics & Attrition Intelligence Project Guide</i>", subtitle_style))

    doc.build(story)
    print(f"[SUCCESS] PDF generated at: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_pdf()
