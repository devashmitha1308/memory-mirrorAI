"""
Generates two distinct, dedicated PDFs for MemoryMirror AI (SparkX 3.0):
1. MemoryMirror_AI_Gauri_Dwivedi_Leader_Guide.pdf
2. MemoryMirror_AI_Devashmitha_Reddy_Member_Guide.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)
from reportlab.pdfgen import canvas


class GauriNumberedCanvas(canvas.Canvas):
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

        if self._pageNumber > 1:
            self.drawString(54, 750, "SPARKX 3.0 | MemoryMirror AI — Team Leader Guide")
            self.drawRightString(612 - 54, 750, "Gauri Dwivedi (Team Leader)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 36, "MemoryMirror AI — Theoretical Foundation, EWC & Analytical Advisor")
        self.drawRightString(612 - 54, 36, page_str)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 612 - 54, 46)
        self.restoreState()


class DevaNumberedCanvas(canvas.Canvas):
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

        if self._pageNumber > 1:
            self.drawString(54, 750, "SPARKX 3.0 | MemoryMirror AI — Technical Lead Guide")
            self.drawRightString(612 - 54, 750, "Nuka Devashmitha Reddy (Technical Lead)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 36, "MemoryMirror AI — System Architecture, Replay, Dashboard & Cloud")
        self.drawRightString(612 - 54, 36, page_str)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 612 - 54, 46)
        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()
    primary = colors.HexColor("#0f172a")
    blue = colors.HexColor("#0284c7")
    purple = colors.HexColor("#7c3aed")
    dark = colors.HexColor("#1e293b")

    return {
        "title": ParagraphStyle("DocTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=primary),
        "subtitle": ParagraphStyle("DocSub", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=blue),
        "h1": ParagraphStyle("H1", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=primary, spaceBefore=12, spaceAfter=5),
        "h2": ParagraphStyle("H2", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=purple, spaceBefore=8, spaceAfter=3),
        "body": ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=13, textColor=dark, spaceAfter=5),
        "script": ParagraphStyle("Script", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=9, leading=13.5, textColor=colors.HexColor("#0f172a"), spaceAfter=5),
        "th": ParagraphStyle("TH", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white),
        "td": ParagraphStyle("TD", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=11, textColor=dark),
        "td_bold": ParagraphStyle("TDBold", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=dark),
    }


# =============================================================================
# BUILD GAURI DWIVEDI'S PDF (TEAM LEADER)
# =============================================================================
def build_gauri_pdf(filename="MemoryMirror_AI_Gauri_Dwivedi_Leader_Guide.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    st = get_styles()
    story = []

    # Header Card
    story.append(Paragraph("SPARKX 3.0 INTERNATIONAL INNOVATION CHALLENGE", st["subtitle"]))
    story.append(Spacer(1, 3))
    story.append(Paragraph("MEMORYMIRROR AI — TEAM LEADER GUIDE", st["title"]))
    story.append(Paragraph("Prepared Exclusively for: <b>GAURI DWIVEDI</b> (Team Leader)", st["subtitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>“Teach AI Something New, Without Making It Forget the Old.”</i>", st["body"]))
    story.append(Spacer(1, 6))

    meta_data = [
        [Paragraph("<b>Role:</b> Team Leader & Algorithm Theorist", st["td"]), Paragraph("<b>Category:</b> Novel Product-Based Innovation", st["td"])],
        [Paragraph("<b>Key Ownership:</b> Problem Formulation, EWC, Advisor, Q&A", st["td"]), Paragraph("<b>Partner:</b> Nuka Devashmitha Reddy", st["td"])],
        [Paragraph("<b>Live Cloud Demo:</b> <font color='#0284c7'>https://memory-mirror-ai.onrender.com</font>", st["td"]), Paragraph("<b>GitHub:</b> <font color='#0284c7'>devashmitha1308/memory-mirrorAI</font>", st["td"])],
    ]
    t = Table(meta_data, colWidths=[250, 254])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # 1. Executive Summary & Gauri's Core Concept
    story.append(Paragraph("1. Executive Summary & Gauri's Core Concept", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))
    summary_p = (
        "<b>What you must convey:</b> AI models suffer from <b>Catastrophic Forgetting</b>. When an AI learns "
        "Task B, standard gradient descent destroys the synaptic weights representing Task A.<br/>"
        "<b>The Musician Analogy (Use this in your speech!):</b> If a pianist learns the violin, but upon mastering the "
        "violin completely forgets how to play the piano, we wouldn't call that intelligence. "
        "MemoryMirror AI provides the AI with a memory mirror and synaptic stiffness so it masters both.<br/>"
        "<b>The Key Innovation:</b> Traditional ML tests models once at the end. MemoryMirror AI uses an active audit loop: "
        "<b>Every time the model learns anything new, it automatically goes back and audits everything it learned before.</b>"
    )
    story.append(Paragraph(summary_p, st["body"]))
    story.append(Spacer(1, 8))

    # 2. Gauri's Modules Deep Dive
    story.append(Paragraph("2. Gauri's Modules Deep Dive (What You Own)", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))

    gauri_modules = [
        [Paragraph("Module", st["th"]), Paragraph("Technical Functionality", st["th"]), Paragraph("How to Explain to Judges", st["th"])],
        [
            Paragraph("<b>Elastic Weight Consolidation (EWC)</b>", st["td_bold"]),
            Paragraph("• Calculates diagonal of Fisher Information Matrix (FIM) $F_i$.<br/>"
                      "• Adds quadratic penalty: $\\frac{\\lambda}{2} \\sum F_i (\\theta_i - \\theta_i^*)^2$.", st["td"]),
            Paragraph("<i>'Think of high-Fisher weights as stiff steel springs. We freeze the critical synapses that remember Task A, while soft flexible synapses learn Task B.'</i>", st["td"]),
        ],
        [
            Paragraph("<b>Forgetting Detection Engine</b>", st["td_bold"]),
            Paragraph("• Computes Forgetting Score: $f_j^k = \\max_{l < k} R_{l,j} - R_{k,j}$.<br/>"
                      "• Computes Backward Transfer (BWT) & Average Acc ($A_k$).<br/>"
                      "• Triggers automated Critical (>25%) & Warning (>15%) alerts.", st["td"]),
            Paragraph("<i>'The system doesn\\'t wait for a human to notice failure; it instantly calculates the exact percentage point drop and sounds an automated alert.'</i>", st["td"]),
        ],
        [
            Paragraph("<b>Analytical AI Advisor</b>", st["td_bold"]),
            Paragraph("• Generates Continual Learning Health Index (0–100, A+ to F).<br/>"
                      "• Analyzes Plasticity-Stability trade-off.<br/>"
                      "• Prescribes dynamic $\\lambda$ and buffer hyperparameter tuning.", st["td"]),
            Paragraph("<i>'We don\\'t just detect forgetting; our AI Advisor tells the engineer exactly what to change—like increasing $\\lambda$ by 2x—to fix it.'</i>", st["td"]),
        ],
    ]
    t_mod = Table(gauri_modules, colWidths=[110, 190, 204])
    t_mod.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 8))

    # 3. What is Used vs What is NOT Used (Gauri's Scope)
    story.append(Paragraph("3. Scope Audit: What is Used vs. What is NOT Used", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))
    scope_data = [
        [Paragraph("Category", st["th"]), Paragraph("What Gauri Built & Used", st["th"]), Paragraph("What Was Excluded & Why", st["th"])],
        [
            Paragraph("<b>Algorithm Choice</b>", st["td_bold"]),
            Paragraph("• Elastic Weight Consolidation (EWC) with Fisher Information.<br/>"
                      "• Multi-Task Joint Upper Bound Oracle for baseline.", st["td"]),
            Paragraph("• <b>Retraining from scratch:</b> Excluded because it is computationally impossible on continuous streaming data.<br/>"
                      "• <b>Full Hessian matrix:</b> Excluded because $O(P^2)$ memory is intractable; diagonal Fisher is $O(P)$ and optimal.", st["td"]),
        ],
        [
            Paragraph("<b>Model Architecture</b>", st["td_bold"]),
            Paragraph("• Continual neural network with He initialization and exact mathematical backprop.", st["td"]),
            Paragraph("• <b>Billion-parameter LLMs:</b> Excluded to ensure zero-latency demonstration and first-principles algorithmic validation.", st["td"]),
        ],
    ]
    t_scope = Table(scope_data, colWidths=[90, 210, 204])
    t_scope.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_scope)
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # 4. Gauri's Word-for-Word Speaking Script
    story.append(Paragraph("4. Gauri's Word-for-Word Speaking Script", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))

    story.append(Paragraph("PART 1: Opening & Problem Statement (~2 minutes)", st["h2"]))
    g_script_1 = (
        "<i>'Good morning respected judges and faculty. Imagine an AI deployed in hospitals to detect pneumonia. "
        "Next month, new data on COVID-19 arrives, and we train it. Shockingly, the model suddenly loses its ability "
        "to recognize pneumonia! In machine learning, this dangerous failure is known as <b>Catastrophic Forgetting</b>.<br/><br/>"
        "Today, my teammate Devashmitha and I present <b>MemoryMirror AI</b>, under the motto: "
        "<b>Teach AI something new, without making it forget the old.</b><br/><br/>"
        "Traditional systems only test an AI once at the very end. But MemoryMirror AI operates on a fundamental breakthrough: "
        "<b>Every time the model learns anything new, we automatically go back and audit everything it learned before.</b> "
        "To preserve knowledge, we formulated an active Forgetting Detection Engine and implemented Elastic Weight Consolidation (EWC), "
        "which uses the Fisher Information Matrix to freeze the model\\'s most vital synapses.<br/><br/>"
        "I will now invite Devashmitha to demonstrate our live working product deployed in the cloud.</i>"
    )
    story.append(Paragraph(g_script_1, st["script"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("PART 3: AI Advisor & Closing (~1.5 minutes)", st["h2"]))
    g_script_2 = (
        "<i>'Thank you, Devashmitha. As you saw, MemoryMirror AI doesn\\'t just detect memory loss; our <b>Analytical AI Advisor</b> "
        "evaluates the Plasticity-Stability trade-off and calculates a Continual Health Index from 0 to 100 with actionable recommendations.<br/><br/>"
        "From autonomous vehicles streaming new city environments to adaptive fraud detection, MemoryMirror AI makes continual learning "
        "reliable, quantifiable, and production-ready. AI should evolve without losing its past. Thank you, and we welcome your questions!'</i>"
    )
    story.append(Paragraph(g_script_2, st["script"]))
    story.append(Spacer(1, 8))

    # 5. Gauri's Judge Q&A Defense Cheat Sheet
    story.append(Paragraph("5. Gauri's Judge Q&A Defense Cheat Sheet", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))

    qas_gauri = [
        (
            "Q: 'Why not just retrain the entire model on all historical data?'",
            "<b>Your Answer:</b> 'Retraining from scratch is computationally impossible for streaming big data. If a hospital or Tesla fleet receives 50GB of new data every week, retraining on terabytes of past data causes massive compute costs, carbon emissions, and downtime. MemoryMirror AI learns incrementally in seconds while mathematically protecting past memories.'"
        ),
        (
            "Q: 'What exactly is the Fisher Information Matrix in EWC?'",
            "<b>Your Answer:</b> 'The Fisher Information Matrix measures the second-order curvature of the loss function. Intuitively, it tells us how sensitive the model\\'s past task predictions are to small changes in each synapse. Synapses with high Fisher values are vital to Task A, so EWC heavily penalizes modifying them during Task B.'"
        ),
        (
            "Q: 'What is the Plasticity-Stability dilemma?'",
            "<b>Your Answer:</b> 'If a model has too much plasticity, it learns new things fast but erases the past (catastrophic forgetting). If it has too much stability, its weights freeze and it cannot learn anything new. Our AI Advisor dynamically balances this by tracking Backward Transfer (BWT) to tune the stiffness parameter $\\lambda$.'"
        ),
    ]
    for q, a in qas_gauri:
        story.append(Paragraph(f"<b>{q}</b>", st["h2"]))
        story.append(Paragraph(a, st["body"]))
        story.append(Spacer(1, 3))

    doc.build(story, canvasmaker=GauriNumberedCanvas)
    print(f"[SUCCESS] Gauri PDF generated at: {filename}")


# =============================================================================
# BUILD DEVASHMITHA REDDY'S PDF (TECHNICAL LEAD)
# =============================================================================
def build_devashmitha_pdf(filename="MemoryMirror_AI_Devashmitha_Reddy_Member_Guide.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    st = get_styles()
    story = []

    # Header Card
    story.append(Paragraph("SPARKX 3.0 INTERNATIONAL INNOVATION CHALLENGE", st["subtitle"]))
    story.append(Spacer(1, 3))
    story.append(Paragraph("MEMORYMIRROR AI — TECHNICAL LEAD GUIDE", st["title"]))
    story.append(Paragraph("Prepared Exclusively for: <b>NUKA DEVASHMITHA REDDY</b> (Team Member / Tech Lead)", st["subtitle"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>“Teach AI Something New, Without Making It Forget the Old.”</i>", st["body"]))
    story.append(Spacer(1, 6))

    meta_data = [
        [Paragraph("<b>Role:</b> Technical Architecture, Replay & Cloud Deployment", st["td"]), Paragraph("<b>Category:</b> Novel Product-Based Innovation", st["td"])],
        [Paragraph("<b>Key Ownership:</b> Datasets, Neural Engine, Replay Buffer, UI, Render", st["td"]), Paragraph("<b>Partner:</b> Gauri Dwivedi (Team Leader)", st["td"])],
        [Paragraph("<b>Live Cloud Demo:</b> <font color='#0284c7'>https://memory-mirror-ai.onrender.com</font>", st["td"]), Paragraph("<b>GitHub:</b> <font color='#0284c7'>devashmitha1308/memory-mirrorAI</font>", st["td"])],
    ]
    t = Table(meta_data, colWidths=[250, 254])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # 1. Executive Summary & Devashmitha's Core Concept
    story.append(Paragraph("1. Executive Summary & Engineering Overview", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))
    summary_p = (
        "<b>What you must convey:</b> You built the complete, production-grade working model and deployed it live "
        "in the cloud at <b>memory-mirror-ai.onrender.com</b>.<br/>"
        "<b>The Engineering Achievement:</b> The platform contains a dual-engine architecture: a high-speed vectorized "
        "continual neural network written from mathematical first principles, an episodic Experience Replay buffer, "
        "and an interactive Streamlit + Plotly dashboard that visually demonstrates catastrophic forgetting occurring and being solved in real time.<br/>"
        "<b>Deployment:</b> 100% cloud-hosted 24/7 on Render with automated CI/CD from GitHub, unit-tested (100% pass), and exportable reports in JSON/CSV."
    )
    story.append(Paragraph(summary_p, st["body"]))
    story.append(Spacer(1, 8))

    # 2. Devashmitha's Modules Deep Dive
    story.append(Paragraph("2. Devashmitha's Modules Deep Dive (What You Own)", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))

    deva_modules = [
        [Paragraph("Module", st["th"]), Paragraph("Technical Functionality", st["th"]), Paragraph("How to Explain to Judges", st["th"])],
        [
            Paragraph("<b>Dataset Manager</b>", st["td_bold"]),
            Paragraph("• Split MNIST: Task A (0–4) vs Task B (5–9).<br/>"
                      "• 5-Task Incremental Digits (2 digits per stage).<br/>"
                      "• Sensory shift (inversion & noise) & synthetic drift.", st["td"]),
            Paragraph("<i>'Our Dataset Manager streams non-overlapping tasks sequentially, simulating real-world non-stationary environments.'</i>", st["td"]),
        ],
        [
            Paragraph("<b>ContinualMLP Neural Engine</b>", st["td_bold"]),
            Paragraph("• Vectorized forward inference & backpropagation.<br/>"
                      "• He weight initialization + Adam optimizer.<br/>"
                      "• Task-IL class masking & Frobenius weight drift tracking.", st["td"]),
            Paragraph("<i>'I engineered the neural network from first principles so it executes in milliseconds without heavy GPU latency during live demos.'</i>", st["td"]),
        ],
        [
            Paragraph("<b>Experience Replay (Memory Mirror)</b>", st["td_bold"]),
            Paragraph("• Episodic memory reservoir buffer.<br/>"
                      "• Stores balanced prototype exemplars per class.<br/>"
                      "• Interleaves memory batches during subsequent task training.", st["td"]),
            Paragraph("<i>'Like human memory, the model rehearses a tiny handful of past prototypes alongside new experiences, preserving accuracy at 96.5%.'</i>", st["td"]),
        ],
        [
            Paragraph("<b>Streamlit Web App & Render Cloud</b>", st["td_bold"]),
            Paragraph("• 5 interactive dashboard tabs.<br/>"
                      "• Plotly timelines, heatmaps, waterfall, and radars.<br/>"
                      "• 24/7 cloud hosting on Render via <code>render.yaml</code>.", st["td"]),
            Paragraph("<i>'The judges can open memory-mirror-ai.onrender.com on their own phones right now and run the live benchmark.'</i>", st["td"]),
        ],
    ]
    t_mod = Table(deva_modules, colWidths=[110, 190, 204])
    t_mod.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 8))

    # 3. What is Used vs What is NOT Used (Devashmitha's Scope)
    story.append(Paragraph("3. Scope Audit: What is Used vs. What is NOT Used", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))
    scope_data = [
        [Paragraph("Category", st["th"]), Paragraph("What Devashmitha Built & Used", st["th"]), Paragraph("What Was Excluded & Why", st["th"])],
        [
            Paragraph("<b>Memory Buffer</b>", st["td_bold"]),
            Paragraph("• Bounded reservoir buffer (50 exemplars per task).<br/>"
                      "• Visual inspection of cached prototypes in UI.", st["td"]),
            Paragraph("• <b>Unbounded storage:</b> Excluded because storing all raw data violates data privacy (GDPR/HIPAA) and consumes infinite memory.", st["td"]),
        ],
        [
            Paragraph("<b>Web Stack & Hosting</b>", st["td_bold"]),
            Paragraph("• Streamlit + Plotly + Render Cloud Hosting.<br/>"
                      "• Dual-layer local background auto-restart on Windows.", st["td"]),
            Paragraph("• <b>Static PowerPoint slides:</b> Excluded in favor of a live interactive cloud product accessible on any device.", st["td"]),
        ],
    ]
    t_scope = Table(scope_data, colWidths=[90, 210, 204])
    t_scope.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_scope)
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # 4. Devashmitha's Word-for-Word Speaking Script
    story.append(Paragraph("4. Devashmitha's Word-for-Word Live Demo Script", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))

    story.append(Paragraph("PART 2: Architecture & Live Cloud Demonstration (~2.5 minutes)", st["h2"]))
    d_script = (
        "<i>'Thank you, Gauri! Respected judges, you can see our live working product right now at "
        "<b>memory-mirror-ai.onrender.com</b>.<br/><br/>"
        "Let us demonstrate how catastrophic forgetting actually happens. In our sidebar, we select our baseline: "
        "<b>Naive Fine-Tuning</b> on the Split MNIST benchmark.<br/><br/>"
        "• <b>Step 1:</b> The model learns Task A (Digits 0 to 4). It reaches 100% accuracy.<br/>"
        "• <b>Step 2:</b> Now we teach it Task B (Digits 5 to 9). Watch the Forgetting Timeline: the instant Task B is learned, "
        "Task A accuracy plummets down to 85%—a 15-point drop! Our Forgetting Detection Engine immediately triggers a "
        "<b>CRITICAL ALERT</b> on screen.<br/><br/>"
        "• <b>Step 3:</b> Now we activate our preservation algorithms: <b>Experience Replay</b> and <b>Elastic Weight Consolidation (EWC)</b>. "
        "With EWC stiffness set to $\\lambda=1000$, Task A retains 95.1% accuracy—a massive 10-point preservation boost! "
        "And with Replay, past accuracy is preserved at 96.5%.<br/><br/>"
        "• <b>Step 4:</b> If you click on Tab 3, you can inspect the actual prototype images cached in our episodic memory mirror buffer. "
        "And in Tab 2, our multi-strategy benchmark plots all 4 methods side-by-side on an interactive radar chart. "
        "Finally, all experiment results can be exported as JSON or CSV reports with one click.<br/><br/>"
        "I will now hand back to Gauri to walk through our AI Advisor and real-world impact.'</i>"
    )
    story.append(Paragraph(d_script, st["script"]))
    story.append(Spacer(1, 8))

    # 5. Devashmitha's Judge Q&A Defense Cheat Sheet
    story.append(Paragraph("5. Devashmitha's Judge Q&A Defense Cheat Sheet", st["h1"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=6))

    qas_deva = [
        (
            "Q: 'Doesn\\'t Experience Replay require massive storage and violate privacy?'",
            "<b>Your Answer:</b> 'No, because we do not store raw datasets. Our Dataset Manager uses a bounded reservoir buffer storing only 50 representative prototype exemplars per task. More importantly, if strict privacy regulations like HIPAA or GDPR forbid storing any raw samples, our system seamlessly switches to Elastic Weight Consolidation (EWC), which stores zero raw data and relies purely on synaptic stiffness.'"
        ),
        (
            "Q: 'What is the evaluation matrix R and how do judges read it?'",
            "<b>Your Answer:</b> 'The matrix $R_{i,j}$ displays the accuracy on Task $j$ after completing training on Task $i$. The diagonal values $R_{i,i}$ show how well each task was learned initially. The values below the diagonal reveal whether older tasks degraded or remained stable as new tasks were added.'"
        ),
        (
            "Q: 'How is this deployed in production?'",
            "<b>Your Answer:</b> 'The application is containerized and running 24/7 on Render cloud with automated CI/CD directly linked to our GitHub repository `devashmitha1308/memory-mirrorAI`. It requires zero setup and is accessible worldwide from any mobile browser or desktop.'"
        ),
    ]
    for q, a in qas_deva:
        story.append(Paragraph(f"<b>{q}</b>", st["h2"]))
        story.append(Paragraph(a, st["body"]))
        story.append(Spacer(1, 3))

    doc.build(story, canvasmaker=DevaNumberedCanvas)
    print(f"[SUCCESS] Devashmitha PDF generated at: {filename}")


if __name__ == "__main__":
    build_gauri_pdf()
    build_devashmitha_pdf()
