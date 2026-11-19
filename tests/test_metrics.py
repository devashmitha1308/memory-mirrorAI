"""
Unit tests for ContinualMetrics calculation engine.
"""

import os
import sys
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from memory_mirror.metrics import ContinualMetrics


class TestContinualMetrics(unittest.TestCase):
    def test_metrics_calculations(self):
        # Synthetic R matrix (2 tasks, exactly like slide mockup)
        # Stage 1: Learn Task A -> Task A = 95%, Task B = 0%
        # Stage 2: Learn Task B -> Task A = 60%, Task B = 93%
        R = np.array([
            [95.0, 0.0],
            [60.0, 93.0],
        ])

        # 1. Forgetting for Task A: 95 - 60 = 35 pts
        forgetting_A = ContinualMetrics.calculate_task_forgetting(R, task_id=0, stage=1)
        self.assertTrue(np.isclose(forgetting_A, 35.0))

        # 2. Average Accuracy at stage 2: (60 + 93) / 2 = 76.5%
        avg_acc = ContinualMetrics.calculate_average_accuracy(R, stage=1)
        self.assertTrue(np.isclose(avg_acc, 76.5))

        # 3. Backward Transfer: R[1, 0] - R[0, 0] = 60 - 95 = -35.0 pts
        bwt = ContinualMetrics.calculate_backward_transfer(R)
        self.assertTrue(np.isclose(bwt, -35.0))

        # 4. Event detection
        alerts = ContinualMetrics.detect_forgetting_events(R, ["Task A", "Task B"], critical_threshold=25.0)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].severity, "CRITICAL")
        self.assertEqual(alerts[0].drop, 35.0)


if __name__ == "__main__":
    unittest.main()
