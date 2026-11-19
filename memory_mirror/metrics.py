"""
Forgetting Detection Engine & Metrics Calculator for MemoryMirror AI.
Implements standard Continual Learning metrics:
- Task-wise Forgetting Score (Best Past Score - Current Score)
- Average Accuracy (A)
- Average Forgetting Measure (F)
- Backward Transfer (BWT)
- Catastrophic Forgetting Event Alerts
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import numpy as np


@dataclass
class ForgettingAlert:
    task_id: int
    task_name: str
    stage_id: int
    stage_name: str
    peak_accuracy: float
    current_accuracy: float
    drop: float
    severity: str  # "CRITICAL", "HIGH", "MODERATE", "STABLE", "POSITIVE_TRANSFER"
    message: str


class ContinualMetrics:
    """
    Computes retention and forgetting metrics from the R matrix.
    R[i, j] represents accuracy on Task j after completing training on Task i.
    """

    @staticmethod
    def calculate_task_forgetting(
        R: np.ndarray,
        task_id: int,
        stage: Optional[int] = None,
    ) -> float:
        """
        Calculates forgetting for task_id at a specific stage (or final stage):
        f_j^k = max_{l < k} R[l, j] - R[k, j]
        """
        if stage is None:
            stage = R.shape[0] - 1

        if stage <= task_id:
            return 0.0  # Cannot forget before or during initial training

        peak_acc = np.max(R[:stage, task_id])
        current_acc = R[stage, task_id]
        forgetting = max(0.0, peak_acc - current_acc)
        return float(forgetting)

    @staticmethod
    def calculate_average_accuracy(R: np.ndarray, stage: Optional[int] = None) -> float:
        """
        Average Accuracy across all tasks learned up to stage k:
        A_k = (1 / (k + 1)) * sum_{j=0}^k R[k, j]
        """
        if stage is None:
            stage = R.shape[0] - 1
        num_tasks_seen = stage + 1
        return float(np.mean(R[stage, :num_tasks_seen]))

    @staticmethod
    def calculate_average_forgetting(R: np.ndarray, stage: Optional[int] = None) -> float:
        """
        Average Forgetting measure across all previously learned tasks:
        F_k = (1 / k) * sum_{j=0}^{k-1} f_j^k
        """
        if stage is None:
            stage = R.shape[0] - 1

        if stage == 0:
            return 0.0

        forgetting_list = [
            ContinualMetrics.calculate_task_forgetting(R, j, stage)
            for j in range(stage)
        ]
        return float(np.mean(forgetting_list))

    @staticmethod
    def calculate_backward_transfer(R: np.ndarray) -> float:
        """
        Backward Transfer (BWT):
        BWT = (1 / (T - 1)) * sum_{j=0}^{T-2} (R[T-1, j] - R[j, j])
        Negative values indicate catastrophic forgetting.
        Positive values indicate backward transfer (learning new tasks improved old tasks).
        """
        T = R.shape[0]
        if T <= 1:
            return 0.0

        bwt_values = [R[T - 1, j] - R[j, j] for j in range(T - 1)]
        return float(np.mean(bwt_values))

    @staticmethod
    def detect_forgetting_events(
        R: np.ndarray,
        task_names: List[str],
        critical_threshold: float = 25.0,
        warning_threshold: float = 12.0,
    ) -> List[ForgettingAlert]:
        """
        Scans matrix R across all sequential stages to detect catastrophic forgetting events.
        """
        alerts = []
        T = R.shape[0]

        for stage in range(1, T):
            stage_name = task_names[stage] if stage < len(task_names) else f"Stage {stage + 1}"
            for task_id in range(stage):
                task_name = task_names[task_id] if task_id < len(task_names) else f"Task {task_id + 1}"
                peak_acc = float(np.max(R[:stage, task_id]))
                curr_acc = float(R[stage, task_id])
                drop = peak_acc - curr_acc

                if drop >= critical_threshold:
                    severity = "CRITICAL"
                    msg = (
                        f"🚨 Catastrophic Forgetting Detected! {task_name} plummeted from "
                        f"{peak_acc:.1f}% to {curr_acc:.1f}% (Loss of {drop:.1f} pts) "
                        f"immediately after learning {stage_name}."
                    )
                elif drop >= warning_threshold:
                    severity = "HIGH"
                    msg = (
                        f"⚠️ Significant Knowledge Degradation: {task_name} decreased by {drop:.1f} pts "
                        f"(from {peak_acc:.1f}% to {curr_acc:.1f}%) during {stage_name}."
                    )
                elif drop > 3.0:
                    severity = "MODERATE"
                    msg = (
                        f"ℹ️ Minor Memory Drift: {task_name} slipped by {drop:.1f} pts "
                        f"(now {curr_acc:.1f}%)."
                    )
                elif drop <= -2.0:
                    severity = "POSITIVE_TRANSFER"
                    msg = (
                        f"✨ Positive Backward Transfer! {task_name} accuracy boosted by "
                        f"{abs(drop):.1f} pts (now {curr_acc:.1f}%)."
                    )
                else:
                    severity = "STABLE"
                    msg = f"✅ Stable Memory: {task_name} retained {curr_acc:.1f}% accuracy."

                if severity in ["CRITICAL", "HIGH", "MODERATE", "POSITIVE_TRANSFER"]:
                    alerts.append(
                        ForgettingAlert(
                            task_id=task_id,
                            task_name=task_name,
                            stage_id=stage,
                            stage_name=stage_name,
                            peak_accuracy=peak_acc,
                            current_accuracy=curr_acc,
                            drop=drop,
                            severity=severity,
                            message=msg,
                        )
                    )

        return alerts
