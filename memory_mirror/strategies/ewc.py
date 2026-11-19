"""
Elastic Weight Consolidation (EWC) Strategy.
Protects crucial weights using the Fisher Information Matrix diagonal.
Kirkpatrick et al. (PNAS, 2017).
"""

from typing import List, Dict, Any, Callable, Optional
import numpy as np
from ..engine import ContinualMLP
from ..datasets import TaskData


class EWCLearner:
    """Continual learner utilizing Fisher Information regularization."""

    def __init__(
        self,
        model: ContinualMLP,
        ewc_lambda: float = 800.0,
        epochs_per_task: int = 15,
        batch_size: int = 32,
        fisher_samples: int = 250,
    ):
        self.model = model
        self.ewc_lambda = ewc_lambda
        self.epochs = epochs_per_task
        self.batch_size = batch_size
        self.fisher_samples = fisher_samples
        self.strategy_name = f"Elastic Weight Consolidation (EWC, λ={ewc_lambda})"

    def train_task_sequence(
        self,
        tasks: List[TaskData],
        on_epoch_end: Optional[Callable[[int, int, float], None]] = None,
    ) -> np.ndarray:
        """Trains sequentially while regularizing weight drift via Fisher Information."""
        num_tasks = len(tasks)
        R = np.zeros((num_tasks, num_tasks))

        for task_idx, current_task in enumerate(tasks):
            X_tr, y_tr = current_task.X_train, current_task.y_train
            n_samples = len(X_tr)

            for epoch in range(self.epochs):
                perm = np.random.permutation(n_samples)
                epoch_loss = 0.0
                batches = 0

                for b_start in range(0, n_samples, self.batch_size):
                    batch_idx = perm[b_start : b_start + self.batch_size]
                    xb = X_tr[batch_idx]
                    yb = y_tr[batch_idx]

                    # Regularize with past task Fisher matrices when task_idx > 0
                    current_lambda = self.ewc_lambda if task_idx > 0 else 0.0

                    grad_w, grad_b, loss = self.model.compute_gradients(
                        xb,
                        yb,
                        allowed_classes=current_task.classes,
                        ewc_lambda=current_lambda,
                    )
                    self.model.apply_gradients(grad_w, grad_b)
                    epoch_loss += loss
                    batches += 1

                avg_loss = epoch_loss / max(1, batches)
                if on_epoch_end:
                    on_epoch_end(task_idx, epoch, avg_loss)

            # 1. Save optimal parameter checkpoint theta*
            self.model.save_checkpoint(task_idx)

            # 2. Estimate Fisher Information Matrix diagonal for this completed task
            f_w, f_b = self.model.compute_fisher_information(
                X_tr,
                y_tr,
                allowed_classes=current_task.classes,
                num_samples=self.fisher_samples,
            )
            self.model.register_fisher(task_idx, f_w, f_b)

            # 3. Evaluate across all tasks
            for eval_idx, eval_task in enumerate(tasks):
                acc, _ = self.model.evaluate(
                    eval_task.X_test, eval_task.y_test, allowed_classes=eval_task.classes
                )
                R[task_idx, eval_idx] = acc

        return R

    def get_fisher_importance_summary(self) -> Dict[str, Any]:
        """Provides summary of parameter importance calculated across tasks."""
        summary = {}
        for task_id, (f_w, f_b) in self.model.task_fishers.items():
            total_params = sum(w.size for w in f_w) + sum(b.size for b in f_b)
            max_importance = max(float(np.max(w)) for w in f_w)
            mean_importance = float(
                np.mean([np.mean(w) for w in f_w])
            )
            summary[f"Task {task_id + 1}"] = {
                "total_parameters_protected": total_params,
                "peak_fisher_stiffness": max_importance,
                "mean_fisher_stiffness": mean_importance,
            }
        return summary
