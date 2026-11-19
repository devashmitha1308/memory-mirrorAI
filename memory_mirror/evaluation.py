"""
Model Evaluation Engine for MemoryMirror AI.
Executes individual continual learning strategies or automated multi-strategy benchmarks.
Produces evaluation matrices, retention timelines, and exportable reports.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Callable
import time
import numpy as np
import pandas as pd

from .datasets import TaskData, DatasetManager
from .engine import ContinualMLP
from .metrics import ContinualMetrics, ForgettingAlert
from .strategies import (
    NaiveContinualLearner,
    ExperienceReplayLearner,
    EWCLearner,
    JointMultiTaskLearner,
)


@dataclass
class ExperimentResult:
    strategy_name: str
    benchmark_name: str
    task_names: List[str]
    R_matrix: np.ndarray  # Shape (T, T)
    final_avg_accuracy: float
    avg_forgetting: float
    backward_transfer: float
    task_forgetting_scores: Dict[str, float]
    alerts: List[ForgettingAlert]
    execution_time_sec: float
    weight_drift: float
    layer_drift: Dict[str, float]
    extra_info: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_name": self.strategy_name,
            "benchmark_name": self.benchmark_name,
            "task_names": self.task_names,
            "R_matrix": self.R_matrix.tolist(),
            "final_avg_accuracy": round(self.final_avg_accuracy, 2),
            "avg_forgetting": round(self.avg_forgetting, 2),
            "backward_transfer": round(self.backward_transfer, 2),
            "task_forgetting_scores": {k: round(v, 2) for k, v in self.task_forgetting_scores.items()},
            "alerts": [
                {
                    "task": a.task_name,
                    "stage": a.stage_name,
                    "peak_acc": round(a.peak_accuracy, 1),
                    "curr_acc": round(a.current_accuracy, 1),
                    "drop": round(a.drop, 1),
                    "severity": a.severity,
                    "message": a.message,
                }
                for a in self.alerts
            ],
            "execution_time_sec": round(self.execution_time_sec, 3),
            "weight_drift": round(self.weight_drift, 3),
            "layer_drift": self.layer_drift,
        }

    def to_dataframe(self) -> pd.DataFrame:
        """Returns R matrix as a clean Pandas DataFrame."""
        return pd.DataFrame(
            self.R_matrix,
            index=[f"Trained on {name}" for name in self.task_names],
            columns=[f"Eval {name}" for name in self.task_names],
        )


class EvaluationEngine:
    """Orchestrates continual learning training and quantitative evaluation."""

    @staticmethod
    def run_strategy(
        strategy_type: str,
        tasks: List[TaskData],
        benchmark_name: str,
        hidden_dim: int = 64,
        epochs_per_task: int = 15,
        batch_size: int = 32,
        lr: float = 0.005,
        ewc_lambda: float = 800.0,
        buffer_size: int = 60,
        random_state: int = 42,
        on_progress: Optional[Callable[[int, int, float], None]] = None,
    ) -> ExperimentResult:
        """Executes a single continual learning strategy on the task sequence."""
        t0 = time.time()
        input_dim = tasks[0].input_dim
        num_classes = tasks[0].num_classes
        task_names = [t.name for t in tasks]

        # Initialize fresh continual neural network
        model = ContinualMLP(
            layer_sizes=[input_dim, hidden_dim, hidden_dim // 2, num_classes],
            learning_rate=lr,
            random_state=random_state,
        )

        extra_info = {}

        if strategy_type == "Naive":
            learner = NaiveContinualLearner(model, epochs_per_task, batch_size)
        elif strategy_type == "Replay":
            learner = ExperienceReplayLearner(
                model,
                buffer_size_per_task=buffer_size,
                epochs_per_task=epochs_per_task,
                batch_size=batch_size,
            )
        elif strategy_type == "EWC":
            learner = EWCLearner(
                model,
                ewc_lambda=ewc_lambda,
                epochs_per_task=epochs_per_task,
                batch_size=batch_size,
            )
        elif strategy_type == "Joint":
            learner = JointMultiTaskLearner(
                model,
                total_epochs=epochs_per_task * len(tasks),
                batch_size=batch_size,
            )
        else:
            learner = NaiveContinualLearner(model, epochs_per_task, batch_size)

        # Train across task sequence
        R = learner.train_task_sequence(tasks, on_epoch_end=on_progress)
        elapsed = time.time() - t0

        # Compute continual learning metrics
        final_avg_acc = ContinualMetrics.calculate_average_accuracy(R)
        avg_forgetting = ContinualMetrics.calculate_average_forgetting(R)
        bwt = ContinualMetrics.calculate_backward_transfer(R)

        task_forgetting_scores = {}
        for j in range(len(tasks)):
            score = ContinualMetrics.calculate_task_forgetting(R, j)
            task_forgetting_scores[task_names[j]] = score

        alerts = ContinualMetrics.detect_forgetting_events(R, task_names)

        # Weight drift metrics
        weight_drift = model.get_weight_drift(initial_checkpoint_task=0)
        layer_drift = model.get_layer_drift_summary(baseline_task=0)

        if hasattr(learner, "get_buffer_summary"):
            extra_info["replay_buffer"] = learner.get_buffer_summary()
        if hasattr(learner, "get_fisher_importance_summary"):
            extra_info["fisher_summary"] = learner.get_fisher_importance_summary()

        return ExperimentResult(
            strategy_name=learner.strategy_name,
            benchmark_name=benchmark_name,
            task_names=task_names,
            R_matrix=R,
            final_avg_accuracy=final_avg_acc,
            avg_forgetting=avg_forgetting,
            backward_transfer=bwt,
            task_forgetting_scores=task_forgetting_scores,
            alerts=alerts,
            execution_time_sec=elapsed,
            weight_drift=weight_drift,
            layer_drift=layer_drift,
            extra_info=extra_info,
        )

    @staticmethod
    def run_all_comparative_benchmark(
        tasks: List[TaskData],
        benchmark_name: str,
        hidden_dim: int = 64,
        epochs_per_task: int = 15,
        batch_size: int = 32,
        lr: float = 0.005,
        ewc_lambda: float = 800.0,
        buffer_size: int = 60,
        random_state: int = 42,
    ) -> Dict[str, ExperimentResult]:
        """Runs all 4 strategies in parallel for rigorous head-to-head comparison."""
        results = {}
        strategies = ["Naive", "Replay", "EWC", "Joint"]

        for strat in strategies:
            res = EvaluationEngine.run_strategy(
                strategy_type=strat,
                tasks=tasks,
                benchmark_name=benchmark_name,
                hidden_dim=hidden_dim,
                epochs_per_task=epochs_per_task,
                batch_size=batch_size,
                lr=lr,
                ewc_lambda=ewc_lambda,
                buffer_size=buffer_size,
                random_state=random_state,
            )
            results[strat] = res

        return results
