"""
Script to generate the comprehensive, professional Project Report & Study Guide PDF
for MemoryMirror AI (SparkX 3.0 International Innovation Challenge).
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Custom canvas that adds 'Page X of Y' and header/footer to all pages."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(
                54, 750, "SPARKX 3.0 | MemoryMirror AI: Project Guide & Team Task Division"
            )
            self.drawRightString(612 - 54, 750, "Gauri Dwivedi & Nuka Devashmitha Reddy")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        # Running footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 36, "MemoryMirror AI — Intelligent Continual Learning & Retention Monitoring")
        self.drawRightString(612 - 54, 36, page_str)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 612 - 54, 46)

        self.restoreState()


def build_pdf(filename="MemoryMirror_AI_Project_Report_and_Study_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0f172a")
    accent_blue = colors.HexColor("#0284c7")
    accent_purple = colors.HexColor("#7c3aed")
    dark_text = colors.HexColor("#1e293b")
    muted_text = colors.HexColor("#64748b")
    light_bg = colors.HexColor("#f8fafc")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=0,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        alignment=0,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=accent_purple,
        spaceBefore=10,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=dark_text,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4,
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=dark_text,
        alignment=0,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=dark_text,
        alignment=0,
    )

    callout_style = ParagraphStyle(
        "Callout",
        parent=body_style,
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
    )

    story = []

    # ---------------------------------------------------------
    # COVER / HEADER BLOCK
    # ---------------------------------------------------------
    story.append(Paragraph("SPARKX 3.0 | INTERNATIONAL PROJECT INNOVATION CHALLENGE", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("MEMORYMIRROR AI", title_style))
    story.append(Paragraph("An Intelligent Continual Learning & Memory Retention Monitoring System", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>“Teach AI Something New, Without Making It Forget the Old.”</i>", callout_style))
    story.append(Spacer(1, 8))

    meta_table_data = [
        [
            Paragraph("<b>Competition:</b> SPARKX 3.0 Challenge", table_cell_style),
            Paragraph("<b>Project Category:</b> Novel Product-Based Innovation", table_cell_style),
        ],
        [
            Paragraph("<b>Team Leader:</b> Gauri Dwivedi", table_cell_style),
            Paragraph("<b>Team Member:</b> Nuka Devashmitha Reddy", table_cell_style),
        ],
        [
            Paragraph("<b>Live Cloud URL:</b> <font color='#0284c7'>https://memory-mirror-ai.onrender.com</font>", table_cell_style),
            Paragraph("<b>GitHub Repo:</b> <font color='#0284c7'>devashmitha1308/memory-mirrorAI</font>", table_cell_style),
        ],
    ]
    meta_table = Table(meta_table_data, colWidths=[250, 254])
    meta_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # 1. EXECUTIVE SUMMARY & 60-SECOND PITCH
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & 60-Second Explanation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_blue, spaceAfter=8))
    
    pitch_text = (
        "<b>The Problem (Catastrophic Forgetting):</b> When standard machine learning models learn a new task, "
        "backpropagation updates their neural synapses to fit the new data. In doing so, it inadvertently overwrites "
        "the synaptic patterns that encoded earlier skills. For instance, an AI trained to recognize digits 0–4 with "
        "99% accuracy will suddenly collapse to 60% or lower once it is trained on digits 5–9.<br/><br/>"
        "<b>The Analogy (The Musician's Dilemma):</b> Imagine a pianist who learns to play the violin, but the moment "
        "she masters the violin, she completely forgets how to play the piano. That is catastrophic forgetting. "
        "<b>MemoryMirror AI</b> acts as a rehearsal coach and memory shield that allows the AI to acquire the violin "
        "while permanently retaining its mastery of the piano.<br/><br/>"
        "<b>The Solution:</b> MemoryMirror AI introduces a dual-engine architecture: (1) An active <b>audit loop</b> "
        "that tests all previous tasks every time the model learns anything new, and (2) An adaptive <b>Memory Preservation "
        "Module</b> featuring <i>Elastic Weight Consolidation (EWC)</i> to stiffen crucial synapses and an <i>Episodic Replay Buffer</i> "
        "to interleave exemplar memories."
    )
    story.append(Paragraph(pitch_text, body_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # 2. WHAT IS USED VS. WHAT IS NOT USED (SCOPE AUDIT)
    # ---------------------------------------------------------
    story.append(Paragraph("2. Scope Audit: What is Used vs. What is NOT Used", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_blue, spaceAfter=8))

    used_table_data = [
        [
            Paragraph("Dimension", table_header_style),
            Paragraph("What is USED & BUILT (In Working Model)", table_header_style),
            Paragraph("What is NOT USED (Out of Scope / Justified)", table_header_style),
        ],
        [
            Paragraph("<b>Core ML Engine</b>", table_cell_bold),
            Paragraph("• Vectorized Continual Neural Network (MLP) with exact Autograd.<br/>"
                      "• He initialization & Adam optimizer.<br/>"
                      "• Fisher Information Matrix (FIM) diagonal calculator.<br/>"
                      "• Synaptic weight drift & Frobenius norm tracker.", table_cell_style),
            Paragraph("• Heavy pre-trained LLMs (GPT/Llama) requiring multi-GPU clusters.<br/>"
                      "• Black-box API wrappers (everything is written from mathematical first principles).", table_cell_style),
        ],
        [
            Paragraph("<b>Memory Preservation</b>", table_cell_bold),
            Paragraph("• <b>Naive Fine-Tuning:</b> Baseline proving forgetting.<br/>"
                      "• <b>Elastic Weight Consolidation (EWC):</b> Quadratic loss penalty protecting high-curvature synapses.<br/>"
                      "• <b>Experience Replay:</b> Reservoir buffer interleaving past prototypes.<br/>"
                      "• <b>Joint Multi-Task:</b> Theoretical upper bound.", table_cell_style),
            Paragraph("• Generative Replay via GANs/Diffusion (avoids heavy generative hallucination and excessive compute).<br/>"
                      "• Architecture Expansion / Progressive Neural Networks (avoids unbounded parameter explosion).", table_cell_style),
        ],
        [
            Paragraph("<b>Datasets & Benchmarks</b>", table_cell_bold),
            Paragraph("• <b>Split MNIST (2 Tasks):</b> Digits 0–4 vs. 5–9.<br/>"
                      "• <b>5-Task Incremental Digits:</b> 2 digits per task.<br/>"
                      "• <b>Sensory Shift:</b> Inverted polarity & noise shifts.<br/>"
                      "• <b>Synthetic Manifold Drift:</b> Continuous domain shift.", table_cell_style),
            Paragraph("• Full ImageNet (1.2M high-res images, which would cause slow latency during live demo presentations).<br/>"
                      "• Medical/Robotics proprietary sets (focus is on general-purpose continual validation).", table_cell_style),
        ],
        [
            Paragraph("<b>Evaluation & Metrics</b>", table_cell_bold),
            Paragraph("• Complete $R_{i,j}$ Cross-Task Accuracy Matrix.<br/>"
                      "• Task-wise Forgetting Score ($f_j^k$).<br/>"
                      "• Backward Transfer (BWT) & Forward Transfer.<br/>"
                      "• Automated Catastrophic Forgetting Severity Alerts.", table_cell_style),
            Paragraph("• Static single-epoch accuracy snapshots (continual learning requires full evolutionary matrices).", table_cell_style),
        ],
        [
            Paragraph("<b>Dashboard & Cloud</b>", table_cell_bold),
            Paragraph("• <b>Streamlit:</b> Dark-themed, responsive web UI.<br/>"
                      "• <b>Plotly:</b> Dynamic timelines, heatmaps, radars.<br/>"
                      "• <b>Render:</b> 24/7 cloud deployment via <code>render.yaml</code>.<br/>"
                      "• <b>JSON/CSV:</b> Full experiment data export.", table_cell_style),
            Paragraph("• Static PowerPoint slide decks for live demonstration (replaced by real interactive web dashboard).", table_cell_style),
        ],
    ]

    used_table = Table(used_table_data, colWidths=[90, 210, 204])
    used_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary_color),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(used_table)
    story.append(Spacer(1, 14))

    story.append(PageBreak())

    # ---------------------------------------------------------
    # 3. TASK DIVISION: GAURI VS. DEVASHMITHA
    # ---------------------------------------------------------
    story.append(Paragraph("3. Team Division of Tasks & Ownership", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_blue, spaceAfter=8))
    story.append(Paragraph(
        "To ensure a seamless, high-impact defense in front of the competition jury, the project "
        "responsibilities and presentation ownership are divided into two distinct, complementary tracks:",
        body_style,
    ))
    story.append(Spacer(1, 6))

    roles_table_data = [
        [
            Paragraph("Team Member", table_header_style),
            Paragraph("Project Role & Primary Modules", table_header_style),
            Paragraph("Core Technical Responsibilities", table_header_style),
        ],
        [
            Paragraph("<b>GAURI DWIVEDI</b><br/><i>Team Leader</i>", table_cell_bold),
            Paragraph("<b>Theoretical Foundation, EWC & Analytical Advisor</b><br/>"
                      "• Theoretical Continual Learning Formulation<br/>"
                      "• Elastic Weight Consolidation (EWC)<br/>"
                      "• Fisher Information Matrix Algorithm<br/>"
                      "• Forgetting Detection Engine & Alerts<br/>"
                      "• Analytical AI Recommendations Engine", table_cell_style),
            Paragraph("1. Formulated the loss regularizer $\\mathcal{L}(\\theta)$ with quadratic parameter stiffness.<br/>"
                      "2. Derived and coded diagonal Fisher curvature approximation.<br/>"
                      "3. Designed the Catastrophic Forgetting Alert thresholds (>15% warning, >25% critical).<br/>"
                      "4. Built the Continual Learning Health Index algorithm (0–100 score & A+ to F grading).<br/>"
                      "5. Handles the presentation opening, theoretical defense, and future research vision.", table_cell_style),
        ],
        [
            Paragraph("<b>NUKA DEVASHMITHA REDDY</b><br/><i>Team Member</i>", table_cell_bold),
            Paragraph("<b>System Engineering, Replay Buffer & Deployment</b><br/>"
                      "• Sequential Data Streaming & Task Manager<br/>"
                      "• Vectorized Neural Network Architecture<br/>"
                      "• Experience Replay (Memory Mirror Buffer)<br/>"
                      "• Streamlit Interactive Web Application<br/>"
                      "• Render Cloud Deployment & CI/CD", table_cell_style),
            Paragraph("1. Engineered the Dataset Manager for Split MNIST (0–4 vs 5–9) and 5-Task benchmarks.<br/>"
                      "2. Built the forward/backprop matrix operations and Adam optimization engine.<br/>"
                      "3. Implemented the balanced prototype rehearsal buffer for Experience Replay.<br/>"
                      "4. Designed all Plotly interactive charts (Timeline, Heatmap, Radar, Waterfall).<br/>"
                      "5. Led GitHub repository setup, Render cloud configuration (<code>render.yaml</code>), and live cloud hosting.", table_cell_style),
        ],
    ]

    roles_table = Table(roles_table_data, colWidths=[110, 190, 204])
    roles_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary_color),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(roles_table)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # 4. STEP-BY-STEP PRESENTATION SCRIPT
    # ---------------------------------------------------------
    story.append(Paragraph("4. Presentation Script & Speaking Flow (How to Present)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_blue, spaceAfter=8))

    script_intro = (
        "<b>Total Time:</b> 5–7 Minutes | <b>Format:</b> Tag-team presentation with live web demo."
    )
    story.append(Paragraph(script_intro, body_style))
    story.append(Spacer(1, 4))

    # Gauri Part 1
    story.append(Paragraph("PART 1: The Problem & The Innovation (Speaker: Gauri Dwivedi — ~2 mins)", h2_style))
    gauri_script = (
        "• <i>Opening:</i> 'Respected judges, imagine teaching an AI to diagnose pneumonia from X-rays. "
        "Next month, you teach it to detect COVID-19. Suddenly, it completely forgets how to detect pneumonia! "
        "This critical flaw is called <b>Catastrophic Forgetting</b>.'<br/>"
        "• <i>The Spark:</i> 'Today, Devashmitha and I present <b>MemoryMirror AI</b>: an intelligent continual learning "
        "and memory retention monitoring system whose motto is <i>Teach AI something new, without making it forget the old</i>.'<br/>"
        "• <i>The Innovation:</i> 'Unlike traditional systems that evaluate an AI once at the end, MemoryMirror AI operates on a "
        "vital principle: <b>Every time the model learns something new, we go back and audit everything it learned before.</b> "
        "We formulated an active forgetting metric and integrated Elastic Weight Consolidation (EWC) to shield the neural network\\'s "
        "most critical synapses using Fisher Information curvature.'<br/>"
        "• <i>Hand-off:</i> 'I will now invite my teammate Devashmitha to demonstrate our live working model in action.'"
    )
    story.append(Paragraph(gauri_script, body_style))
    story.append(Spacer(1, 6))

    # Devashmitha Part 2
    story.append(Paragraph("PART 2: Architecture & Live Cloud Demo (Speaker: Devashmitha Reddy — ~2.5 mins)", h2_style))
    deva_script = (
        "• <i>Live Demo Opening:</i> 'Thank you, Gauri. As you can see on screen at <b>memory-mirror-ai.onrender.com</b>, "
        "our full product is live 24/7 in the cloud.'<br/>"
        "• <i>Demonstrating Catastrophic Forgetting (Naive):</i> 'In our first experiment, we train on Task A (Digits 0 to 4). "
        "It achieves 100% accuracy. Next, we stream Task B (Digits 5 to 9). Watch the timeline: the moment Task B is learned, "
        "Task A accuracy plummets by 15 to 35 points! Our Forgetting Detection Engine immediately flags a <b>CRITICAL ALERT</b>.'<br/>"
        "• <i>Activating Memory Preservation:</i> 'Now, we switch to our preservation algorithms: <b>Experience Replay</b> and "
        "<b>Elastic Weight Consolidation</b>. With EWC stiffness λ=1000, Task A retains 95.1% accuracy—a 10-point retention boost! "
        "And in the Replay tab, you can inspect the actual prototype images cached in the memory buffer.'<br/>"
        "• <i>Multi-Strategy Benchmark:</i> 'Our head-to-head tab compares Naive vs. Replay vs. EWC against the theoretical "
        "Joint Multi-Task oracle across an interactive radar chart and full accuracy matrix R.'"
    )
    story.append(Paragraph(deva_script, body_style))
    story.append(Spacer(1, 6))

    # Gauri Part 3
    story.append(Paragraph("PART 3: AI Advisor & Real-World Impact (Speaker: Gauri Dwivedi — ~1.5 mins)", h2_style))
    gauri_closing = (
        "• <i>Advisor & Health Score:</i> 'MemoryMirror AI doesn't just measure forgetting; it tells you how to fix it. "
        "Our Analytical AI Advisor computes a <b>Continual Health Index</b> and analyzes the Plasticity-Stability trade-off, "
        "recommending optimal hyperparameter tuning for production models.'<br/>"
        "• <i>Impact & Applications:</i> 'From autonomous driving systems that encounter new cities, to medical diagnostic models "
        "updating with new disease strains, MemoryMirror AI guarantees AI models evolve without losing their past. "
        "Thank you, and we welcome your questions!'"
    )
    story.append(Paragraph(gauri_closing, body_style))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # ---------------------------------------------------------
    # 5. CORE MATHEMATICAL FORMULATIONS EXPLAINED SIMPLY
    # ---------------------------------------------------------
    story.append(Paragraph("5. Mathematical Foundation (Explained in Plain English)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_blue, spaceAfter=8))

    math_table_data = [
        [
            Paragraph("Metric / Concept", table_header_style),
            Paragraph("Mathematical Formula", table_header_style),
            Paragraph("Plain English Meaning (What to Tell Judges)", table_header_style),
        ],
        [
            Paragraph("<b>Forgetting Score ($f_j^k$)</b>", table_cell_bold),
            Paragraph("$$f_j^k = \\max_{l < k} R_{l,j} - R_{k,j}$$", table_cell_style),
            Paragraph("<b>Peak Past Score minus Score Now:</b> How many percentage points of accuracy Task $j$ lost since its peak, after learning up to stage $k$.", table_cell_style),
        ],
        [
            Paragraph("<b>Average Accuracy ($A_k$)</b>", table_cell_bold),
            Paragraph("$$A_k = \\frac{1}{k} \\sum_{j=1}^k R_{k,j}$$", table_cell_style),
            Paragraph("<b>Overall Score Across Seen Tasks:</b> The mean performance across all $k$ tasks trained so far.", table_cell_style),
        ],
        [
            Paragraph("<b>Backward Transfer (BWT)</b>", table_cell_bold),
            Paragraph("$$\\text{BWT} = \\frac{1}{T-1} \\sum_{j=1}^{T-1} (R_{T,j} - R_{j,j})$$", table_cell_style),
            Paragraph("<b>Impact of New Learning on the Past:</b><br/>• Negative BWT = Catastrophic forgetting.<br/>• Zero BWT = Perfect memory.<br/>• Positive BWT = Learning new tasks made old tasks even better!", table_cell_style),
        ],
        [
            Paragraph("<b>EWC Loss Regularizer</b>", table_cell_bold),
            Paragraph("$$\\mathcal{L}(\\theta) = \\mathcal{L}_{\\text{new}} + \\sum_i \\frac{\\lambda}{2} F_i (\\theta_i - \\theta_i^*)^2$$", table_cell_style),
            Paragraph("<b>Spring Stiffness on Brain Synapses:</b> Penalizes changing weights that have a high Fisher information score $F_i$. Important synapses act like stiff steel springs; unimportant synapses remain soft and flexible to learn new tasks.", table_cell_style),
        ],
        [
            Paragraph("<b>Fisher Information ($F_i$)</b>", table_cell_bold),
            Paragraph("$$F_i = \\mathbb{E}\\left[\\left(\\frac{\\partial \\log p(y|x, \\theta)}{\\partial \\theta_i}\\right)^2\\right]$$", table_cell_style),
            Paragraph("<b>Synaptic Sensitivity:</b> Measures how sensitive the model's past task predictions are to small perturbations in parameter $\\theta_i$.", table_cell_style),
        ],
    ]

    math_table = Table(math_table_data, colWidths=[100, 180, 224])
    math_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), primary_color),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.append(math_table)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # 6. JUDGE Q&A DEFENSE GUIDE (WINNING ANSWERS)
    # ---------------------------------------------------------
    story.append(Paragraph("6. Judge Q&A Defense Guide: Top Questions & Winning Answers", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_blue, spaceAfter=8))

    qa_list = [
        (
            "Q1 (To Gauri): 'Why not just retrain the entire model from scratch every time new data arrives?'",
            "<b>Answer:</b> 'Retraining from scratch is computationally prohibitive and practically impossible in real-world streaming applications. If an autonomous vehicle or medical system receives 10 GB of new sensor data daily, retraining on petabytes of historical data every night would cost millions in compute and cause unacceptable latency. MemoryMirror AI allows models to learn incrementally on-the-fly in seconds while mathematically guaranteeing past memory preservation.'"
        ),
        (
            "Q2 (To Devashmitha): 'Doesn\\'t Experience Replay violate data privacy or require huge storage?'",
            "<b>Answer:</b> 'Excellent question. That is why our Dataset Manager uses a bounded reservoir buffer that retains only tiny representative exemplar prototypes (e.g. 50 samples per task), rather than storing raw datasets. Furthermore, if strict privacy laws (like HIPAA or GDPR) forbid storing raw exemplars, our system seamlessly switches to Elastic Weight Consolidation (EWC), which stores zero raw data and relies entirely on synaptic weight stiffness.'"
        ),
        (
            "Q3 (To Gauri): 'What is the Plasticity-Stability dilemma, and how does your AI Advisor solve it?'",
            "<b>Answer:</b> 'If an AI is too plastic, it learns new things instantly but forgets everything old. If it is too stable, its weights are frozen and it refuses to absorb new skills. Our AI Advisor dynamically balances this by tracking Backward Transfer and layer parameter drift. If new task accuracy drops below 75%, it recommends reducing EWC λ; if past tasks slip by >15%, it automatically recommends increasing λ stiffness.'"
        ),
        (
            "Q4 (To Devashmitha): 'How is this deployed in production, and can anyone access it right now?'",
            "<b>Answer:</b> 'Yes! The entire pipeline is containerized and hosted live 24/7 on Render at <b>memory-mirror-ai.onrender.com</b>. We implemented automated CI/CD directly linked to our GitHub repository. Any continual learning experiment can be configured in the sidebar, executed in real-time, and exported as standardized JSON or CSV reports for audit compliance.'"
        ),
    ]

    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 4))

    # Build PDF with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated successfully at: {os.path.abspath(filename)}")


if __name__ == "__main__":
    build_pdf()
