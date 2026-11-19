"""
Unit tests for preservation strategies and evaluation pipeline.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from memory_mirror.datasets import DatasetManager
from memory_mirror.evaluation import EvaluationEngine


class TestContinualStrategies(unittest.TestCase):
    def test_strategies_execution(self):
        tasks = DatasetManager.load_task_sequence("Split MNIST Digits (2 Tasks: 0-4 vs 5-9)")
        self.assertEqual(len(tasks), 2)

        # Run Naive
        res_naive = EvaluationEngine.run_strategy(
            "Naive", tasks, "Test Benchmark", hidden_dim=32, epochs_per_task=4, batch_size=64
        )
        self.assertEqual(res_naive.R_matrix.shape, (2, 2))
        self.assertGreaterEqual(res_naive.final_avg_accuracy, 0)

        # Run Replay
        res_replay = EvaluationEngine.run_strategy(
            "Replay", tasks, "Test Benchmark", hidden_dim=32, epochs_per_task=4, batch_size=64, buffer_size=20
        )
        self.assertEqual(res_replay.R_matrix.shape, (2, 2))
        self.assertIn("replay_buffer", res_replay.extra_info)

        # Run EWC
        res_ewc = EvaluationEngine.run_strategy(
            "EWC", tasks, "Test Benchmark", hidden_dim=32, epochs_per_task=4, batch_size=64, ewc_lambda=500.0
        )
        self.assertEqual(res_ewc.R_matrix.shape, (2, 2))
        self.assertIn("fisher_summary", res_ewc.extra_info)


if __name__ == "__main__":
    unittest.main()
