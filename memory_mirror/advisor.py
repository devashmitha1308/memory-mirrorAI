"""
Analytical Recommendations Engine for MemoryMirror AI.
Analyzes retention dynamics, plasticity-stability trade-offs, and provides
automated, actionable recommendations to mitigate catastrophic forgetting.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from .evaluation import ExperimentResult


@dataclass
class RecommendationItem:
    category: str  # "HYPERPARAMETER", "ARCHITECTURE", "DATASET", "STRATEGY"
    priority: str  # "HIGH", "MEDIUM", "LOW"
    finding: str
    action: str
    rationale: str


class ContinualLearningAdvisor:
    """Intelligent diagnostic engine for continual learning systems."""

    @staticmethod
    def generate_diagnosis(result: ExperimentResult) -> Dict[str, Any]:
        """Performs comprehensive diagnosis of retention health and generates recommendations."""
        R = result.R_matrix
        T = R.shape[0]
        avg_f = result.avg_forgetting
        bwt = result.backward_transfer
        avg_acc = result.final_avg_accuracy

        # 1. Continual Learning Health Score (0 to 100)
        # Max score requires high accuracy, minimal forgetting, and non-negative BWT
        health_score = max(
            0.0,
            min(
                100.0,
                (avg_acc * 0.5) + ((100.0 - min(100.0, avg_f * 2.0)) * 0.35) + (max(0.0, 50.0 + bwt) * 0.15),
            ),
        )

        if health_score >= 85:
            grade = "A+ (Superior Retention)"
            status_color = "#10b981"
            diagnosis_summary = "Model exhibits excellent continual retention with minimal catastrophic interference."
        elif health_score >= 70:
            grade = "B (Moderate Retention)"
            status_color = "#3b82f6"
            diagnosis_summary = "Good general performance, but mild memory drift is observable across earlier tasks."
        elif health_score >= 50:
            grade = "C (Significant Degradation)"
            status_color = "#f59e0b"
            diagnosis_summary = "Noticeable catastrophic forgetting detected. Model loses substantial knowledge upon new learning."
        else:
            grade = "F (Catastrophic Forgetting)"
            status_color = "#ef4444"
            diagnosis_summary = "Severe catastrophic forgetting! Earlier task capabilities collapse after learning subsequent stages."

        # 2. Analyze Plasticity-Stability Trade-Off
        first_task_drop = R[0, 0] - R[-1, 0] if T > 1 else 0.0
        last_task_acc = R[-1, -1]

        if last_task_acc >= 85 and first_task_drop > 25:
            tradeoff = "Hyper-Plastic (High learning speed on new tasks, but catastrophic erasure of past memories)."
        elif last_task_acc < 65 and first_task_drop < 10:
            tradeoff = "Hyper-Rigid / Intransigent (Model is overly stiff; struggles to absorb new knowledge)."
        elif last_task_acc >= 80 and first_task_drop <= 15:
            tradeoff = "Optimal Pareto Balance (High plasticity for new tasks coupled with strong stability for past tasks)."
        else:
            tradeoff = "Suboptimal Balance (Interference across both plasticity and stability dimensions)."

        # 3. Actionable Recommendations
        recommendations: List[RecommendationItem] = []

        if avg_f > 25.0:
            recommendations.append(
                RecommendationItem(
                    category="STRATEGY",
                    priority="HIGH",
                    finding=f"Average Forgetting is {avg_f:.1f} pts, indicating critical catastrophic forgetting.",
                    action="Upgrade from Naive Fine-Tuning to Elastic Weight Consolidation (EWC) or Experience Replay.",
                    rationale="Vanilla gradient descent overwrites orthogonal task manifold directions without memory preservation.",
                )
            )

        if "Naive" in result.strategy_name and avg_f > 15.0:
            recommendations.append(
                RecommendationItem(
                    category="HYPERPARAMETER",
                    priority="HIGH",
                    finding="Unconstrained parameter drift detected.",
                    action="Activate Elastic Weight Consolidation with regularization stiffness λ between 800 and 1500.",
                    rationale="High Fisher penalty prevents key weights from drifting away from Task 1 optimal parameters.",
                )
            )

        if "EWC" in result.strategy_name:
            if avg_f > 20.0:
                recommendations.append(
                    RecommendationItem(
                        category="HYPERPARAMETER",
                        priority="HIGH",
                        finding=f"EWC regularizer still allowed {avg_f:.1f} pts of forgetting.",
                        action="Increase EWC penalty multiplier λ by 2.0x to 3.0x (e.g., from 800 to 2000).",
                        rationale="Higher stiffness prevents parameter drift on high-curvature directions of past task loss manifolds.",
                    )
                )
            elif last_task_acc < 75.0:
                recommendations.append(
                    RecommendationItem(
                        category="HYPERPARAMETER",
                        priority="MEDIUM",
                        finding="New task acquisition is constrained by excessive weight stiffness.",
                        action="Relax EWC λ parameter downwards by 30-50% to improve new task plasticity.",
                        rationale="Excessive Fisher penalty freezes synapses, preventing model capacity from absorbing new concepts.",
                    )
                )

        if "Replay" in result.strategy_name:
            recommendations.append(
                RecommendationItem(
                    category="DATASET",
                    priority="MEDIUM",
                    finding="Replay buffer rehearsal is operating.",
                    action="Use reservoir or prototype-based representative exemplar selection instead of random sampling.",
                    rationale="Selecting boundary and centroid exemplars maintains sharper classification margins for old tasks.",
                )
            )

        if result.weight_drift > 15.0:
            recommendations.append(
                RecommendationItem(
                    category="ARCHITECTURE",
                    priority="MEDIUM",
                    finding=f"Global parameter drift norm is elevated ({result.weight_drift:.2f}).",
                    action="Expand hidden layer capacity or introduce task-specific modular sub-networks / adapters.",
                    rationale="Additional parameter capacity provides dedicated orthogonal subspaces for distinct tasks.",
                )
            )

        return {
            "health_score": round(health_score, 1),
            "grade": grade,
            "status_color": status_color,
            "diagnosis_summary": diagnosis_summary,
            "plasticity_stability_tradeoff": tradeoff,
            "recommendations": recommendations,
        }
