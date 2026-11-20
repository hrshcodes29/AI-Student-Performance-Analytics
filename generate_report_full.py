"""
Generate the complete official Chandigarh University Industrial Internship Report in Microsoft Word (.docx).
File name: Harsh_Chandel_Industrial_Internship_Report_AI_Student_Performance.docx
Candidate: Harsh Chandel (UID: 24BAI70240)
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

OUTPUT_FILENAME = "Harsh_Chandel_Industrial_Internship_Report_AI_Student_Performance.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
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
    r_left.font.size = Pt(9)
    r_left.font.color.rgb = RGBColor(120, 120, 120)
    
    r_page = p.add_run("Page ")
    r_page.font.name = "Times New Roman"
    r_page.font.size = Pt(9)
    r_page.font.color.rgb = RGBColor(120, 120, 120)
    
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p._p.append(fldSimple)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.style = doc.styles['Heading 1']
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.style = doc.styles['Heading 2']
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.style = doc.styles['Heading 3']
    return p

def add_body(doc, text, bold_prefix="", italic=False, space_after=6, line_spacing=1.5):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = italic
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.italic = True
    r.font.color.rgb = RGBColor(40, 40, 40)
    return p

def create_table(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        cell = hdr_cells[i]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            cell = row_cells[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(str(cell_value))
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(20, 20, 20)

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return table

def add_weekly_report_table(doc, week_no, dates_str, topic_covered, day_entries, outcomes, summary):
    """
    Renders an official Appendix 5 table for a single week.
    """
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_before = Pt(12)
    p_hdr.paragraph_format.space_after = Pt(4)
    r_hdr = p_hdr.add_run(f"WEEK {week_no} – {topic_covered.upper()}")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(13)
    r_hdr.font.bold = True

    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    # Col widths: Col 0 = 1.6 inches, Col 1 = 4.9 inches
    col_widths = [Inches(1.6), Inches(4.9)]

    # Header Row
    cell_w = table.rows[0].cells[0]
    cell_t = table.rows[0].cells[1]
    set_cell_background(cell_w, "1E293B")
    set_cell_background(cell_t, "1E293B")
    set_cell_margins(cell_w, 120, 120, 140, 140)
    set_cell_margins(cell_t, 120, 120, 140, 140)

    pw = cell_w.paragraphs[0]
    pw.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rw = pw.add_run(f"WEEK {week_no}\nDATES\n({dates_str})")
    rw.font.name = "Times New Roman"
    rw.font.size = Pt(10)
    rw.font.bold = True
    rw.font.color.rgb = RGBColor(255, 255, 255)

    pt = cell_t.paragraphs[0]
    pt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = pt.add_run(f"TOPIC COVERED:\n{topic_covered.upper()}")
    rt.font.name = "Times New Roman"
    rt.font.size = Pt(10)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(255, 255, 255)

    # Days 1 to 5
    for i in range(1, 6):
        cell_day = table.rows[i].cells[0]
        cell_desc = table.rows[i].cells[1]
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        set_cell_background(cell_day, bg)
        set_cell_background(cell_desc, bg)
        set_cell_margins(cell_day, 100, 100, 120, 120)
        set_cell_margins(cell_desc, 100, 100, 120, 120)

        p_d = cell_day.paragraphs[0]
        p_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rd = p_d.add_run(f"DAY-{i}\n[DATE]")
        rd.font.name = "Times New Roman"
        rd.font.size = Pt(9.5)
        rd.font.bold = True

        p_desc = cell_desc.paragraphs[0]
        p_desc.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_desc.paragraph_format.line_spacing = 1.15
        rdesc = p_desc.add_run(day_entries[i - 1])
        rdesc.font.name = "Times New Roman"
        rdesc.font.size = Pt(9.5)

    for row in table.rows:
        row.cells[0].width = col_widths[0]
        row.cells[1].width = col_widths[1]

    # Outcomes and Summary below table
    p_out = doc.add_paragraph()
    p_out.paragraph_format.space_before = Pt(6)
    p_out.paragraph_format.space_after = Pt(4)
    p_out.paragraph_format.line_spacing = 1.25
    r_ot = p_out.add_run("Key Learning Outcomes: ")
    r_ot.font.name = "Times New Roman"
    r_ot.font.size = Pt(11)
    r_ot.font.bold = True
    r_ot_txt = p_out.add_run(outcomes)
    r_ot_txt.font.name = "Times New Roman"
    r_ot_txt.font.size = Pt(11)

    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(2)
    p_sum.paragraph_format.space_after = Pt(12)
    p_sum.paragraph_format.line_spacing = 1.25
    r_st = p_sum.add_run("Weekly Work Summary: ")
    r_st.font.name = "Times New Roman"
    r_st.font.size = Pt(11)
    r_st.font.bold = True
    r_st_txt = p_sum.add_run(summary)
    r_st_txt.font.name = "Times New Roman"
    r_st_txt.font.size = Pt(11)

    return table

print("Setup completed.")
