"""
Dataset Manager Module for MemoryMirror AI
Handles continuous dataset streaming, task partitioning, and sequential split generation.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


@dataclass
class TaskData:
    task_id: int
    name: str
    description: str
    classes: List[int]
    X_train: np.ndarray
    y_train: np.ndarray
    X_test: np.ndarray
    y_test: np.ndarray
    input_dim: int
    num_classes: int
    sample_images: Dict[int, np.ndarray]  # One representative image per class for preview

    @property
    def train_size(self) -> int:
        return len(self.X_train)

    @property
    def test_size(self) -> int:
        return len(self.X_test)


class DatasetManager:
    """
    Manages benchmarks for continual learning evaluation.
    Provides standard sequential tasks such as Split MNIST (Digits 0-4 vs 5-9)
    and 5-Task Incremental Digits.
    """

    AVAILABLE_DATASETS = [
        "Split MNIST Digits (2 Tasks: 0-4 vs 5-9)",
        "Incremental Digits (5 Tasks: 2 Digits Each)",
        "Continual Sensory Shifts (3 Tasks)",
        "Synthetic Non-Stationary Drift (4 Tasks)",
    ]

    @staticmethod
    def load_task_sequence(
        benchmark_name: str = "Split MNIST Digits (2 Tasks: 0-4 vs 5-9)",
        test_size: float = 0.25,
        random_state: int = 42,
    ) -> List[TaskData]:
        """Loads and partitions a benchmark into an ordered sequence of tasks."""
        if benchmark_name.startswith("Split MNIST Digits"):
            return DatasetManager._create_split_mnist_2tasks(test_size, random_state)
        elif benchmark_name.startswith("Incremental Digits"):
            return DatasetManager._create_split_mnist_5tasks(test_size, random_state)
        elif benchmark_name.startswith("Continual Sensory Shifts"):
            return DatasetManager._create_sensory_shift_tasks(test_size, random_state)
        elif benchmark_name.startswith("Synthetic Non-Stationary"):
            return DatasetManager._create_synthetic_drift_tasks(test_size, random_state)
        else:
            return DatasetManager._create_split_mnist_2tasks(test_size, random_state)

    @staticmethod
    def _create_split_mnist_2tasks(test_size: float, random_state: int) -> List[TaskData]:
        raw = load_digits()
        X = raw.data / 16.0  # Normalized to [0, 1]
        y = raw.target
        images = raw.images

        # Task A: Digits 0 to 4
        # Task B: Digits 5 to 9
        splits = [
            (0, "Task A: Digits 0–4", "Low numerical digits (0, 1, 2, 3, 4)", list(range(0, 5))),
            (1, "Task B: Digits 5–9", "High numerical digits (5, 6, 7, 8, 9)", list(range(5, 10))),
        ]

        tasks = []
        for task_id, name, desc, cls_list in splits:
            mask = np.isin(y, cls_list)
            X_task = X[mask]
            y_task = y[mask]
            img_task = images[mask]

            X_tr, X_te, y_tr, y_te, img_tr, _ = train_test_split(
                X_task, y_task, img_task, test_size=test_size, random_state=random_state, stratify=y_task
            )

            # Extract one preview image per class
            sample_imgs = {}
            for c in cls_list:
                c_idx = np.where(y_tr == c)[0]
                if len(c_idx) > 0:
                    sample_imgs[c] = img_tr[c_idx[0]]

            tasks.append(
                TaskData(
                    task_id=task_id,
                    name=name,
                    description=desc,
                    classes=cls_list,
                    X_train=X_tr,
                    y_train=y_tr,
                    X_test=X_te,
                    y_test=y_te,
                    input_dim=64,
                    num_classes=10,  # Global shared output head across all 10 digits
                    sample_images=sample_imgs,
                )
            )

        return tasks

    @staticmethod
    def _create_split_mnist_5tasks(test_size: float, random_state: int) -> List[TaskData]:
        raw = load_digits()
        X = raw.data / 16.0
        y = raw.target
        images = raw.images

        splits = [
            (0, "Task 1: Digits 0 & 1", "Binary discrimination (0 vs 1)", [0, 1]),
            (1, "Task 2: Digits 2 & 3", "Curved digits (2 vs 3)", [2, 3]),
            (2, "Task 3: Digits 4 & 5", "Middle numerals (4 vs 5)", [4, 5]),
            (3, "Task 4: Digits 6 & 7", "Loop & stroke digits (6 vs 7)", [6, 7]),
            (4, "Task 5: Digits 8 & 9", "High loop digits (8 vs 9)", [8, 9]),
        ]

        tasks = []
        for task_id, name, desc, cls_list in splits:
            mask = np.isin(y, cls_list)
            X_task = X[mask]
            y_task = y[mask]
            img_task = images[mask]

            X_tr, X_te, y_tr, y_te, img_tr, _ = train_test_split(
                X_task, y_task, img_task, test_size=test_size, random_state=random_state, stratify=y_task
            )

            sample_imgs = {}
            for c in cls_list:
                c_idx = np.where(y_tr == c)[0]
                if len(c_idx) > 0:
                    sample_imgs[c] = img_tr[c_idx[0]]

            tasks.append(
                TaskData(
                    task_id=task_id,
                    name=name,
                    description=desc,
                    classes=cls_list,
                    X_train=X_tr,
                    y_train=y_tr,
                    X_test=X_te,
                    y_test=y_te,
                    input_dim=64,
                    num_classes=10,
                    sample_images=sample_imgs,
                )
            )

        return tasks

    @staticmethod
    def _create_sensory_shift_tasks(test_size: float, random_state: int) -> List[TaskData]:
        """Tasks with non-stationary sensor transformations (Rotated & Inverted domain shifts)."""
        raw = load_digits()
        X = raw.data / 16.0
        y = raw.target
        images = raw.images

        rng = np.random.RandomState(random_state)

        # Task 1: Clean Digits (0-5)
        # Task 2: Noisy Inverted Digits (0-5)
        # Task 3: Permuted Digits (0-5)
        classes = list(range(6))
        mask = np.isin(y, classes)
        X_base = X[mask]
        y_base = y[mask]
        img_base = images[mask]

        # Shift 1: Clean
        X1 = X_base.copy()
        # Shift 2: Inverted polarity + contrast
        X2 = 1.0 - X_base + rng.normal(0, 0.05, X_base.shape)
        X2 = np.clip(X2, 0, 1)
        # Shift 3: Scrambled pixel permutation
        perm = rng.permutation(64)
        X3 = X_base[:, perm]

        shifts = [
            (0, "Stage 1: Clean Sensor Intake", "Original calibrated image distribution (Classes 0-5)", X1),
            (1, "Stage 2: Sensor Inversion & Noise", "High-exposure contrast shift with ambient noise", X2),
            (2, "Stage 3: Spatial Channel Permutation", "Misaligned sensor spatial wiring permutation", X3),
        ]

        tasks = []
        for task_id, name, desc, X_data in shifts:
            X_tr, X_te, y_tr, y_te, img_tr, _ = train_test_split(
                X_data, y_base, img_base, test_size=test_size, random_state=random_state, stratify=y_base
            )
            sample_imgs = {}
            for c in classes:
                c_idx = np.where(y_tr == c)[0]
                if len(c_idx) > 0:
                    sample_imgs[c] = img_tr[c_idx[0]]

            tasks.append(
                TaskData(
                    task_id=task_id,
                    name=name,
                    description=desc,
                    classes=classes,
                    X_train=X_tr,
                    y_train=y_tr,
                    X_test=X_te,
                    y_test=y_te,
                    input_dim=64,
                    num_classes=6,
                    sample_images=sample_imgs,
                )
            )

        return tasks

    @staticmethod
    def _create_synthetic_drift_tasks(test_size: float, random_state: int) -> List[TaskData]:
        """Synthetic multimodal streaming tasks with rotating class manifolds."""
        rng = np.random.RandomState(random_state)
        n_samples_per_task = 400
        n_features = 32
        n_classes = 4

        tasks = []
        for task_id in range(4):
            angle = task_id * (np.pi / 4.0)
            centers = []
            for c in range(n_classes):
                c_angle = angle + c * (2 * np.pi / n_classes)
                center = np.zeros(n_features)
                center[0] = 3.0 * np.cos(c_angle)
                center[1] = 3.0 * np.sin(c_angle)
                center[2:] = rng.normal(0, 0.5, n_features - 2)
                centers.append(center)

            X_list, y_list = [], []
            for c, center in enumerate(centers):
                samples = rng.normal(loc=center, scale=0.8, size=(n_samples_per_task // n_classes, n_features))
                X_list.append(samples)
                y_list.append(np.full(len(samples), c))

            X_all = np.vstack(X_list)
            y_all = np.concatenate(y_list)

            X_tr, X_te, y_tr, y_te = train_test_split(
                X_all, y_all, test_size=test_size, random_state=random_state, stratify=y_all
            )

            # Synthetic pseudo-image for visualizer (8x4 reshaped)
            sample_imgs = {}
            for c in range(n_classes):
                c_idx = np.where(y_tr == c)[0]
                if len(c_idx) > 0:
                    sample_imgs[c] = X_tr[c_idx[0]][:16].reshape((4, 4))

            tasks.append(
                TaskData(
                    task_id=task_id,
                    name=f"Subspace Task {task_id + 1}",
                    description=f"Rotated feature manifold at {int(np.degrees(angle))}° offset",
                    classes=list(range(n_classes)),
                    X_train=X_tr,
                    y_train=y_tr,
                    X_test=X_te,
                    y_test=y_te,
                    input_dim=n_features,
                    num_classes=n_classes,
                    sample_images=sample_imgs,
                )
            )

        return tasks
