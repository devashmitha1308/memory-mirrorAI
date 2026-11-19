"""
Experience Replay Strategy (Memory Buffer Rehearsal).
Maintains a reservoir memory of exemplar samples from past tasks
and interleaves them during gradient updates on subsequent tasks.
"""

from typing import List, Dict, Any, Callable, Optional, Tuple
import numpy as np
from ..engine import ContinualMLP
from ..datasets import TaskData


class ExperienceReplayLearner:
    """Continual learner equipped with an episodic replay buffer."""

    def __init__(
        self,
        model: ContinualMLP,
        buffer_size_per_task: int = 50,
        epochs_per_task: int = 15,
        batch_size: int = 32,
        replay_ratio: float = 0.5,
    ):
        self.model = model
        self.buffer_size_per_task = buffer_size_per_task
        self.epochs = epochs_per_task
        self.batch_size = batch_size
        self.replay_ratio = replay_ratio
        self.strategy_name = "Experience Replay (Memory Rehearsal)"

        # Memory buffer: stores (X_sample, y_sample, task_id)
        self.buffer_X: List[np.ndarray] = []
        self.buffer_y: List[int] = []
        self.buffer_task: List[int] = []

    def _update_buffer(self, task_idx: int, task: TaskData):
        """Populates replay buffer with balanced exemplar samples from current task."""
        classes = task.classes
        samples_per_class = max(1, self.buffer_size_per_task // len(classes))

        for c in classes:
            c_indices = np.where(task.y_train == c)[0]
            if len(c_indices) > 0:
                selected = np.random.choice(
                    c_indices,
                    size=min(len(c_indices), samples_per_class),
                    replace=False,
                )
                for idx in selected:
                    self.buffer_X.append(task.X_train[idx])
                    self.buffer_y.append(int(task.y_train[idx]))
                    self.buffer_task.append(task_idx)

    def train_task_sequence(
        self,
        tasks: List[TaskData],
        on_epoch_end: Optional[Callable[[int, int, float], None]] = None,
    ) -> np.ndarray:
        """Trains sequentially with rehearsal replay on previous exemplars."""
        num_tasks = len(tasks)
        R = np.zeros((num_tasks, num_tasks))
        seen_classes = []

        for task_idx, current_task in enumerate(tasks):
            seen_classes = sorted(list(set(seen_classes + current_task.classes)))
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

                    # If replay buffer has memories from earlier tasks, blend them in
                    if len(self.buffer_X) > 0 and task_idx > 0:
                        replay_count = int(len(xb) * self.replay_ratio)
                        if replay_count > 0:
                            buf_indices = np.random.choice(len(self.buffer_X), size=replay_count, replace=True)
                            x_buf = np.array([self.buffer_X[i] for i in buf_indices])
                            y_buf = np.array([self.buffer_y[i] for i in buf_indices])

                            xb = np.vstack([xb, x_buf])
                            yb = np.concatenate([yb, y_buf])

                    grad_w, grad_b, loss = self.model.compute_gradients(
                        xb, yb, allowed_classes=seen_classes, ewc_lambda=0.0
                    )
                    self.model.apply_gradients(grad_w, grad_b)
                    epoch_loss += loss
                    batches += 1

                avg_loss = epoch_loss / max(1, batches)
                if on_epoch_end:
                    on_epoch_end(task_idx, epoch, avg_loss)

            # Store exemplars into memory mirror buffer
            self._update_buffer(task_idx, current_task)
            self.model.save_checkpoint(task_idx)

            # Evaluate across all tasks
            for eval_idx, eval_task in enumerate(tasks):
                acc, _ = self.model.evaluate(
                    eval_task.X_test, eval_task.y_test, allowed_classes=eval_task.classes
                )
                R[task_idx, eval_idx] = acc

        return R

    def get_buffer_summary(self) -> Dict[str, Any]:
        """Returns statistics of the current memory mirror buffer."""
        return {
            "total_exemplars": len(self.buffer_X),
            "classes_retained": sorted(list(set(self.buffer_y))),
            "task_distribution": {
                f"Task {t + 1}": self.buffer_task.count(t)
                for t in sorted(list(set(self.buffer_task)))
            },
        }
