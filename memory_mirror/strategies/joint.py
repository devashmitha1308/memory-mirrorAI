"""
Joint Multi-Task Training Strategy (Upper Bound Oracle).
Trains on all tasks simultaneously to provide the multi-task upper bound baseline.
"""

from typing import List, Dict, Any, Callable, Optional
import numpy as np
from ..engine import ContinualMLP
from ..datasets import TaskData


class JointMultiTaskLearner:
    """Multi-task learning oracle benchmark."""

    def __init__(
        self,
        model: ContinualMLP,
        total_epochs: int = 25,
        batch_size: int = 32,
    ):
        self.model = model
        self.total_epochs = total_epochs
        self.batch_size = batch_size
        self.strategy_name = "Joint Multi-Task (Upper Bound Oracle)"

    def train_task_sequence(
        self,
        tasks: List[TaskData],
        on_epoch_end: Optional[Callable[[int, int, float], None]] = None,
    ) -> np.ndarray:
        """Trains simultaneously on pooled data from all tasks."""
        num_tasks = len(tasks)
        R = np.zeros((num_tasks, num_tasks))

        # Pool all task datasets together
        X_all = np.vstack([t.X_train for t in tasks])
        y_all = np.concatenate([t.y_train for t in tasks])
        n_samples = len(X_all)

        epochs_per_step = max(1, self.total_epochs // num_tasks)

        for step in range(num_tasks):
            for epoch in range(epochs_per_step):
                perm = np.random.permutation(n_samples)
                epoch_loss = 0.0
                batches = 0

                for b_start in range(0, n_samples, self.batch_size):
                    batch_idx = perm[b_start : b_start + self.batch_size]
                    xb = X_all[batch_idx]
                    yb = y_all[batch_idx]

                    grad_w, grad_b, loss = self.model.compute_gradients(xb, yb, ewc_lambda=0.0)
                    self.model.apply_gradients(grad_w, grad_b)
                    epoch_loss += loss
                    batches += 1

                avg_loss = epoch_loss / max(1, batches)
                if on_epoch_end:
                    on_epoch_end(step, epoch, avg_loss)

            self.model.save_checkpoint(step)

            # Evaluate each task
            for eval_idx, eval_task in enumerate(tasks):
                acc, _ = self.model.evaluate(
                    eval_task.X_test, eval_task.y_test, allowed_classes=eval_task.classes
                )
                R[step, eval_idx] = acc

        return R
