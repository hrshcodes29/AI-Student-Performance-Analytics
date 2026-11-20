"""
Build the official Chandigarh University Industrial Internship Report to be EXACTLY 26 PAGES in Microsoft Word.
Candidate: Harsh Chandel (UID: 24BAI70240)
Project: AI STUDENT PERFORMANCE ANALYTICS AND PREDICTION SYSTEM USING MACHINE LEARNING
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_NAME = "Harsh_Chandel_Industrial_Internship_Report_AI_Student_Performance.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=90, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def setup_footer(section, is_front_matter=False):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    
    r_left = p.add_run("Harsh Chandel | UID: 24BAI70240 | CSE (AI & ML)              ")
    r_left.font.name = "Times New Roman"
    r_left.font.size = Pt(8.5)
    r_left.font.color.rgb = RGBColor(120, 120, 120)
    
    r_page = p.add_run("Page ")
    r_page.font.name = "Times New Roman"
    r_page.font.size = Pt(8.5)
    r_page.font.color.rgb = RGBColor(120, 120, 120)
    
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p._p.append(fldSimple)

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.style = doc.styles['Heading 1']
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.style = doc.styles['Heading 2']
    return p

def add_p(doc, text, bold_prefix="", italic=False, space_after=3.5, line_spacing=1.28):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.italic = italic
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.italic = True
    r.font.color.rgb = RGBColor(50, 50, 50)
    return p

def create_table(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        cell = hdr_cells[i]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            cell = row_cells[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            r = p.add_run(str(cell_value))
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(20, 20, 20)

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table

def add_appendix5_week(doc, week_no, dates_str, topic_covered, day_entries, outcomes, summary):
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_before = Pt(6)
    p_hdr.paragraph_format.space_after = Pt(2)
    r_hdr = p_hdr.add_run(f"WEEK {week_no} – {topic_covered.upper()}")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(10)
    r_hdr.font.bold = True

    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    col_widths = [Inches(1.4), Inches(5.1)]

    cell_w = table.rows[0].cells[0]
    cell_t = table.rows[0].cells[1]
    set_cell_background(cell_w, "1E293B")
    set_cell_background(cell_t, "1E293B")
    set_cell_margins(cell_w, 60, 60, 80, 80)
    set_cell_margins(cell_t, 60, 60, 80, 80)

    pw = cell_w.paragraphs[0]
    pw.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rw = pw.add_run(f"WEEK {week_no}\nDATES ({dates_str})")
    rw.font.name = "Times New Roman"
    rw.font.size = Pt(8.5)
    rw.font.bold = True
    rw.font.color.rgb = RGBColor(255, 255, 255)

    pt = cell_t.paragraphs[0]
    pt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = pt.add_run(f"TOPIC COVERED: {topic_covered.upper()}")
    rt.font.name = "Times New Roman"
    rt.font.size = Pt(8.5)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(255, 255, 255)

    for i in range(1, 6):
        cell_day = table.rows[i].cells[0]
        cell_desc = table.rows[i].cells[1]
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        set_cell_background(cell_day, bg)
        set_cell_background(cell_desc, bg)
        set_cell_margins(cell_day, 45, 45, 65, 65)
        set_cell_margins(cell_desc, 45, 45, 65, 65)

        p_d = cell_day.paragraphs[0]
        p_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rd = p_d.add_run(f"DAY-{i}\n[DATE]")
        rd.font.name = "Times New Roman"
        rd.font.size = Pt(8)
        rd.font.bold = True

        p_desc = cell_desc.paragraphs[0]
        p_desc.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_desc.paragraph_format.line_spacing = 1.05
        rdesc = p_desc.add_run(day_entries[i - 1])
        rdesc.font.name = "Times New Roman"
        rdesc.font.size = Pt(8)

    for row in table.rows:
        row.cells[0].width = col_widths[0]
        row.cells[1].width = col_widths[1]

    p_out = doc.add_paragraph()
    p_out.paragraph_format.space_before = Pt(2)
    p_out.paragraph_format.space_after = Pt(1)
    p_out.paragraph_format.line_spacing = 1.05
    r_ot = p_out.add_run("Key Outcomes: ")
    r_ot.font.name = "Times New Roman"
    r_ot.font.size = Pt(8.5)
    r_ot.font.bold = True
    r_ot_txt = p_out.add_run(outcomes)
    r_ot_txt.font.name = "Times New Roman"
    r_ot_txt.font.size = Pt(8.5)

    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(1)
    p_sum.paragraph_format.space_after = Pt(4)
    p_sum.paragraph_format.line_spacing = 1.05
    r_st = p_sum.add_run("Weekly Summary: ")
    r_st.font.name = "Times New Roman"
    r_st.font.size = Pt(8.5)
    r_st.font.bold = True
    r_st_txt = p_sum.add_run(summary)
    r_st_txt.font.name = "Times New Roman"
    r_st_txt.font.size = Pt(8.5)

    return table

def generate_report_26_pages():
    doc = Document()
    
    # Section 1: Cover Page
    sec_cover = doc.sections[0]
    sec_cover.page_width = Inches(8.27)
    sec_cover.page_height = Inches(11.69)
    sec_cover.top_margin = Inches(0.9)
    sec_cover.bottom_margin = Inches(0.9)
    sec_cover.left_margin = Inches(1.25)
    sec_cover.right_margin = Inches(0.9)
    sec_cover.different_first_page_header_footer = True

    # ====================================================
    # PAGE 1: COVER PAGE (Appendix 1)
    # ====================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run("INDUSTRIAL INTERNSHIP REPORT")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(16)
    p.paragraph_format.line_spacing = 1.3
    r = p.add_run("AI STUDENT PERFORMANCE ANALYTICS AND PREDICTION SYSTEM USING MACHINE LEARNING")
    r.font.name = "Times New Roman"
    r.font.size = Pt(18)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Submitted in Partial Fulfillment of the Requirements for the Degree of")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.italic = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Bachelor of Engineering\nin\nComputer Science Engineering – (Artificial Intelligence & Machine Learning)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("by")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.italic = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(16)
    r = p.add_run("HARSH CHANDEL\n(UID: 24BAI70240)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True

    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(8)
    p_logo.paragraph_format.space_after = Pt(12)
    r_logo = p_logo.add_run()
    logo_path = os.path.join(os.path.dirname(__file__), 'assets_template', 'word', 'media', 'image1.png')
    if not os.path.exists(logo_path):
        logo_path = 'assets_template/word/media/image1.png'
    r_logo.add_picture(logo_path, width=Inches(1.0))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run("AIT – Computer Science and Engineering\nUniversity Institute of Engineering\nChandigarh University, Gharuan")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("NOVEMBER 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True

    # ====================================================
    # PAGE 2: BONAFIDE CERTIFICATE (Appendix 2)
    # ====================================================
    sec_front = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_footer(sec_front, is_front_matter=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("APPENDIX 2")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(20)
    r = p.add_run("BONAFIDE CERTIFICATE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0  # Double line spacing as specified
    p.paragraph_format.space_after = Pt(18)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(
        "This is to certify that the industrial internship report entitled “AI STUDENT PERFORMANCE ANALYTICS AND PREDICTION SYSTEM USING MACHINE LEARNING” "
        "submitted by “HARSH CHANDEL (UID: 24BAI70240)” in partial fulfillment of the requirements for the award of the Degree of "
        "Bachelor of Engineering in Computer Science Engineering (Artificial Intelligence & Machine Learning Specialization) "
        "is a bonafide record of the work carried out during the six-week industrial internship/certification-based learning period "
        "under my guidance and supervision at Chandigarh University, Gharuan."
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(28)
    p.paragraph_format.space_after = Pt(3)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run("<<Signature of Program Leader>>\nSIGNATURE\n[PROGRAM LEADER NAME]\nProgram Leader – AI & ML Specialization\n[ACADEMIC DESIGNATION]\n[DEPARTMENT]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(24)
    p.paragraph_format.space_after = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run("This project report was evaluated by us on: [DATE]\n\nEXTERNAL EXAMINER\n[EXAMINER NAME / EID]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    # ====================================================
    # PAGE 3: DECLARATION BY CANDIDATE (Appendix 3)
    # ====================================================
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("APPENDIX 3")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(20)
    r = p.add_run("Declaration by Candidate")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.space_after = Pt(14)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(
        "I hereby declare that this Industrial Internship Report entitled “AI STUDENT PERFORMANCE ANALYTICS AND PREDICTION SYSTEM USING MACHINE LEARNING” "
        "is prepared by me as part of the academic requirements for the Bachelor of Engineering in Computer Science Engineering "
        "with specialization in Artificial Intelligence and Machine Learning at Chandigarh University.\n\n"
        "The report presents my genuine learning, understanding, study, and developmental work related to Artificial Intelligence fundamentals, "
        "machine learning methodologies, student performance analytics, predictive modeling, data preprocessing, model evaluation, and the "
        "implementation of an enterprise academic analytics web application.\n\n"
        "All information, concepts, empirical benchmarks, and references taken from academic literature and technical documentation have been "
        "appropriately acknowledged and cited in accordance with institutional academic integrity standards. I declare that I have not knowingly "
        "plagiarized any part of this report. I aver that if any part of the report is found to be plagiarized, I shall take full academic responsibility for it."
    )
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(36)
    p.paragraph_format.space_after = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run("<<Signature of Candidate>>\nHARSH CHANDEL\nUID: 24BAI70240")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run("Place: Chandigarh University, Gharuan\nDate: [DATE]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)

    # ====================================================
    # PAGE 4: ABSTRACT
    # ====================================================
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(16)
    r = p.add_run("ABSTRACT")
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True

    abstract_text = (
        "Educational data mining and learning analytics represent a critical transformative frontier in higher education, offering educators the tools "
        "to proactively identify students experiencing academic distress before end-of-semester evaluations. Traditional academic monitoring approaches "
        "typically rely on post-examination retrospectives, which often detect student failure too late to execute meaningful pedagogical remediation. "
        "This industrial internship project, titled “AI Student Performance Analytics and Prediction System Using Machine Learning,” was developed as a "
        "six-week capstone initiative aligned with the curriculum of the Microsoft AI-901: Azure AI Fundamentals certification at Chandigarh University. "
        "The primary objective of this project is to develop an end-to-end, data-driven academic analytics and predictive platform capable of analyzing multi-dimensional "
        "student academic and behavioral indicators, identifying at-risk learners, predicting composite final scores, and generating actionable prescriptive interventions.\n\n"
        "The system incorporates a complete machine learning lifecycle including data ingestion, schema validation, median-based missing value imputation, "
        "standard feature scaling, and one-hot categorical encoding. The modeling architecture addresses both continuous numerical grade estimation via supervised regression "
        "and discrete academic vulnerability tiering via supervised multi-class classification. Benchmark evaluations conducted across Linear Regression, Ridge Regression, "
        "Decision Tree Regressor, and Random Forest Regressor demonstrated that the Linear Regression model achieved optimal generalization on the test split "
        "(Coefficient of Determination R² = 0.9043, Mean Absolute Error MAE = 2.719 points, Root Mean Squared Error RMSE = 3.429 points). For multi-class risk categorization "
        "(Low Risk, Moderate Risk, High Risk), the Random Forest Classifier yielded superior performance, achieving a classification accuracy of 93.00% and an out-of-sample "
        "weighted F1-Score of 0.9305.\n\n"
        "The platform delivers an enterprise-grade dark-themed web interface built using Streamlit, featuring an Executive KPI Dashboard, AI Student Prediction form "
        "with feature impact waterfall decomposition, an Individual Student Dossier Explorer with multidimensional radar profiles, an Early-Warning At-Risk Intelligence registry, "
        "an Exploratory Academic Insights suite with Pearson correlation matrices, and a Prescriptive AI Recommendation Engine with downloadable action plans. Furthermore, "
        "the application strictly integrates the Six Microsoft Responsible AI Principles (Fairness, Reliability & Safety, Privacy & Security, Inclusiveness, Transparency, and "
        "Accountability), reinforcing that statistical model inferences serve exclusively as decision-support alerts for human educators and must never replace teacher empathy or pedagogical judgment."
    )
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.0  # Single spacing
    p.paragraph_format.space_after = Pt(12)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(abstract_text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(4)
    r_kw = p.add_run("Keywords: ")
    r_kw.font.name = "Times New Roman"
    r_kw.font.size = Pt(11)
    r_kw.font.bold = True
    r_kwt = p.add_run("Artificial Intelligence, Machine Learning, Student Performance Prediction, Academic Analytics, Data Preprocessing, Predictive Modeling, Responsible AI.")
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.size = Pt(11)

    # ====================================================
    # PAGE 5: TABLE OF CONTENTS (Appendix 4)
    # ====================================================
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("APPENDIX 4")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("TABLE OF CONTENTS")
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.font.bold = True

    toc_items = [
        ("CHAPTER NO.", "TITLE", "PAGE NO.", True),
        ("", "ABSTRACT", "iv", True),
        ("", "LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE", "vi", True),
        ("1.", "INTRODUCTION", "1", True),
        ("1.1", "Introduction to Artificial Intelligence", "1", False),
        ("1.2", "Introduction to Machine Learning", "1", False),
        ("1.3", "Background of the Problem & Problem Statement", "2", False),
        ("1.4", "Importance and Objectives of the Project", "2", False),
        ("1.5", "Scope and Boundary Conditions", "3", False),
        ("1.6", "Related Work and Literature Review", "3", False),
        ("1.7", "Organization of the Report", "4", False),
        ("2.", "AI FUNDAMENTALS AND METHODOLOGY", "5", True),
        ("2.1", "AI Fundamentals and AI-901 Learning Context", "5", False),
        ("2.2", "Machine Learning Approach and Lifecycle", "5", False),
        ("2.3", "Supervised Learning, Regression, and Classification", "6", False),
        ("2.4", "Dataset Preparation and Preprocessing Pipeline", "6", False),
        ("2.5", "Model Selection and Evaluation Framework", "7", False),
        ("2.6", "Responsible AI Methodology", "8", False),
        ("3.", "SYSTEM DESIGN AND IMPLEMENTATION", "9", True),
        ("3.1", "System Overview and Architecture", "9", False),
        ("3.2", "Hardware and Software Requirements", "10", False),
        ("3.3", "Dataset Description and Feature Engineering", "10", False),
        ("3.4", "Machine Learning Model Development & Prediction", "11", False),
        ("3.5", "Student Risk Analysis and Recommendation Engine", "11", False),
        ("3.6", "Dashboard Design, CSV Ingestion, and Workflow", "12", False),
        ("4.", "SIX-WEEK INTERNSHIP WEEKLY REPORT", "13", True),
        ("4.1", "Week 1: AI Fundamentals and Project Planning", "13", False),
        ("4.2", "Week 2: Machine Learning and Exploratory Data Analysis", "13", False),
        ("4.3", "Week 3: Data Preprocessing and Feature Pipeline Engineering", "14", False),
        ("4.4", "Week 4: Machine Learning Model Development and Tuning", "14", False),
        ("4.5", "Week 5: Analytics Dashboard and Application Interface Development", "15", False),
        ("4.6", "Week 6: System Testing, Model Evaluation, and Documentation", "15", False),
        ("5.", "RESULTS, ANALYSIS AND DISCUSSION", "16", True),
        ("5.1", "Overview of Experimental Results & Dashboard Analytics", "16", False),
        ("5.2", "Model Evaluation and Benchmark Verification", "16", False),
        ("5.3", "Empirical Findings, Risk Insights, and Limitations", "17", False),
        ("6.", "CONCLUSIONS AND RECOMMENDATIONS", "18", True),
        ("6.1", "Conclusions, Recommendations, and Future Scope", "18", False),
        ("6.2", "Internship Technical and Professional Learning Outcomes", "18", False),
        ("", "APPENDICES (Syllabus, Certificate Placeholders, Layouts)", "19", True),
        ("", "REFERENCES", "20", True)
    ]

    toc_table = doc.add_table(rows=len(toc_items), cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_table, color="FFFFFF", val="none")

    for idx, (num, title, page_no, is_major) in enumerate(toc_items):
        r_cells = toc_table.rows[idx].cells
        set_cell_margins(r_cells[0], 10, 10, 20, 20)
        set_cell_margins(r_cells[1], 10, 10, 20, 20)
        set_cell_margins(r_cells[2], 10, 10, 20, 20)
        
        p0 = r_cells[0].paragraphs[0]
        r0 = p0.add_run(num)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9.5 if not is_major else 10)
        r0.font.bold = is_major
        
        p1 = r_cells[1].paragraphs[0]
        r1 = p1.add_run(title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5 if not is_major else 10)
        r1.font.bold = is_major
        
        p2 = r_cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2 = p2.add_run(page_no)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(9.5 if not is_major else 10)
        r2.font.bold = is_major

    toc_table.rows[0].cells[0].width = Inches(1.1)
    toc_table.rows[0].cells[1].width = Inches(4.7)
    toc_table.rows[0].cells[2].width = Inches(0.7)

    # ====================================================
    # PAGE 6: NOMENCLATURE
    # ====================================================
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run("LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.font.bold = True

    nom_data = [
        ["AI", "Artificial Intelligence"],
        ["ML", "Machine Learning"],
        ["CSV", "Comma-Separated Values"],
        ["EDA", "Exploratory Data Analysis"],
        ["KPI", "Key Performance Indicator"],
        ["MAE", "Mean Absolute Error"],
        ["MSE", "Mean Squared Error"],
        ["RMSE", "Root Mean Squared Error"],
        ["R²", "Coefficient of Determination"],
        ["API", "Application Programming Interface"],
        ["UI", "User Interface"],
        ["UX", "User Experience"],
        ["ID", "Identification"],
        ["CPU", "Central Processing Unit"],
        ["RAM", "Random Access Memory"],
        ["NLP", "Natural Language Processing"],
        ["ROC", "Receiver Operating Characteristic"],
        ["F1 Score", "Harmonic Mean of Precision and Recall"],
        ["XAI", "Explainable Artificial Intelligence"],
        ["EWIS", "Early Warning Intervention System"],
        ["FERPA", "Family Educational Rights and Privacy Act"],
        ["GDPR", "General Data Protection Regulation"],
        ["ETL", "Extract, Transform, Load"],
        ["OHE", "One-Hot Encoding"]
    ]
    create_table(doc, ["Abbreviation / Symbol", "Full Nomenclature / Definition"], nom_data, [Inches(2.0), Inches(4.5)])

    # ====================================================
    # SECTION 3: MAIN REPORT CONTENT (Pages 7 to 26)
    # ====================================================
    sec_main = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_footer(sec_main, is_front_matter=False)

    # ----------------------------------------------------
    # CHAPTER 1 - INTRODUCTION (PAGES 7 TO 10 -> EXACTLY 4 PAGES)
    # ----------------------------------------------------
    add_h1(doc, "CHAPTER 1: INTRODUCTION")

    add_h2(doc, "1.1 Introduction to Artificial Intelligence")
    add_p(
        doc,
        "Artificial Intelligence (AI) represents the domain of computer science devoted to engineering synthetic systems capable of executing "
        "tasks that traditionally demand human cognitive agency. These capabilities encompass visual perception, contextual language comprehension, "
        "autonomous inductive reasoning, knowledge representation, and predictive inference from historical empirical observations. From its academic "
        "inception at the Dartmouth Conference of 1956 through the development of symbolic logic paradigms and expert systems, AI has transitioned "
        "dramatically over the past two decades into a data-driven computational methodology powered by statistical machine learning."
    )
    add_p(
        doc,
        "In contemporary classification, AI systems are categorized into Narrow AI (Artificial Narrow Intelligence, ANI) and Artificial General Intelligence (AGI). "
        "Whereas AGI envisions broad, human-like generalized cognition across arbitrary domains, Narrow AI is engineered to excel at precisely scoped operational tasks. "
        "The application developed in this industrial internship operates strictly within the paradigm of Narrow AI, deploying specialized predictive algorithms "
        "to discover non-obvious patterns within academic performance records. By evaluating student interaction logs, assignment submission cadences, and continuous "
        "assessment milestones, narrow AI platforms function as cognitive force-multipliers for human educators, replacing retrospective intuition with proactive empirical foresight."
    )

    add_h2(doc, "1.2 Introduction to Machine Learning")
    add_p(
        doc,
        "Machine Learning (ML) constitutes the core operational engine of modern applied artificial intelligence. Rather than relying on human programmers "
        "to manually construct rigid, rule-based algorithmic decision trees, machine learning models ingest structured historical datasets and mathematically "
        "estimate functional mappings between input features and target outcomes. Tom M. Mitchell famously defined machine learning: “A computer program is said "
        "to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E.”"
    )
    add_p(
        doc,
        "The machine learning continuum is formally divided into three primary paradigms: supervised learning, unsupervised learning, and reinforcement learning. "
        "Supervised learning trains models on labeled training pairs (X, y), adjusting internal parameters through loss minimization algorithms such that the model "
        "generalizes accurately to unobserved test samples. Unsupervised learning discovers latent clustering structures or manifold representations within unlabeled data. "
        "Reinforcement learning optimizes sequential decision policies through environmental reward and penalty signals. This internship project primarily harnesses "
        "supervised learning, integrating both regression (predicting continuous final examination percentages) and multi-class classification (categorizing students into "
        "actionable academic vulnerability tiers: Low Risk, Moderate Risk, and High Risk)."
    )

    add_h2(doc, "1.3 Background of the Problem")
    add_p(
        doc,
        "Higher educational institutions face systemic operational challenges in monitoring and safeguarding student academic progression. In conventional academic structures, "
        "student performance evaluation is largely retrospective. Summative examinations administered at the conclusion of a semester provide authoritative marks, but they arrive "
        "far too late to execute meaningful instructional remediation. When a student receives a failing mark on a final comprehensive examination, the pedagogical opportunity "
        "to address foundational misconceptions, encourage attendance recovery, or offer targeted peer tutoring has already expired."
    )
    add_p(
        doc,
        "Furthermore, modern university cohorts frequently encompass hundreds of students per academic stream, creating an acute teacher-to-student ratio imbalance. "
        "Faculty members and academic counselors cannot realistically review the daily study habits, attendance fluctuations, and formative assessment scores of every student manually. "
        "Subtle behavioral warning signs—such as a progressive decline in lecture attendance below institutional thresholds, irregular assignment submissions, or localized weakness "
        "in analytical coursework—frequently go unnoticed until academic crisis becomes irreversible. Consequently, there is an urgent institutional necessity for automated, "
        "intelligent analytics platforms that continuously ingest academic indicators and flag at-risk learners weeks before high-stakes semester assessments occur."
    )

    add_h2(doc, "1.4 Problem Statement")
    add_p(
        doc,
        "The primary challenge addressed in this investigation is formally articulated as follows: How can educational institutions utilize supervised machine learning "
        "and interactive data analytics to accurately predict student academic outcomes, identify primary behavioral vulnerability factors, and deliver prioritized, "
        "actionable academic recommendations without compromising algorithmic fairness, student privacy, or human educator oversight?"
    )
    add_p(
        doc,
        "To resolve this challenge, the system must formulate a mathematically rigorous pipeline capable of handling missing data, normalizing heterogeneous numerical features, "
        "encoding categorical attributes, and outputting calibrated predictions accompanied by transparent feature impact explanations, thereby serving as an empathetic decision-support "
        "tool rather than an opaque, automated academic gatekeeper."
    )

    add_h2(doc, "1.5 Importance of the Project")
    add_p(
        doc,
        "The development of an AI Student Performance Analytics and Prediction System carries substantial pedagogical, institutional, and technical significance:"
    )
    add_bullet(doc, "Proactive Early Intervention: Enables faculty advisors to schedule remedial tutoring and counseling sessions before final exams take place.", "1. ")
    add_bullet(doc, "Data-Driven Institutional Resource Allocation: Directs limited institutional resources, such as teaching assistants and remedial lab hours, to the cohorts and courses exhibiting the greatest vulnerability.", "2. ")
    add_bullet(doc, "Personalized Student Action Directives: Replaces generic admonitions with concrete, empirical recommendations tailored to individual student gaps (e.g., target daily study hours, specific subject drills).", "3. ")
    add_bullet(doc, "Educational Equity and Transparency: De-biases decision-making by anchoring support allocation on demonstrated academic behaviors rather than subjective impressionism.", "4. ")
    add_bullet(doc, "Practical Demonstration of Microsoft AI-901 Principles: Connects fundamental theoretical competencies—such as loss optimization, model evaluation metrics, and responsible AI governance—with an active production-style software artifact.", "5. ")

    add_h2(doc, "1.6 Objectives of the Project")
    add_p(
        doc,
        "To achieve a comprehensive, academically sound analytics platform, the project established the following explicit, measurable objectives:"
    )
    add_bullet(doc, "To construct a statistically consistent, reproducible student performance benchmark dataset comprising 1,000 student records across 20 distinct academic, behavioral, and demographic features.", "Objective 1: ")
    add_bullet(doc, "To engineer an automated data preprocessing pipeline utilizing Scikit-learn that executes median imputation, standard scaling, and one-hot encoding without target leakage.", "Objective 2: ")
    add_bullet(doc, "To benchmark, tune, and evaluate multiple supervised regression algorithms (Linear Regression, Ridge, Decision Tree, Random Forest) for final score prediction, achieving an out-of-sample R² score exceeding 0.85.", "Objective 3: ")
    add_bullet(doc, "To benchmark, tune, and evaluate multiple supervised classification algorithms (Logistic Regression, Decision Tree, Random Forest) for multi-tier risk classification, achieving an out-of-sample accuracy exceeding 90.0%.", "Objective 4: ")
    add_bullet(doc, "To implement an Explainable AI (XAI) feature attribution mechanism that calculates individual feature contributions against cohort benchmarks, visually explaining every prediction.", "Objective 5: ")
    add_bullet(doc, "To develop an intelligent, rules-driven Prescriptive Recommendation Engine that converts diagnostic scores into prioritized academic recovery plans with estimated performance gains.", "Objective 6: ")
    add_bullet(doc, "To design and deploy a full-stack, enterprise-grade dark-themed web dashboard utilizing Streamlit and Plotly, comprising 9 complete functional modules.", "Objective 7: ")
    add_bullet(doc, "To integrate the Six Microsoft Responsible AI Principles into the system's operational architecture and user-facing disclaimers, ensuring ethical compliance and human educator oversight.", "Objective 8: ")

    add_h2(doc, "1.7 Scope and Boundary Conditions")
    add_p(
        doc,
        "The scope of this project encompasses the statistical modeling of secondary and undergraduate student cohorts across quantitative academic features (attendance rate, "
        "daily study hours, previous semester examination marks, continuous assignment completion rate, and diagnostic marks in Mathematics, Science, English, and Computer Science). "
        "The system delivers real-time inference, interactive cohort exploratory data analysis, dynamic CSV dataset upload with automated schema validation, and downloadable analytical reports."
    )
    add_p(
        doc,
        "Boundary Conditions & Explicit Non-Claims: To maintain academic credibility and ethical integrity, the boundaries of this system are explicitly demarcated: "
        "(1) The primary dataset utilized for demonstration is a statistically coherent synthetic benchmark; it does not claim to represent real-world confidential institutional records; "
        "(2) The predictive models generate probabilistic approximations based on historical correlation, not deterministic certainties; "
        "(3) The platform is engineered exclusively as a decision-support aid for human educators and academic advisors; it is not designed, authorized, or intended to execute "
        "automated admissions decisions, disciplinary sanctions, or terminal academic grading without human verification."
    )

    add_h2(doc, "1.8 Related Work and Literature Review")
    add_p(
        doc,
        "The intersection of machine learning and academic outcome forecasting has garnered extensive scholarly attention over the past decade under the umbrellas of Educational Data Mining (EDM) "
        "and Learning Analytics (LA). A foundational survey by Romero and Ventura [1] established the taxonomy of educational data mining, identifying performance prediction, student clustering, "
        "and curriculum sequencing as the primary application pillars of educational machine learning."
    )
    add_p(
        doc,
        "In a prominent empirical study, Cortez and Silva [2] utilized supervised regression and classification models to predict student failure in secondary school mathematics and language curricula "
        "in Portugal. Utilizing attributes ranging from demographic backgrounds to previous trimester evaluations, Cortez and Silva evaluated Decision Trees, Random Forests, Neural Networks, "
        "and Support Vector Machines. Their findings established that previous academic evaluation scores (past grades) and class attendance represent the two single strongest predictors of future academic success, "
        "a conclusion strongly corroborated by the empirical correlation findings (r = 0.82 and r = 0.74) discovered in this project's analysis."
    )
    add_p(
        doc,
        "Baker and Inventado [3] expanded the literature by examining operational early-warning intervention systems (EWIS) across North American school districts. Their research demonstrated that while complex "
        "deep neural networks occasionally yield marginally superior curve-fitting accuracy on massive administrative datasets, shallower ensemble models—such as Random Forests and regularized linear regressors—"
        "offer vastly superior interpretability and trust among pedagogical stakeholders. Human educators routinely reject black-box models that cannot explain the underlying drivers of a risk classification, "
        "underscoring the critical necessity of the feature impact decomposition and Responsible AI frameworks incorporated into this system's architecture."
    )

    add_h2(doc, "1.9 Organization of the Report")
    add_p(
        doc,
        "The remainder of this industrial internship report is organized into the following structured chapters: "
        "Chapter 2 reviews core AI-901 competencies, mathematical formulations of supervised learning, and responsible AI governance. "
        "Chapter 3 details the end-to-end technical system architecture, hardware/software specifications, Scikit-learn pipelines, and dashboard design. "
        "Chapter 4 outlines the progressive day-by-day technical tasks, learning outcomes, and weekly milestones achieved during the six-week internship period. "
        "Chapter 5 presents the empirical evaluation metrics, multi-model benchmark comparisons, confusion matrices, and limitations. "
        "Chapter 6 summarizes key conclusions, practical stakeholder recommendations, future research scope, and professional learning outcomes. "
        "Finally, Appendices and References provide supporting course syllabus details, certificates, UI layouts, and verified academic literature citations."
    )

    # ----------------------------------------------------
    # CHAPTER 2 - AI FUNDAMENTALS & METHODOLOGY (PAGES 11 TO 14 -> EXACTLY 4 PAGES)
    # ----------------------------------------------------
    doc.add_page_break()
    add_h1(doc, "CHAPTER 2: AI FUNDAMENTALS AND METHODOLOGY")

    add_h2(doc, "2.1 AI Fundamentals and AI-901 Learning Context")
    add_p(
        doc,
        "The conceptual foundation of this industrial internship project is directly derived from the curriculum of the Microsoft AI-901: Azure AI Fundamentals certification. "
        "The AI-901 framework establishes a structured, foundational understanding of core artificial intelligence workloads, machine learning principles, and responsible deployment ethics. "
        "Within this curriculum, artificial intelligence workloads are demarcated into distinct functional domains:"
    )
    add_bullet(doc, "Machine Learning: Predictive modeling using numerical and tabular data to identify relationships and forecast future values.", "1. ")
    add_bullet(doc, "Computer Vision: Algorithmic visual processing of images and video streams for classification, object detection, and spatial recognition.", "2. ")
    add_bullet(doc, "Natural Language Processing (NLP): Computational linguistics, semantic analysis, entity extraction, sentiment analysis, and machine translation.", "3. ")
    add_bullet(doc, "Document Intelligence & Knowledge Mining: Extraction of structured tabular information from unstructured documents, PDFs, and forms.", "4. ")
    add_bullet(doc, "Generative AI: Foundation models and conversational agents generating synthetic text, code, and multimedia representations.", "5. ")
    add_bullet(doc, "Responsible AI: Ethical governance ensuring algorithmic fairness, safety, transparency, privacy, inclusiveness, and human accountability.", "6. ")
    add_p(
        doc,
        "This capstone project translates the theoretical principles of the machine learning and responsible AI workloads into a fully functioning, locally hosted and cloud-deployable software application. "
        "While cloud services such as Azure Machine Learning Studio provide enterprise infrastructure for distributed training, the core mathematical abstractions—loss functions, gradient minimization, "
        "train/test partitioning, metric evaluation, and bias auditing—remain universal. In accordance with the accuracy guidelines of this report, all training, feature scaling, and inference operations "
        "were executed directly using open-source Python, Scikit-learn, and Streamlit, faithfully mirroring the algorithmic workflows taught within the Microsoft AI curriculum without falsely asserting "
        "active commercial cloud billing."
    )

    add_h2(doc, "2.2 Machine Learning Approach and Lifecycle")
    add_p(
        doc,
        "The system adheres to the standard CRISP-DM (Cross-Industry Standard Process for Data Mining) and Microsoft Machine Learning lifecycle. The workflow proceeds through eight sequential phases: "
        "(1) Problem Formulation, (2) Data Ingestion and Validation, (3) Exploratory Data Analysis, (4) Data Preprocessing and Imputation, (5) Feature Scaling and Categorical Encoding, "
        "(6) Multi-Model Training and Hyperparameter Tuning, (7) Metric Benchmarking and Verification, and (8) Deployment and Live Inference."
    )
    add_p(
        doc,
        "[Dataset Ingestion] ➔ [Schema Bounds Validation] ➔ [Median/Mode Imputation] ➔ [StandardScaler & OneHotEncoder] ➔ "
        "[80/20 Stratified Split] ➔ [Multi-Model Benchmarking] ➔ [Holdout Test Evaluation] ➔ [Artifact Persistence (Joblib)] ➔ [Streamlit Live Serving]",
        italic=True, space_after=6
    )
    add_caption(doc, "Figure 2.1: End-to-End Supervised Machine Learning Engineering Lifecycle")

    add_h2(doc, "2.3 Supervised Learning Paradigms")
    add_p(
        doc,
        "Supervised learning operates under the mathematical assumption that there exists an underlying data-generating function f(X) such that: y = f(X) + ε, "
        "where X represents a vector of observable academic input features, y represents the target academic outcome, and ε represents irreducible zero-mean Gaussian observation noise. "
        "During model optimization, the learning algorithm searches a parameterized hypothesis class H to find a parameter vector θ* that minimizes an empirical loss function L over the training dataset: "
        "θ* = argmin_θ (1/N) Σ L(y_i, f(x_i; θ)) + λ R(θ), where R(θ) represents a regularization penalty (such as L1 Lasso or L2 Ridge) scaled by hyperparameter λ to prevent model overfitting. "
        "In this project, supervised learning is bifurcated into two coordinated estimation tasks: continuous score regression and discrete risk tier classification."
    )

    add_h2(doc, "2.4 Regression and Classification Approaches")
    add_p(
        doc,
        "Regression and classification address complementary dimensions of student academic performance analytics:"
    )
    add_bullet(doc, "Continuous Score Regression: The target variable y_reg ∈ [0, 100] is continuous, representing a student's estimated composite final examination mark. Regression provides granular, fine-grained performance forecasting, enabling counselors to gauge whether a student is tracking toward distinction (≥85%), a first-class pass (70-84%), a second-class pass (55-69%), or course failure (<55%).", "Regression: ")
    add_bullet(doc, "Multi-Class Risk Classification: The target variable y_clf ∈ {Low Risk, Moderate Risk, High Risk} is discrete. While continuous scores provide fine-grained predictions, institutional counselors require unambiguous categorical triage. Students flagged as 'High Risk' trigger immediate early-warning workflows, whereas 'Low Risk' students proceed along standard monitoring tracks.", "Classification: ")

    add_h2(doc, "2.5 Dataset Preparation and Attribute Architecture")
    add_p(
        doc,
        "Data quality is paramount in academic analytics. The project features a benchmark dataset comprising 1,000 student records structured across 20 distinct columns. "
        "The attributes encompass three fundamental educational dimensions: (1) Behavioral Indicators (daily study hours, class attendance rate, assignment completion rate, sleep hours), "
        "(2) Formative & Diagnostic Marks (previous semester examination score, diagnostic marks in Mathematics, Science, English, Computer Science, and count of weak subjects), and "
        "(3) Environmental & Demographic Factors (grade level, gender, parental education level, home high-speed internet access, and extracurricular participation)."
    )

    add_h2(doc, "2.6 Data Preprocessing and Leakage Prevention")
    add_p(
        doc,
        "Data preprocessing is executed via a rigorous Scikit-learn Pipeline architecture to eliminate data leakage. Target leakage occurs when information from outside the training dataset "
        "is inadvertently utilized to train the model, producing overly optimistic validation metrics that collapse in production. To prevent leakage:"
    )
    add_bullet(doc, "Strict Train/Test Partitioning: The dataset is split into an 80% training set (N = 800) and a 20% holdout test set (N = 200) using a fixed random seed (42). Stratification is enforced along risk tiers to guarantee identical class distribution across both partitions.", "1. ")
    add_bullet(doc, "Transformer Fitting Encapsulation: All scalers and imputers are fitted strictly on the 80% training split (preprocessor.fit(X_train)). The holdout test set and prospective user queries are transformed strictly using the pre-fitted parameters (preprocessor.transform(X_test)).", "2. ")
    add_bullet(doc, "Numerical Standardization: Numerical features are standardized using StandardScaler to exhibit zero mean and unit variance (z = (x - μ) / σ), preventing features with wide numerical ranges from dominating gradient updates.", "3. ")
    add_bullet(doc, "Categorical One-Hot Encoding: Nominal features are transformed via OneHotEncoder(handle_unknown='ignore', sparse_output=False), mapping non-ordinal categories into orthogonal binary vectors.", "4. ")

    add_h2(doc, "2.7 Machine Learning Model Selection")
    add_p(
        doc,
        "To identify the optimal predictive models, four candidate regression algorithms and three candidate classification algorithms were implemented and empirically compared:"
    )
    add_bullet(doc, "Linear Regression (Ordinary Least Squares): Fits an optimal hyper-plane by minimizing the residual sum of squares. Offers complete mathematical transparency, low computational overhead, and excellent baseline stability.", "• ")
    add_bullet(doc, "Ridge Regression (L2 Regularization): Introduces an L2 penalty on coefficient magnitudes (α = 1.0) to stabilize collinear predictors, such as correlated subject examination marks.", "• ")
    add_bullet(doc, "Decision Tree Regressor / Classifier: Non-parametric tree models that recursively partition feature space based on variance reduction (regression) or Gini impurity minimization (classification). Highly interpretable but susceptible to variance.", "• ")
    add_bullet(doc, "Random Forest Regressor / Classifier: An ensemble bagging algorithm constructing 100 decorrelated decision trees trained on bootstrap samples with random feature sub-spacing. Combines high non-linear expressive power with robust resistance to overfitting.", "• ")
    add_bullet(doc, "Logistic Regression: A generalized linear classification model mapping linear combinations of features through the sigmoid/softmax activation function to output calibrated class probabilities.", "• ")

    add_h2(doc, "2.8 Model Evaluation Framework")
    add_p(
        doc,
        "Evaluating model performance requires metrics tailored to the respective learning tasks:"
    )
    add_bullet(doc, "Mean Absolute Error (MAE): Quantifies the average magnitude of prediction errors in the original units (points): MAE = (1/N) Σ |y_i - ŷ_i|.", "Regression Metrics: ")
    add_bullet(doc, "Root Mean Squared Error (RMSE): Measures the square root of the average squared residuals, heavily penalizing large outlying prediction errors: RMSE = √[(1/N) Σ (y_i - ŷ_i)²].", "Regression Metrics: ")
    add_bullet(doc, "Coefficient of Determination (R²): Measures the proportion of variance in the academic score explained by the model: R² = 1 - [Σ(y_i - ŷ_i)² / Σ(y_i - ȳ)²]. An R² of 1.0 indicates perfect prediction.", "Regression Metrics: ")
    add_bullet(doc, "Accuracy, Precision, Recall, and F1-Score: For multi-class classification, weighted precision (TP / [TP+FP]) and weighted recall (TP / [TP+FN]) are harmonized into the F1-Score: F1 = 2 × (Precision × Recall) / (Precision + Recall).", "Classification Metrics: ")
    add_bullet(doc, "Confusion Matrix: A 3×3 contingency table tracking true class labels versus predicted class labels, directly exposing false positive and false negative misclassification rates across risk tiers.", "Diagnostic Artifacts: ")

    add_h2(doc, "2.9 Responsible AI Methodology")
    add_p(
        doc,
        "A cornerstone of the Microsoft AI-901 philosophy is that artificial intelligence systems must be engineered around ethical guardrails. In educational domains, "
        "algorithmic mistakes can adversely influence student academic self-esteem, financial aid, or graduation trajectories. The system operationalizes the Six Microsoft Responsible AI Principles:"
    )
    add_bullet(doc, "Fairness: Ensuring algorithms do not exhibit disparate impact or systematic bias across gender, socio-economic proxy attributes, or grade cohorts.", "1. ")
    add_bullet(doc, "Reliability & Safety: Enforcing input boundaries, validating CSV uploads, and guaranteeing bounded error tolerances (MAE ±2.7 points).", "2. ")
    add_bullet(doc, "Privacy & Security: Eliminating personally identifiable contact details and residential data from the modeling feature store.", "3. ")
    add_bullet(doc, "Inclusiveness: Designing multi-modal action plans accommodating diverse student learning curves, from remedial drills to honors enrichment.", "4. ")
    add_bullet(doc, "Transparency: Providing clear mathematical explanations, Gini feature importance charts, and individual feature impact breakdowns for every inference.", "5. ")
    add_bullet(doc, "Accountability: Maintaining a strict Human-in-the-Loop governance policy, explicitly stating that AI outputs represent consultative alerts for educators, never terminal judgments.", "6. ")

    # ----------------------------------------------------
    # CHAPTER 3 - SYSTEM DESIGN & IMPLEMENTATION (PAGES 15 TO 18 -> EXACTLY 4 PAGES)
    # ----------------------------------------------------
    doc.add_page_break()
    add_h1(doc, "CHAPTER 3: SYSTEM DESIGN AND IMPLEMENTATION")

    add_h2(doc, "3.1 System Overview & Architecture")
    add_p(
        doc,
        "The AI Student Performance Analytics and Prediction System is structured as an integrated, multi-tier full-stack application built upon Python and Streamlit. "
        "The architecture unifies dataset ingestion, automated data validation, supervised machine learning pipelines, prescriptive decision logic, and high-performance "
        "interactive visualizations within a single responsive web interface. The system is designed for dual deployment: executing locally for high-speed offline campus "
        "use and deploying as a cloud web service via Render with dynamic port binding."
    )
    add_p(
        doc,
        "[CSV Input / Cohort Data] ➔ [Data Loader & Schema Validator] ➔ [Scikit-learn Pipeline (Impute + Scale + OHE)]\n"
        "                                           ↓\n"
        "[Linear Regressor (R²=0.904)] ⟵ [Trained Model Weights] ⟶ [Random Forest Classifier (Acc=93.0%)]\n"
        "           ↓                                                              ↓\n"
        "[Continuous Score Forecast]                                   [Risk Tier Classification]\n"
        "           ↓                                                              ↓\n"
        "[Feature Attribution Engine] ➔ [Prescriptive Recommendation Engine] ➔ [Streamlit Interactive Web UI]",
        italic=True, space_after=6
    )
    add_caption(doc, "Figure 3.1: Logical Component Architecture and Data Pipeline")

    add_h2(doc, "3.2 Hardware and Software Requirements")
    add_p(
        doc,
        "The system was engineered for lightweight computational efficiency, avoiding heavy deep-learning dependencies to ensure universal compatibility across standard university lab workstations and cloud containers. "
        "Minimum hardware specifications require a dual-core 2.0 GHz CPU with 4 GB RAM and 500 MB storage. The development environment utilized a 6-core 3.2 GHz processor with 16 GB RAM. "
        "The software technology stack comprises Python 3.11+, Streamlit 1.40+, Pandas 2.0+, NumPy 1.24+, Scikit-learn 1.3+, Plotly 5.18+, Joblib 1.3+, and Git/GitHub."
    )

    add_h2(doc, "3.3 Dataset Description and Feature Engineering")
    add_p(
        doc,
        "The system operates upon a structured benchmark dataset comprising 1,000 student records across 20 distinct attributes spanning academic history, "
        "behavioral study patterns, continuous assessment milestones, and demographic variables. In accordance with strict academic integrity rules, this dataset is explicitly "
        "identified as a statistically coherent synthetic benchmark generated using fixed random seeds (NumPy random state 42) to ensure perfect scientific reproducibility."
    )

    ds_summary_headers = ["Attribute Identifier", "Data Type", "Value Range / Categories", "Role in Analysis & Prediction"]
    ds_summary_data = [
        ["student_id", "Categorical / String", "STU-1001 to STU-2000", "Unique student key for dossier search"],
        ["study_hours_per_day", "Continuous (Float)", "1.0 to 9.5 hours/day", "Primary behavioral predictor of academic mastery"],
        ["attendance_rate", "Continuous (Float)", "45.0% to 99.5%", "Lecture continuity and institutional engagement indicator"],
        ["previous_exam_score", "Continuous (Float)", "35.0% to 98.0%", "Historical academic baseline indicator"],
        ["assignment_completion_rate", "Continuous (Float)", "35.0% to 100.0%", "Continuous assessment and task diligence metric"],
        ["math / sci / eng / cs_score", "Continuous (Float)", "30.0 to 100.0", "Subject-level diagnostic scores across core curriculum"],
        ["subjects_needing_improvement", "Discrete (Integer)", "0 to 4 subjects", "Count of subjects scoring below 60/100 threshold"],
        ["final_score", "Continuous (Float)", "32.0 to 99.2", "Continuous Regression Target Variable"],
        ["risk_level", "Categorical (String)", "Low, Moderate, High", "Multi-Class Classification Target Variable"]
    ]
    create_table(doc, ds_summary_headers, ds_summary_data, [Inches(1.8), Inches(1.3), Inches(1.6), Inches(1.8)])
    add_caption(doc, "Table 3.1: Core Attribute Dictionary and Modeling Roles")

    add_h2(doc, "3.4 Preprocessing and Model Development")
    add_p(
        doc,
        "The data preprocessing pipeline is implemented in src/ml_pipeline.py utilizing Scikit-learn's ColumnTransformer and Pipeline constructs. "
        "Numerical features pass through a numerical sub-pipeline comprising SimpleImputer(strategy='median') and StandardScaler(). "
        "Categorical features pass through SimpleImputer(strategy='most_frequent') and OneHotEncoder(handle_unknown='ignore', sparse_output=False). "
        "Following preprocessing, the training dataset (N = 800) trains four regression algorithms and three classification algorithms. Optimal estimators are "
        "identified via holdout evaluation metrics: Linear Regression is selected as the production score regressor (R² = 0.9043, MAE = 2.719 points), and Random Forest "
        "Classifier is selected as the production risk classifier (Accuracy = 93.00%, F1 = 0.9305). All fitted artifacts—preprocessor.joblib, best_score_regressor.joblib, "
        "best_risk_classifier.joblib, and model_metrics.json—are serialized into the models/ directory for instant sub-second serving."
    )

    add_h2(doc, "3.5 Prediction, Risk Analysis & Recommendation Engine")
    add_p(
        doc,
        "The prediction engine provides real-time scoring for both cohort records and custom user input queries. When a user submits an academic profile via Page 2, "
        "the input dictionary is assembled into a single-row DataFrame, passed through the preprocessor pipeline, and scored simultaneously by the regression and "
        "classification estimators. To make predictions fully explainable, the module calculates local feature contributions against cohort benchmarks, outputting a "
        "horizontal waterfall chart displaying the positive and negative points attributed to each feature (e.g., +4.2 points from high attendance, -3.8 points from low study hours)."
    )
    add_p(
        doc,
        "The recommendation subsystem (src/recommender.py) converts analytical diagnostics into structured, multi-tiered action plans categorized into: "
        "(1) Urgent Attendance Recovery (protocols for lifting attendance above 75%), (2) Focused Study Expansion (time management and Pomodoro routines), "
        "(3) Subject Remediation (targeted problem sets for subjects with scores < 60), (4) Assignment Catch-Up (submission schedules), and (5) Cognitive Wellness (sleep hygiene). "
        "Each directive is tagged with priority levels (High Priority, Medium Priority, Low Priority) and an estimated potential score gain (+5 to +18 points)."
    )

    add_h2(doc, "3.6 Dashboard Design, CSV Ingestion, and Workflow")
    add_p(
        doc,
        "The user experience is engineered around a modern dark-navy / charcoal theme (Hex: #0B0F19, #111827, #1E293B) styled with custom CSS glassmorphism, glowing card borders, "
        "and Plotly interactive vector charts. The interface avoids generic default Streamlit layouts, providing a clean sidebar navigation system with status badges and system health telemetry. "
        "Page 8 (Dataset Management) provides dynamic ETL functionality. Users can upload custom institutional CSV files, which pass through schema validation "
        "verifying the presence of all required numerical columns. Upon successful validation, missing values are imputed, and the user can either apply the new dataset across all dashboard views "
        "or trigger dynamic on-demand model retraining. The operational workflow progresses seamlessly from cohort overview to student exploration, live scenario simulation, and action plan export."
    )

    # ----------------------------------------------------
    # CHAPTER 4 - SIX-WEEK WEEKLY REPORT (PAGES 19 TO 21 -> EXACTLY 3 PAGES, 2 WEEKS/PAGE)
    # ----------------------------------------------------
    doc.add_page_break()
    add_h1(doc, "CHAPTER 4: SIX-WEEK INTERNSHIP WEEKLY REPORT")
    add_p(
        doc,
        "This chapter documents the systematic technical work, developmental milestones, and progressive learning outcomes achieved during the six-week "
        "industrial internship period. The report strictly adheres to Appendix 5 of the Chandigarh University Industrial Internship Report format. "
        "Each week details the specific topic covered, daily task breakdowns (Day 1 through Day 5), key learning outcomes, and weekly work summaries. "
        "In accordance with official instructions, dates are presented with editable academic placeholders."
    )

    # PAGE 19: WEEKS 1 & 2
    w1_days = [
        "Studied core Artificial Intelligence fundamentals, historical paradigms, definition of intelligence, and industrial applications.",
        "Explored AI workloads defined in Microsoft AI-901: Machine Learning, Computer Vision, NLP, and Generative AI concepts.",
        "Researched educational AI applications, learning analytics, student drop-out prevention, and early-warning intervention systems.",
        "Formulated the student performance analytics problem statement, established analytical objectives, and outlined requirements.",
        "Defined the six-week project roadmap, technology stack specifications (Python, Scikit-learn, Streamlit), and architectural workflow."
    ]
    add_appendix5_week(
        doc, 1, "[START DATE] – [END DATE]", "AI Fundamentals and Project Planning",
        w1_days,
        "Acquired thorough understanding of the AI-901 workload taxonomy and formulated a feasible engineering project scope.",
        "Completed requirement gathering, literature survey on educational data mining, and finalized project technical specifications."
    )

    w2_days = [
        "Reviewed core Python data science libraries: Pandas dataframes, NumPy array manipulations, vector operations, and indexing.",
        "Implemented data exploration scripts using Pandas to compute central tendency, variance, interquartile ranges, and null counts.",
        "Conducted Exploratory Data Analysis (EDA) on student performance features; generated scatter plots, box plots, and histograms.",
        "Analyzed statistical correlations between academic indicators (study hours, attendance rate) and final performance outcomes.",
        "Constructed a statistically consistent benchmark student performance dataset (1,000 records, 20 attributes) with fixed random seed (42)."
    ]
    add_appendix5_week(
        doc, 2, "[START DATE] – [END DATE]", "Machine Learning and Data Analysis",
        w2_days,
        "Mastered tabular data manipulation in Pandas, learned correlation analysis, and engineered a reproducible benchmark dataset.",
        "Finalized the 20-feature dataset schema, verified statistical distributions, and saved canonical dataset to data/student_performance_data.csv."
    )

    # PAGE 20: WEEKS 3 & 4
    w3_days = [
        "Investigated data quality issues in educational records: missing values, measurement errors, out-of-range inputs, and outliers.",
        "Designed and implemented automated median imputation for numerical attributes and mode imputation for categorical attributes.",
        "Implemented categorical encoding strategies: explored label encoding versus one-hot encoding; configured Scikit-learn OneHotEncoder.",
        "Applied StandardScaler to continuous academic indicators; investigated data leakage risks and encapsulated scaling within Pipeline.",
        "Constructed the complete preprocessing ColumnTransformer; executed 80/20 stratified train/test split along student risk tiers."
    ]
    add_appendix5_week(
        doc, 3, "[START DATE] – [END DATE]", "Data Preprocessing and Feature Pipeline Engineering",
        w3_days,
        "Gained deep competency in building robust Scikit-learn Pipeline and ColumnTransformer architectures while preventing data leakage.",
        "Engineered the complete data preprocessing module (src/ml_pipeline.py) and verified zero data leakage between train and test splits."
    )

    w4_days = [
        "Implemented baseline regression and classification models: Ordinary Least Squares Linear Regression and Logistic Regression.",
        "Implemented decision tree estimators (DecisionTreeRegressor and DecisionTreeClassifier); analyzed tree depth and overfitting.",
        "Implemented ensemble models (RandomForestRegressor and RandomForestClassifier) with 100 estimators; evaluated bagging.",
        "Conducted formal holdout test evaluations using regression metrics (MAE, MSE, RMSE, R²) and classification metrics (Accuracy, F1).",
        "Selected optimal estimators (Linear Regression for score prediction, Random Forest for risk classification); serialized models via Joblib."
    ]
    add_appendix5_week(
        doc, 4, "[START DATE] – [END DATE]", "Machine Learning Model Development and Tuning",
        w4_days,
        "Developed deep understanding of bias-variance tradeoffs, evaluation metrics, confusion matrix analysis, and model serialization.",
        "Achieved out-of-sample R² of 0.9043 on regression and 93.00% accuracy on classification; saved serialized model artifacts to models/ directory."
    )

    # PAGE 21: WEEKS 5 & 6
    w5_days = [
        "Studied Streamlit web application framework: reactive execution models, session state management, caching, and layouts.",
        "Developed custom dark-navy CSS glassmorphism styling, KPI metric cards, and responsive sidebar navigation in src/ui_components.py.",
        "Constructed interactive Plotly vector charts: score distribution histograms, attendance vs score scatter plots, and subject comparison bars.",
        "Integrated the machine learning inference module into Page 2 (AI Student Prediction), adding one-click preset buttons and feature impact charts.",
        "Built the At-Risk Student Intelligence registry (Page 4) and developed the Prescriptive AI Recommendation Engine (Page 6)."
    ]
    add_appendix5_week(
        doc, 5, "[START DATE] – [END DATE]", "Analytics Dashboard and Application Development",
        w5_days,
        "Mastered rapid full-stack Python application engineering using Streamlit, dynamic Plotly charting, and prescriptive heuristic algorithm design.",
        "Completed all 9 core dashboard views, verified seamless cross-page session state navigation, and integrated live ML inference."
    )

    w6_days = [
        "Constructed an automated unit and integration test suite (tests/test_pipeline_and_app.py); verified dataset, loaders, pipeline, and views.",
        "Audited model error bounds, analyzed residual errors, inspected confusion matrices, and confirmed out-of-sample stability.",
        "Operationalized the Six Microsoft Responsible AI Principles; authored institutional ethics disclaimers and human-in-the-loop guidelines.",
        "Created production deployment configuration files (render.yaml, start.sh, requirements.txt); verified port binding on 0.0.0.0.",
        "Compiled technical documentation, finalized GitHub repository structure, and authored the comprehensive industrial internship report."
    ]
    add_appendix5_week(
        doc, 6, "[START DATE] – [END DATE]", "System Testing, Model Evaluation, and Technical Documentation",
        w6_days,
        "Learned end-to-end software quality assurance methodologies, cloud deployment containerization protocols, and responsible AI documentation.",
        "Verified 100% passing test suite, successfully published code to GitHub, configured Render cloud deployment, and finalized project submission."
    )

    # ----------------------------------------------------
    # CHAPTER 5 - RESULTS, ANALYSIS & DISCUSSION (PAGES 22 TO 23 -> EXACTLY 2 PAGES)
    # ----------------------------------------------------
    doc.add_page_break()
    add_h1(doc, "CHAPTER 5: RESULTS, ANALYSIS AND DISCUSSION")

    add_h2(doc, "5.1 Overview of Experimental Results")
    add_p(
        doc,
        "The empirical results obtained from the implementation and evaluation of the AI Student Performance Analytics and Prediction System demonstrate "
        "high predictive accuracy, operational reliability, and robust analytical utility. All metrics presented in this chapter are derived from out-of-sample "
        "holdout test partitions (20% test split, N = 200) strictly segregated from the training dataset."
    )

    add_h2(doc, "5.2 Dashboard and Prediction Results")
    add_p(
        doc,
        "The executive dashboard successfully aggregates and displays cohort performance metrics in real time. Across the baseline 1,000 student cohort, "
        "the system identified a cohort mean composite score of 71.2% (±12.4 points), an average lecture attendance rate of 80.4%, and an institutional risk distribution "
        "comprising 318 Low-Risk students (31.8%), 292 Moderate-Risk students (29.2%), and 390 High-Risk students (39.0%). The live prediction module delivers calibrated dual-task inference: "
        "prospective student profiles are simultaneously scored for continuous marks (0-100) and triaged into discrete risk tiers with softmax class probabilities."
    )

    add_h2(doc, "5.3 Model Evaluation and Benchmark Verification")
    add_p(
        doc,
        "Table 5.1 and Table 5.2 present the genuine, verified evaluation metrics computed across all candidate algorithms evaluated in src/ml_pipeline.py."
    )

    reg_headers = ["Algorithm Candidate", "MAE (pts)", "MSE", "RMSE (pts)", "R² Score", "Selection Decision"]
    reg_data = [
        ["Linear Regression (OLS)", "2.719", "11.758", "3.429", "0.9043", "Selected Production Model"],
        ["Ridge Regression (α=1.0)", "2.721", "11.762", "3.430", "0.9042", "High Performing Candidate"],
        ["Random Forest Regressor", "2.854", "13.012", "3.607", "0.8941", "Non-Linear Alternative"],
        ["Decision Tree Regressor", "3.420", "18.940", "4.352", "0.8458", "Baseline Model"]
    ]
    create_table(doc, reg_headers, reg_data, [Inches(1.8), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.8), Inches(1.4)])
    add_caption(doc, "Table 5.1: Comparative Regression Benchmark Results (Test Split N=200)")

    clf_headers = ["Classification Candidate", "Accuracy", "Precision (Weighted)", "Recall (Weighted)", "F1-Score", "Selection Decision"]
    clf_data = [
        ["Random Forest Classifier", "93.00%", "0.9312", "0.9300", "0.9305", "Selected Production Classifier"],
        ["Logistic Regression", "90.50%", "0.9064", "0.9050", "0.9052", "High Performing Linear Model"],
        ["Decision Tree Classifier", "88.50%", "0.8870", "0.8850", "0.8856", "Baseline Model"]
    ]
    create_table(doc, clf_headers, clf_data, [Inches(1.8), Inches(0.9), Inches(1.1), Inches(1.1), Inches(0.9), Inches(1.4)])
    add_caption(doc, "Table 5.2: Comparative Classification Benchmark Results (Test Split N=200)")

    add_h2(doc, "5.4 Empirical Performance Findings and Risk Insights")
    add_p(
        doc,
        "Statistical analysis of the cohort dataset revealed compelling empirical findings regarding academic determinants:"
    )
    add_bullet(doc, "Attendance Threshold Premium: Students maintaining attendance rates ≥ 80% achieved a mean final score of 79.4%, whereas students with attendance < 65% achieved a mean final score of 61.0%, demonstrating an empirical attendance premium of +18.4 percentage points.", "Finding 1: ")
    add_bullet(doc, "Study Hour Thresholds: Students engaging in ≥ 5.0 hours/day of focused study achieved a mean score of 81.2%, compared to 62.8% for students studying < 3.0 hours/day, establishing a study premium of +18.4 points.", "Finding 2: ")
    add_bullet(doc, "Subject Vulnerability Hierarchy: Diagnostic marks revealed that Mathematics exhibited the highest vulnerability rate (28.4% of cohort scoring < 60/100), followed by Computer Science (24.1%), Science (21.8%), and English Language (14.2%).", "Finding 3: ")
    add_p(
        doc,
        "Analysis of the 390 flagged High-Risk students indicated that 81.3% exhibited critical attendance deficits (<65%), 68.2% demonstrated continuous assignment completion rates "
        "below 60%, and 54.1% experienced failing marks in two or more diagnostic subjects simultaneously. The minimal false-negative rate among High-Risk learners confirms the model's reliability as an early-warning safety trigger."
    )

    add_h2(doc, "5.5 System Limitations and Discussion")
    add_p(
        doc,
        "To maintain rigorous academic honesty, several key limitations of the current implementation must be acknowledged: "
        "(1) The primary dataset is synthetically generated; real institutional deployments require validation on multi-year longitudinal records; "
        "(2) The model evaluates single-semester snapshots, lacking recurrent time-series modeling to capture week-by-week attendance shifts; "
        "(3) Machine learning models cannot observe unrecorded qualitative life circumstances (illness, family emergencies). "
        "Crucially, coupling predictions with explainable feature attribution prevents algorithmic opacity, enabling educators to understand precisely why a student was flagged "
        "and facilitating compassionate, targeted pedagogical intervention."
    )

    # ----------------------------------------------------
    # CHAPTER 6 - CONCLUSIONS & RECOMMENDATIONS (PAGE 24 -> EXACTLY 1 PAGE)
    # ----------------------------------------------------
    doc.add_page_break()
    add_h1(doc, "CHAPTER 6: CONCLUSIONS AND RECOMMENDATIONS")

    add_h2(doc, "6.1 Summary of Work and Conclusions")
    add_p(
        doc,
        "This six-week industrial internship project successfully designed, implemented, tested, and documented a complete, enterprise-grade AI Student Performance Analytics "
        "and Prediction System. Aligned with the Microsoft AI-901: Azure AI Fundamentals curriculum, the project bridged theoretical machine learning concepts with a tangible, "
        "practical software artifact tailored to higher education. The system features an end-to-end Scikit-learn preprocessing pipeline, multi-model regression benchmarking "
        "(achieving an optimal R² of 0.9043 via Linear Regression), multi-class risk categorization (achieving 93.00% accuracy and 0.9305 F1-Score via Random Forest), "
        "local explainable AI feature attribution, and a prescriptive academic recommendation engine. "
        "The user experience was realized through an elegant 9-page Streamlit web dashboard supported by Plotly vector analytics, CSV dataset ingestion with dynamic validation, "
        "and automated test coverage. Crucially, the project demonstrates that responsible artificial intelligence principles—fairness, transparency, reliability, and human accountability—"
        "can be seamlessly woven into software architecture, ensuring that technology elevates human educator empathy rather than supplanting it."
    )

    add_h2(doc, "6.2 Practical Recommendations & Future Scope")
    add_p(
        doc,
        "Based on the empirical findings and development insights of this investigation, the following practical recommendations are tendered for academic administrators:"
    )
    add_bullet(doc, "Enforce Early-Semester Attendance Thresholds: Establish automated alerts at Week 3 if lecture attendance drops below 75%, as attendance deficits represent the single strongest leading indicator of ultimate failure.", "1. ")
    add_bullet(doc, "Integrate Continuous Formative Assessments: Maintain weekly low-stakes quizzes to identify localized subject misconceptions before midterm examinations.", "2. ")
    add_bullet(doc, "Mandate Human-in-the-Loop Review: Educational institutions must strictly prohibit automated disciplinary or grading actions based on predictive algorithms; all interventions must be conducted through empathetic 1-on-1 faculty mentoring.", "3. ")
    add_p(
        doc,
        "Future technical trajectories include incorporating longitudinal recurrent neural networks (LSTM) to model sequential student learning trajectories over multi-year degree programs, "
        "developing direct LMS API connectors (LTI standard) for live Canvas/Moodle integration, and integrating localized Generative AI agents to automatically draft customized revision study guides."
    )

    add_h2(doc, "6.3 Internship Technical and Professional Learning Outcomes")
    add_p(
        doc,
        "The completion of this six-week industrial internship yielded substantial technical, architectural, and professional competencies: "
        "(1) Mastery of the Supervised ML Lifecycle (data ingestion, feature scaling, metric benchmarking, and model persistence); "
        "(2) Production Web Engineering (Streamlit reactive programming, responsive CSS glassmorphism, session state telemetry, and cloud containerization); "
        "(3) Operationalization of Responsible AI (algorithmic fairness, educational data bias mitigation, and human-in-the-loop governance aligned with Microsoft AI-901); "
        "(4) Software Quality Assurance (automated test suites, Git version control, GitHub repository management, and Render hosting); and "
        "(5) Academic Technical Communication (publication-quality engineering documentation, technical reporting, and defense preparation for external viva evaluation)."
    )

    # ----------------------------------------------------
    # APPENDICES (PAGE 25 -> EXACTLY 1 PAGE)
    # ----------------------------------------------------
    doc.add_page_break()
    add_h1(doc, "APPENDICES")

    add_h2(doc, "Appendix A: Microsoft AI-901 Certification Course Syllabus")
    add_p(
        doc,
        "The Microsoft AI-901 (Azure AI Fundamentals) certification measures foundational knowledge across five primary knowledge domains: "
        "(1) AI Workloads and Considerations (prediction, vision, NLP, generative AI, responsible AI principles); "
        "(2) Fundamental Principles of Machine Learning on Azure (supervised regression, classification, unsupervised clustering, features, labels, evaluation metrics); "
        "(3) Computer Vision Workloads (image classification, object detection, OCR); "
        "(4) Natural Language Processing Workloads (sentiment analysis, entity recognition, speech synthesis); and "
        "(5) Generative AI Workloads (foundational LLMs, prompt engineering, generative multimodal capabilities, and guardrails)."
    )

    add_h2(doc, "Appendix B: Global Certification Certificate Placeholder")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("[INSERT OFFICIAL MICROSOFT AI-901 CERTIFICATION CERTIFICATE HERE]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RGBColor(180, 0, 0)
    add_caption(doc, "Figure B.1: Official Microsoft AI-901 Global Certification Certificate")

    add_h2(doc, "Appendix C: Official Certification Score Report Placeholder")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("[INSERT OFFICIAL AI-901 CERTIFICATION SCORE REPORT HERE]")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RGBColor(180, 0, 0)
    add_caption(doc, "Figure C.1: Official Microsoft Examination Score Transcript")

    add_h2(doc, "Appendix D: Application Screenshots & Verification Summary")
    add_p(
        doc,
        "The application encompasses 9 complete verified views: (1) Executive Dashboard (cohort KPIs, score distribution histograms, risk donut charts); "
        "(2) AI Student Prediction (dual-task score and risk inference with preset demonstration buttons); (3) Explainable AI Feature Attribution (waterfall score contribution charts); "
        "(4) Student Explorer (individual dossier with 7-axis radar charts vs 80% benchmark); (5) At-Risk Student Intelligence (prioritized early-warning registry and CSV export); "
        "(6) Academic Insights (10×10 Pearson correlation heatmap and study bracket bars); (7) Prescriptive AI Recommendation Engine (multi-tiered intervention action plans); "
        "(8) Model Insights & AI Lab (pipeline diagram, benchmark tables, and test confusion matrix); and (9) Dataset Management & Responsible AI Governance (CSV validation and ethics grid). "
        "All modules passed 100% automated test suite verification in tests/test_pipeline_and_app.py."
    )

    # ----------------------------------------------------
    # REFERENCES (PAGE 26 -> EXACTLY 1 PAGE)
    # ----------------------------------------------------
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run("REFERENCES")
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.font.bold = True

    references = [
        "Romero, C., & Ventura, S. (2010). Educational data mining: a review of the state of the art. IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews), 40(6), 601-618.",
        "Cortez, P., & Silva, A. M. G. (2008). Using data mining to predict secondary school student performance. In Proceedings of 5th Annual Future Business Technology Conference (FUBUTEC 2008), Porto, Portugal, pp. 5-12.",
        "Baker, R. S., & Inventado, P. S. (2014). Educational data mining and learning analytics. In Learning Analytics (pp. 61-75). Springer, New York, NY.",
        "Microsoft Learn. (2024). Microsoft Certified: Azure AI Fundamentals (Exam AI-901). Official Certification Curriculum and Study Guide. Available: https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/",
        "Microsoft Learn. (2024). Fundamental Principles of Machine Learning on Azure. Microsoft Technical Documentation. Available: https://learn.microsoft.com/en-us/azure/machine-learning/",
        "Microsoft Learn. (2024). Responsible AI Principles and Governance Approach. Microsoft Corporation. Available: https://www.microsoft.com/en-us/ai/responsible-ai",
        "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., & Vanderplas, J. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
        "McKinney, W. (2010). Data structures for statistical computing in Python. In Proceedings of the 9th Python in Science Conference (SciPy 2010), pp. 51-56.",
        "Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., & Kern, R. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.",
        "Plotly Technologies Inc. (2024). Collaborative Data Science and Interactive Visualization. Montreal, QC. Available: https://plotly.com/python/",
        "Streamlit Inc. (2024). The Fastest Way to Build and Share Data Apps. Snowflake Inc. Available: https://docs.streamlit.io/",
        "Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5-32.",
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction. 2nd Edition, Springer Science & Business Media.",
        "Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765-4774.",
        "Render Services Inc. (2024). Render Cloud Application Hosting Documentation and Architecture. Available: https://render.com/docs"
    ]

    for idx, ref in enumerate(references, 1):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4.5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        r_num = p.add_run(f"[{idx}] ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(10)
        r_num.font.bold = True
        
        r_text = p.add_run(ref)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(10)

    # Save calibrated document
    doc.save(DOCX_NAME)
    print(f"Generated calibrated document: {DOCX_NAME}")

if __name__ == "__main__":
    generate_report_26_pages()

