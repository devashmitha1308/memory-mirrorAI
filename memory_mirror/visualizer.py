"""
Visualization Engine for MemoryMirror AI.
Generates interactive, publication-ready Plotly charts for:
- Task-wise Retention & Forgetting Timelines
- Accuracy Matrix Heatmaps (R)
- Task Degradation Waterfall & Drop Analysis
- Multi-Strategy Benchmark Radar & Bar Charts
- Fisher Information Synaptic Importance Heatmaps
"""

from typing import List, Dict, Any, Optional
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from .evaluation import ExperimentResult


# Unified sleek dark-mode visual palette
PALETTE = {
    "bg": "#0f172a",
    "card_bg": "#1e293b",
    "border": "#334155",
    "text": "#f8fafc",
    "text_muted": "#94a3b8",
    "accent_cyan": "#06b6d4",
    "accent_blue": "#3b82f6",
    "accent_violet": "#8b5cf6",
    "accent_emerald": "#10b981",
    "accent_amber": "#f59e0b",
    "accent_rose": "#f43f5e",
    "task_colors": ["#38bdf8", "#ec4899", "#10b981", "#f59e0b", "#a855f7", "#6366f1"],
}


class ContinualVisualizer:
    """Creates styled interactive Plotly visualizations."""

    @staticmethod
    def plot_forgetting_timeline(result: ExperimentResult) -> go.Figure:
        """
        Interactive line chart displaying how the performance of each task
        evolves as new tasks are learned sequentially.
        """
        R = result.R_matrix
        T = R.shape[0]
        stages = [f"Stage {i+1}: {result.task_names[i]}" for i in range(T)]

        fig = go.Figure()

        for task_idx in range(T):
            task_name = result.task_names[task_idx]
            color = PALETTE["task_colors"][task_idx % len(PALETTE["task_colors"])]

            # Performance on task_idx at each training stage:
            # Before learning task_idx, accuracy is 0-shot / unlearned (can show or mark with dashed)
            accuracies = [R[stage_idx, task_idx] for stage_idx in range(T)]

            # Differentiate before-learning vs post-learning
            learned_stages = list(range(task_idx, T))
            learned_accs = [accuracies[s] for s in learned_stages]
            x_labels = [stages[s] for s in learned_stages]

            fig.add_trace(
                go.Scatter(
                    x=x_labels,
                    y=learned_accs,
                    mode="lines+markers+text",
                    name=task_name,
                    line=dict(color=color, width=3.5),
                    marker=dict(size=10, symbol="circle"),
                    text=[f"{v:.1f}%" for v in learned_accs],
                    textposition="top center",
                    textfont=dict(size=11, color=PALETTE["text"]),
                    hovertemplate="<b>%{x}</b><br>" + f"{task_name}: %{{y:.1f}}%<extra></extra>",
                )
            )

        fig.update_layout(
            title=dict(
                text=f"<b>Task-Wise Retention Timeline</b> — <i>{result.strategy_name}</i>",
                font=dict(size=16, color=PALETTE["text"]),
            ),
            xaxis=dict(
                title="Sequential Training Milestones",
                gridcolor=PALETTE["border"],
                tickfont=dict(color=PALETTE["text"]),
            ),
            yaxis=dict(
                title="Test Accuracy (%)",
                range=[0, 105],
                gridcolor=PALETTE["border"],
                tickfont=dict(color=PALETTE["text"]),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color=PALETTE["text"]),
            ),
            margin=dict(l=40, r=40, t=70, b=40),
            hovermode="x unified",
        )
        return fig

    @staticmethod
    def plot_accuracy_matrix_heatmap(result: ExperimentResult) -> go.Figure:
        """
        Interactive R matrix heatmap:
        Rows: Model state after training on Task i
        Columns: Accuracy evaluated on Task j
        """
        R = result.R_matrix
        T = R.shape[0]
        row_labels = [f"After {name}" for name in result.task_names]
        col_labels = [f"Eval {name}" for name in result.task_names]

        # Text labels for cells
        text_matrix = [[f"{val:.1f}%" for val in row] for row in R]

        fig = go.Figure(
            data=go.Heatmap(
                z=R,
                x=col_labels,
                y=row_labels,
                text=text_matrix,
                texttemplate="%{text}",
                textfont=dict(size=13, color="#ffffff", family="sans-serif"),
                colorscale=[
                    [0.0, "#0f172a"],
                    [0.4, "#1e3a8a"],
                    [0.7, "#0d9488"],
                    [1.0, "#10b981"],
                ],
                zmin=0,
                zmax=100,
                colorbar=dict(
                    title=dict(text="Accuracy (%)", font=dict(color=PALETTE["text"])),
                    tickfont=dict(color=PALETTE["text"]),
                ),
                hoverongaps=False,
            )
        )

        fig.update_layout(
            title=dict(
                text=f"<b>Continual Evaluation Matrix (R)</b> — <i>R[i, j] Accuracy</i>",
                font=dict(size=16, color=PALETTE["text"]),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickfont=dict(color=PALETTE["text"])),
            yaxis=dict(tickfont=dict(color=PALETTE["text"]), autorange="reversed"),
            margin=dict(l=40, r=40, t=60, b=40),
        )
        return fig

    @staticmethod
    def plot_task_degradation_waterfall(result: ExperimentResult) -> go.Figure:
        """Visualizes Peak Accuracy vs Final Accuracy drop for each task."""
        R = result.R_matrix
        T = R.shape[0]

        task_names = result.task_names
        initial_accs = [float(R[i, i]) for i in range(T)]
        final_accs = [float(R[-1, i]) for i in range(T)]
        drops = [init - fin for init, fin in zip(initial_accs, final_accs)]

        fig = go.Figure()

        # Initial Peak Bar
        fig.add_trace(
            go.Bar(
                x=task_names,
                y=initial_accs,
                name="Initial Peak Accuracy (When Learned)",
                marker_color=PALETTE["accent_cyan"],
                opacity=0.85,
                text=[f"{v:.1f}%" for v in initial_accs],
                textposition="auto",
            )
        )

        # Final Retained Bar
        fig.add_trace(
            go.Bar(
                x=task_names,
                y=final_accs,
                name="Final Retained Accuracy (End of Sequence)",
                marker_color=PALETTE["accent_violet"],
                opacity=0.85,
                text=[f"{v:.1f}%" for v in final_accs],
                textposition="auto",
            )
        )

        fig.update_layout(
            barmode="group",
            title=dict(
                text="<b>Task Memory Degradation</b> (Initial Peak vs Final Retained)",
                font=dict(size=16, color=PALETTE["text"]),
            ),
            xaxis=dict(tickfont=dict(color=PALETTE["text"])),
            yaxis=dict(
                title="Accuracy (%)",
                range=[0, 105],
                gridcolor=PALETTE["border"],
                tickfont=dict(color=PALETTE["text"]),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color=PALETTE["text"]),
            ),
            margin=dict(l=40, r=40, t=70, b=40),
        )
        return fig

    @staticmethod
    def plot_strategy_comparison(results_map: Dict[str, ExperimentResult]) -> go.Figure:
        """
        Grouped comparative chart comparing Naive vs Replay vs EWC vs Joint
        across Average Accuracy, Forgetting, and Backward Transfer.
        """
        strategies = list(results_map.keys())
        avg_accs = [results_map[s].final_avg_accuracy for s in strategies]
        forgettings = [results_map[s].avg_forgetting for s in strategies]
        bwts = [results_map[s].backward_transfer for s in strategies]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=strategies,
                y=avg_accs,
                name="Final Avg Accuracy (↑ Better)",
                marker_color="#10b981",
                text=[f"{v:.1f}%" for v in avg_accs],
                textposition="auto",
            )
        )

        fig.add_trace(
            go.Bar(
                x=strategies,
                y=forgettings,
                name="Average Forgetting (↓ Lower Better)",
                marker_color="#f43f5e",
                text=[f"{v:.1f} pts" for v in forgettings],
                textposition="auto",
            )
        )

        fig.add_trace(
            go.Bar(
                x=strategies,
                y=bwts,
                name="Backward Transfer (BWT)",
                marker_color="#38bdf8",
                text=[f"{v:+.1f} pts" for v in bwts],
                textposition="auto",
            )
        )

        fig.update_layout(
            barmode="group",
            title=dict(
                text="<b>Multi-Strategy Continual Benchmark Comparison</b>",
                font=dict(size=16, color=PALETTE["text"]),
            ),
            xaxis=dict(tickfont=dict(color=PALETTE["text"])),
            yaxis=dict(
                title="Score / Points",
                gridcolor=PALETTE["border"],
                tickfont=dict(color=PALETTE["text"]),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color=PALETTE["text"]),
            ),
            margin=dict(l=40, r=40, t=70, b=40),
        )
        return fig

    @staticmethod
    def plot_tradeoff_radar(results_map: Dict[str, ExperimentResult]) -> go.Figure:
        """Interactive Radar chart mapping multi-dimensional trade-offs."""
        categories = [
            "Retention Stability",
            "Final Accuracy",
            "Backward Transfer",
            "Plasticity Speed",
            "Parameter Protection",
        ]

        fig = go.Figure()

        color_map = {
            "Naive": "#ef4444",
            "Replay": "#3b82f6",
            "EWC": "#8b5cf6",
            "Joint": "#10b981",
        }

        for strat_name, res in results_map.items():
            # Normalize to 0-100 scale for radar
            retention = max(0.0, min(100.0, 100.0 - (res.avg_forgetting * 2.0)))
            acc = res.final_avg_accuracy
            bwt_norm = max(0.0, min(100.0, (res.backward_transfer + 50.0)))
            plasticity = min(100.0, max(20.0, 100.0 - res.execution_time_sec * 5.0))
            param_stability = max(0.0, min(100.0, 100.0 - res.weight_drift * 3.0))

            values = [retention, acc, bwt_norm, plasticity, param_stability]
            values.append(values[0])  # Close the radar loop

            color = color_map.get(strat_name, PALETTE["accent_cyan"])

            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories + [categories[0]],
                    fill="toself",
                    name=strat_name,
                    line=dict(color=color, width=2.5),
                    opacity=0.6,
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color=PALETTE["text_muted"], size=10),
                    gridcolor=PALETTE["border"],
                ),
                angularaxis=dict(
                    tickfont=dict(color=PALETTE["text"], size=12),
                    gridcolor=PALETTE["border"],
                ),
                bgcolor="rgba(15, 23, 42, 0.6)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            title=dict(
                text="<b>Continual Learning Trade-Off Radar</b>",
                font=dict(size=16, color=PALETTE["text"]),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color=PALETTE["text"]),
            ),
            margin=dict(l=50, r=50, t=60, b=60),
        )
        return fig

    @staticmethod
    def plot_fisher_importance_map(model_or_summary: Dict[str, Any]) -> go.Figure:
        """Visualizes Fisher Information Matrix parameter stiffness across layers."""
        layer_names = list(model_or_summary.keys())
        values = list(model_or_summary.values())

        fig = go.Figure(
            go.Bar(
                x=layer_names,
                y=values,
                marker=dict(
                    color=values,
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(
                        title=dict(text="Stiffness Norm", font=dict(color=PALETTE["text"])),
                        tickfont=dict(color=PALETTE["text"]),
                    ),
                ),
                text=[f"{v:.2f}" for v in values],
                textposition="auto",
            )
        )

        fig.update_layout(
            title=dict(
                text="<b>Synaptic Importance Distribution (Fisher Information Stiffness)</b>",
                font=dict(size=16, color=PALETTE["text"]),
            ),
            xaxis=dict(tickfont=dict(color=PALETTE["text"])),
            yaxis=dict(
                title="Relative Fisher Importance Score",
                gridcolor=PALETTE["border"],
                tickfont=dict(color=PALETTE["text"]),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            margin=dict(l=40, r=40, t=60, b=40),
        )
        return fig
