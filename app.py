"""
MemoryMirror AI - Streamlit Web Dashboard
SparkX 3.0 | International Project Innovation Challenge
Team Leader: Gauri Dwivedi | Team Member: Nuka Devashmitha Reddy
"Teach AI Something New, Without Making It Forget the Old."
"""

import json
import time
import numpy as np
import pandas as pd
import streamlit as st

from memory_mirror.datasets import DatasetManager, TaskData
from memory_mirror.evaluation import EvaluationEngine, ExperimentResult
from memory_mirror.metrics import ContinualMetrics
from memory_mirror.advisor import ContinualLearningAdvisor
from memory_mirror.visualizer import ContinualVisualizer, PALETTE


# -----------------------------------------------------------------------------
# Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MemoryMirror AI | SparkX 3.0",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    /* Dark AI Lab Modern Theme */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Gradient & Badges */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid #312e81;
        border-radius: 14px;
        padding: 24px 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
    }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .badge-sparkx {
        background: rgba(236, 72, 153, 0.15);
        color: #f472b6;
        border: 1px solid rgba(236, 72, 153, 0.35);
    }
    .badge-novel {
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.35);
    }
    .badge-leader {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .badge-member {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 6px;
        margin-bottom: 6px;
    }
    
    .hero-motto {
        font-size: 15px;
        font-style: italic;
        color: #94a3b8;
        margin-bottom: 12px;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }
    .metric-val {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 4px;
    }
    .metric-lbl {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9ca3af;
    }
    
    /* Alert Boxes */
    .alert-card-critical {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        color: #fca5a5;
    }
    .alert-card-high {
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        color: #fcd34d;
    }
    .alert-card-stable {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        color: #6ee7b7;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Hero Header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div>
            <span class="badge-pill badge-sparkx">🏆 SparkX 3.0 International Innovation Challenge</span>
            <span class="badge-pill badge-novel">✨ Novel Product-Based Innovation</span>
            <span class="badge-pill badge-leader">👑 Team Leader: Gauri Dwivedi</span>
            <span class="badge-pill badge-member">🚀 Team Member: Nuka Devashmitha Reddy</span>
        </div>
        <div class="hero-title">MEMORY MIRROR AI</div>
        <div class="hero-motto">“Teach AI Something New, Without Making It Forget the Old.”</div>
        <div style="font-size: 13.5px; color: #cbd5e1; max-width: 900px;">
            An Intelligent Continual Learning & Memory Retention Monitoring System that detects, quantifies, and shields 
            artificial neural networks against <b>catastrophic forgetting</b> through real-time backward transfer analysis, 
            Elastic Weight Consolidation (EWC), and episodic rehearsal.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Sidebar: Benchmark & Model Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image(
        "https://img.icons8.com/isometric/100/brain.png",
        width=60,
    )
    st.title("Control Center")
    st.markdown("Configure datasets, sequential training parameters, and preservation strategies.")

    st.subheader("1. Benchmark Selection")
    benchmark_choice = st.selectbox(
        "Continual Learning Benchmark",
        DatasetManager.AVAILABLE_DATASETS,
        index=0,
        help="Select sequential task sequence. Default matches SparkX 3.0 slide: Task A (0-4) vs Task B (5-9).",
    )

    st.subheader("2. Memory Preservation")
    strategy_mode = st.radio(
        "Evaluation Mode",
        [
            "⚡ Compare All 4 Strategies (Head-to-Head)",
            "Naive Fine-Tuning (Catastrophic Forgetting Baseline)",
            "Elastic Weight Consolidation (EWC)",
            "Experience Replay (Rehearsal Buffer)",
            "Joint Multi-Task (Upper Bound Oracle)",
        ],
        index=0,
    )

    st.subheader("3. Hyperparameters")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        epochs_per_task = st.slider("Epochs / Task", min_value=3, max_value=30, value=12, step=1)
        learning_rate = st.slider("Learning Rate", min_value=0.001, max_value=0.02, value=0.005, step=0.001, format="%.3f")
    with col_sb2:
        batch_size = st.select_slider("Batch Size", options=[16, 32, 64, 128], value=32)
        hidden_dim = st.select_slider("Hidden Units", options=[32, 64, 128], value=64)

    # Strategy-specific parameters
    ewc_lambda = 800.0
    buffer_size = 50
    if "EWC" in strategy_mode or "Compare" in strategy_mode:
        ewc_lambda = st.slider(
            "EWC Stiffness (λ)",
            min_value=100.0,
            max_value=3000.0,
            value=1000.0,
            step=100.0,
            help="Higher λ enforces stronger Fisher Information stiffness to protect past task synapses.",
        )

    if "Replay" in strategy_mode or "Compare" in strategy_mode:
        buffer_size = st.slider(
            "Replay Buffer Size / Task",
            min_value=10,
            max_value=150,
            value=50,
            step=10,
            help="Number of exemplar prototypes stored per task in the episodic memory mirror.",
        )

    st.markdown("---")
    run_btn = st.button("🚀 Run Continual Learning Engine", type="primary", use_container_width=True)

    st.markdown(
        """
        <div style="font-size: 11.5px; color: #64748b; margin-top: 15px; text-align: center;">
            MemoryMirror AI v1.0 • SPARKX 3.0 Challenge<br>
            Developed by Gauri Dwivedi & Nuka Devashmitha Reddy
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Session State Initialization & Engine Runner
# -----------------------------------------------------------------------------
if "cached_benchmark" not in st.session_state:
    st.session_state.cached_benchmark = None
    st.session_state.cached_tasks = None
    st.session_state.cached_results = None
    st.session_state.is_multi = True

# Automatically load initial dataset if none
if st.session_state.cached_tasks is None or st.session_state.cached_benchmark != benchmark_choice:
    with st.spinner(f"Loading benchmark: {benchmark_choice}..."):
        st.session_state.cached_tasks = DatasetManager.load_task_sequence(benchmark_choice)
        st.session_state.cached_benchmark = benchmark_choice

# Execute when Run is pressed OR on initial first load
should_execute = run_btn or (st.session_state.cached_results is None)

if should_execute:
    with st.spinner("🧠 Executing Continual Learning Sequential Pipeline..."):
        tasks = st.session_state.cached_tasks

        if "Compare" in strategy_mode:
            st.session_state.cached_results = EvaluationEngine.run_all_comparative_benchmark(
                tasks=tasks,
                benchmark_name=benchmark_choice,
                hidden_dim=hidden_dim,
                epochs_per_task=epochs_per_task,
                batch_size=batch_size,
                lr=learning_rate,
                ewc_lambda=ewc_lambda,
                buffer_size=buffer_size,
            )
            st.session_state.is_multi = True
        else:
            strat_key = "Naive"
            if "EWC" in strategy_mode:
                strat_key = "EWC"
            elif "Replay" in strategy_mode:
                strat_key = "Replay"
            elif "Joint" in strategy_mode:
                strat_key = "Joint"

            res = EvaluationEngine.run_strategy(
                strategy_type=strat_key,
                tasks=tasks,
                benchmark_name=benchmark_choice,
                hidden_dim=hidden_dim,
                epochs_per_task=epochs_per_task,
                batch_size=batch_size,
                lr=learning_rate,
                ewc_lambda=ewc_lambda,
                buffer_size=buffer_size,
            )
            st.session_state.cached_results = {strat_key: res}
            st.session_state.is_multi = False

tasks = st.session_state.cached_tasks
results_map = st.session_state.cached_results

# Select active primary result for single-strategy views (default Naive or first)
primary_key = "Naive" if "Naive" in results_map else list(results_map.keys())[0]
primary_res = results_map[primary_key]


# -----------------------------------------------------------------------------
# Main Dashboard Tabs
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "📊 Retention & Forgetting Analysis",
    "🥊 Multi-Strategy Benchmark",
    "🧠 Synaptic Plasticity & Memory Mirror",
    "💡 Analytical AI Advisor",
    "📜 SparkX 3.0 Project Brief & Docs",
])


# =============================================================================
# TAB 1: RETENTION & FORGETTING ANALYSIS
# =============================================================================
with tabs[0]:
    st.subheader("Continual Retention & Catastrophic Forgetting Monitor")
    st.markdown(
        f"Real-time evaluation across **{len(tasks)} sequential tasks** under "
        f"**`{primary_res.strategy_name}`**."
    )

    # Top KPI Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Final Average Accuracy</div>
                <div class="metric-val" style="color: #38bdf8;">{primary_res.final_avg_accuracy:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        forgetting_color = "#ef4444" if primary_res.avg_forgetting > 15 else "#10b981"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Average Forgetting (F)</div>
                <div class="metric-val" style="color: {forgetting_color};">{primary_res.avg_forgetting:.1f} <span style="font-size:16px;">pts</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        bwt_color = "#10b981" if primary_res.backward_transfer >= 0 else "#f43f5e"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Backward Transfer (BWT)</div>
                <div class="metric-val" style="color: {bwt_color};">{primary_res.backward_transfer:+.1f} <span style="font-size:16px;">pts</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Execution Time</div>
                <div class="metric-val" style="color: #c084fc;">{primary_res.execution_time_sec:.2f} <span style="font-size:16px;">s</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Forgetting Detection Alerts Section
    if primary_res.alerts:
        st.markdown("##### 🚨 Catastrophic Forgetting Events Detected")
        for alert in primary_res.alerts:
            card_class = "alert-card-critical" if alert.severity == "CRITICAL" else "alert-card-high"
            st.markdown(
                f"""
                <div class="{card_class}">
                    <b>[{alert.severity}]</b> {alert.message}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="alert-card-stable">
                <b>[STABLE RETENTION]</b> No catastrophic forgetting events detected. Memory retention remains stable across sequential tasks!
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row: Forgetting Timeline & Accuracy Heatmap
    col_chart1, col_chart2 = st.columns([1.1, 0.9])
    with col_chart1:
        timeline_fig = ContinualVisualizer.plot_forgetting_timeline(primary_res)
        st.plotly_chart(timeline_fig, use_container_width=True)

    with col_chart2:
        heatmap_fig = ContinualVisualizer.plot_accuracy_matrix_heatmap(primary_res)
        st.plotly_chart(heatmap_fig, use_container_width=True)

    # Task Degradation Waterfall
    waterfall_fig = ContinualVisualizer.plot_task_degradation_waterfall(primary_res)
    st.plotly_chart(waterfall_fig, use_container_width=True)


# =============================================================================
# TAB 2: MULTI-STRATEGY BENCHMARK
# =============================================================================
with tabs[1]:
    st.subheader("Head-to-Head Continual Learning Benchmark")
    st.markdown("Direct quantitative comparison of memory preservation paradigms against the naive catastrophic forgetting baseline.")

    if not st.session_state.is_multi:
        st.info("💡 You are currently viewing a single strategy. Select 'Compare All 4 Strategies' in the sidebar to view full multi-strategy comparative charts!")

    # Multi-strategy summary bar chart & radar
    col_bm1, col_bm2 = st.columns([1.1, 0.9])
    with col_bm1:
        comp_fig = ContinualVisualizer.plot_strategy_comparison(results_map)
        st.plotly_chart(comp_fig, use_container_width=True)

    with col_bm2:
        radar_fig = ContinualVisualizer.plot_tradeoff_radar(results_map)
        st.plotly_chart(radar_fig, use_container_width=True)

    # Comparative Metric Table
    st.markdown("##### 📋 Quantitative Benchmark Leaderboard")
    table_rows = []
    for s_name, res in results_map.items():
        table_rows.append({
            "Strategy": s_name,
            "Final Avg Accuracy (%)": f"{res.final_avg_accuracy:.2f}%",
            "Average Forgetting (F)": f"{res.avg_forgetting:.2f} pts",
            "Backward Transfer (BWT)": f"{res.backward_transfer:+.2f} pts",
            "Critical Drops": len([a for a in res.alerts if a.severity == "CRITICAL"]),
            "Param Drift Norm": f"{res.weight_drift:.2f}",
            "Compute Time (s)": f"{res.execution_time_sec:.2f}s",
        })
    df_compare = pd.DataFrame(table_rows)
    st.dataframe(df_compare, use_container_width=True, hide_index=True)


# =============================================================================
# TAB 3: SYNAPTIC PLASTICITY & MEMORY MIRROR BUFFER
# =============================================================================
with tabs[2]:
    st.subheader("Inside the Memory Mirror: Synaptic Protection & Rehearsal Buffer")
    st.markdown("Inspecting parameter-level stiffness mechanisms (Fisher Information) and stored memory exemplars.")

    col_syn1, col_syn2 = st.columns(2)

    with col_syn1:
        st.markdown("##### 🛡️ Elastic Weight Consolidation (Fisher Stiffness)")
        st.markdown(
            """
            EWC calculates the diagonal curvature of the loss surface for past tasks using the 
            **Fisher Information Matrix (FIM)**. High-stiffness synapses are shielded from updates during new tasks:
            $$\\mathcal{L}(\\theta) = \\mathcal{L}_{\\text{new}}(\\theta) + \\sum_i \\frac{\\lambda}{2} F_i (\\theta_i - \\theta_i^*)^2$$
            """
        )

        ewc_res = results_map.get("EWC", primary_res)
        if "fisher_summary" in ewc_res.extra_info and ewc_res.extra_info["fisher_summary"]:
            st.json(ewc_res.extra_info["fisher_summary"])
        else:
            # Display layer weight drift
            drift_fig = ContinualVisualizer.plot_fisher_importance_map(ewc_res.layer_drift)
            st.plotly_chart(drift_fig, use_container_width=True)

    with col_syn2:
        st.markdown("##### 🪞 Episodic Memory Mirror Buffer")
        st.markdown(
            """
            The rehearsal buffer stores a reservoir of exemplar prototypes from past tasks.
            During training on subsequent tasks, memory mirror exemplars are interleaved into gradient batches.
            """
        )

        replay_res = results_map.get("Replay", primary_res)
        if "replay_buffer" in replay_res.extra_info:
            buf_info = replay_res.extra_info["replay_buffer"]
            st.markdown(
                f"""
                - **Total Exemplars Cached:** `{buf_info['total_exemplars']}`
                - **Unique Classes Retained:** `{buf_info['classes_retained']}`
                - **Task Distribution:** `{buf_info['task_distribution']}`
                """
            )

        # Visual preview of sample exemplar images
        st.markdown("###### Sample Prototypes Cached in Memory Mirror:")
        preview_cols = st.columns(min(6, len(tasks[0].classes)))
        for idx, (cls_id, img_arr) in enumerate(tasks[0].sample_images.items()):
            if idx < len(preview_cols):
                with preview_cols[idx]:
                    st.caption(f"Class {cls_id}")
                    st.image(img_arr, width=50, clamp=True)


# =============================================================================
# TAB 4: ANALYTICAL AI ADVISOR
# =============================================================================
with tabs[3]:
    st.subheader("Analytical Recommendations & Continual Learning Health Advisor")
    st.markdown("Automated diagnostic assessment of plasticity-stability trade-offs and prescriptive optimizations.")

    diag = ContinualLearningAdvisor.generate_diagnosis(primary_res)

    col_diag1, col_diag2 = st.columns([0.4, 0.6])
    with col_diag1:
        st.markdown(
            f"""
            <div style="background-color: #111827; border: 2px solid {diag['status_color']}; border-radius: 14px; padding: 24px; text-align: center;">
                <div style="font-size: 13px; text-transform: uppercase; color: #94a3b8; font-weight: 700;">Continual Health Index</div>
                <div style="font-size: 48px; font-weight: 800; color: {diag['status_color']}; margin: 8px 0;">{diag['health_score']}<span style="font-size:22px;">/100</span></div>
                <div style="font-size: 18px; font-weight: 700; color: #ffffff;">{diag['grade']}</div>
                <div style="font-size: 13px; color: #94a3b8; margin-top: 10px;">{diag['diagnosis_summary']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_diag2:
        st.markdown("##### ⚖️ Plasticity-Stability Trade-Off Assessment")
        st.info(diag["plasticity_stability_tradeoff"])

        st.markdown("##### 💡 Prescriptive Optimization Actions")
        for rec in diag["recommendations"]:
            st.markdown(
                f"""
                - **[{rec.priority} | {rec.category}]**: {rec.action}
                  *Rationale:* {rec.rationale}
                """
            )


# =============================================================================
# TAB 5: SPARKX 3.0 PROJECT BRIEF & DOCS
# =============================================================================
with tabs[4]:
    st.subheader("SparkX 3.0 International Project Innovation Challenge")
    st.markdown(
        """
        ### MEMORYMIRROR AI
        **An Intelligent Continual Learning & Memory Retention Monitoring System**  
        *“Teach AI Something New, Without Making It Forget the Old.”*  
        **Category:** Novel Product-Based Innovation  
        **Team Leader:** Gauri Dwivedi  
        **Team Member:** Nuka Devashmitha Reddy  
        """
    )

    st.markdown("---")
    st.markdown(
        """
        #### 1. What is Catastrophic Forgetting?
        When a neural network is sequentially trained on a new task, backpropagation updates weights along the loss gradient of the new task, 
        often overwriting the orthogonal parameter configurations required for previously learned tasks. 
        As an illustrative example:
        1. Model learns to recognize fruits (Task A).
        2. Then we teach it vehicles (Task B).
        3. Now it misclassifies fruits because earlier synaptic representations were overwritten.

        #### 2. The MemoryMirror AI 6-Step Workflow:
        1. **Select model & datasets**: Choose architecture and sequential tasks in order.
        2. **Establish baseline**: Record baseline accuracy on prior tasks.
        3. **Train on a new task**: Stream new task batches.
        4. **Retest earlier tasks**: Evaluate all prior tasks across milestones.
        5. **Calculate forgetting**: Compute peak past score minus current score:
           $$\\text{Forgetting} = \\max_{l < k} R_{l, j} - R_{k, j}$$
        6. **Display retention analysis**: Generate real-time retention timelines, $R$ matrices, and proactive alerts.

        #### 3. Core Formulas Tracked:
        - **Average Accuracy ($A_k$):** $A_k = \\frac{1}{k} \\sum_{j=1}^k R_{k,j}$
        - **Average Forgetting ($F_k$):** $F_k = \\frac{1}{k-1} \\sum_{j=1}^{k-1} f_j^k$
        - **Backward Transfer (BWT):** $\\text{BWT} = \\frac{1}{T-1} \\sum_{j=1}^{T-1} (R_{T,j} - R_{j,j})$
        - **EWC Quadratic Penalty:** $\\Omega(\\theta) = \\sum_k \\frac{\\lambda}{2} F_{k,i} (\\theta_i - \\theta_{k,i}^*)^2$
        """
    )

    st.markdown("---")
    st.markdown("#### 📦 Export Experiment Artifacts")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        json_str = json.dumps(primary_res.to_dict(), indent=2)
        st.download_button(
            label="📥 Download Experiment Report (JSON)",
            data=json_str,
            file_name=f"memory_mirror_report_{int(time.time())}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_exp2:
        csv_str = primary_res.to_dataframe().to_csv()
        st.download_button(
            label="📥 Download R Matrix (CSV)",
            data=csv_str,
            file_name=f"memory_mirror_R_matrix_{int(time.time())}.csv",
            mime="text/csv",
            use_container_width=True,
        )
