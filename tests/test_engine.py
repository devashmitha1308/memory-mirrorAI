"""
Unit tests for ContinualMLP neural network engine.
"""

import os
import sys
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from memory_mirror.engine import ContinualMLP


class TestContinualEngine(unittest.TestCase):
    def test_mlp_forward_and_predict(self):
        mlp = ContinualMLP([8, 16, 4], learning_rate=0.01, random_state=42)
        X = np.random.randn(10, 8)
        probs, acts, pre_acts = mlp.forward(X)

        self.assertEqual(probs.shape, (10, 4))
        self.assertTrue(np.allclose(np.sum(probs, axis=1), 1.0))
        self.assertEqual(len(acts), 3)
        self.assertEqual(len(pre_acts), 2)

        preds = mlp.predict(X)
        self.assertEqual(len(preds), 10)

    def test_mlp_gradients_and_ewc(self):
        mlp = ContinualMLP([8, 16, 4], learning_rate=0.01, random_state=42)
        X = np.random.randn(20, 8)
        y = np.random.randint(0, 4, size=20)

        grad_w, grad_b, loss = mlp.compute_gradients(X, y, ewc_lambda=0.0)
        self.assertEqual(len(grad_w), 2)
        self.assertEqual(len(grad_b), 2)
        self.assertGreater(loss, 0)

        init_w0 = mlp.weights[0].copy()
        mlp.apply_gradients(grad_w, grad_b)
        self.assertFalse(np.allclose(init_w0, mlp.weights[0]))

        mlp.save_checkpoint(0)
        fw, fb = mlp.compute_fisher_information(X, y, num_samples=10)
        mlp.register_fisher(0, fw, fb)

        grad_w_ewc, _, loss_ewc = mlp.compute_gradients(X, y, ewc_lambda=500.0)
        self.assertEqual(len(grad_w_ewc), 2)


if __name__ == "__main__":
    unittest.main()
