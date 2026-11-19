"""
Naive Sequential Fine-Tuning Strategy (Baseline).
Trains continuously on new tasks without preservation mechanisms.
Exhibits standard catastrophic forgetting.
"""

from typing import List, Dict, Any, Callable, Optional
import numpy as np
from ..engine import ContinualMLP
from ..datasets import TaskData


class NaiveContinualLearner:
    """Standard sequential training without memory retention mechanisms."""

    def __init__(
        self,
        model: ContinualMLP,
        epochs_per_task: int = 15,
        batch_size: int = 32,
    ):
        self.model = model
        self.epochs = epochs_per_task
        self.batch_size = batch_size
        self.strategy_name = "Naive Fine-Tuning (No Preservation)"

    def train_task_sequence(
        self,
        tasks: List[TaskData],
        on_epoch_end: Optional[Callable[[int, int, float], None]] = None,
    ) -> np.ndarray:
        """
        Trains model sequentially across tasks.
        Returns accuracy matrix R of shape (T, T):
        R[i, j] = accuracy on task j after training on task i.
        """
        num_tasks = len(tasks)
        R = np.zeros((num_tasks, num_tasks))

        for task_idx, current_task in enumerate(tasks):
            X_tr, y_tr = current_task.X_train, current_task.y_train
            n_samples = len(X_tr)

            # Train on current task
            for epoch in range(self.epochs):
                perm = np.random.permutation(n_samples)
                epoch_loss = 0.0
                batches = 0

                for b_start in range(0, n_samples, self.batch_size):
                    batch_idx = perm[b_start : b_start + self.batch_size]
                    xb = X_tr[batch_idx]
                    yb = y_tr[batch_idx]

                    grad_w, grad_b, loss = self.model.compute_gradients(
                        xb, yb, allowed_classes=current_task.classes, ewc_lambda=0.0
                    )
                    self.model.apply_gradients(grad_w, grad_b)
                    epoch_loss += loss
                    batches += 1

                avg_loss = epoch_loss / max(1, batches)
                if on_epoch_end:
                    on_epoch_end(task_idx, epoch, avg_loss)

            # Save checkpoint
            self.model.save_checkpoint(task_idx)

            # Evaluate on ALL tasks seen so far
            for eval_idx, eval_task in enumerate(tasks):
                acc, _ = self.model.evaluate(
                    eval_task.X_test, eval_task.y_test, allowed_classes=eval_task.classes
                )
                R[task_idx, eval_idx] = acc

        return R
