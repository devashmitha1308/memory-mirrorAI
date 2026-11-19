"""
Sequential Training Engine & Neural Network Core for MemoryMirror AI.
Implements a high-performance continual learning neural network with exact gradients,
Fisher Information Matrix calculation for EWC, memory replay, and PyTorch bridge.
"""

from typing import List, Dict, Tuple, Optional
import numpy as np


class ContinualMLP:
    """
    Continual Learning Multi-Layer Perceptron.
    Supports forward inference, backprop, Adam optimization,
    weight drift tracking, and Fisher Information Matrix diagonal computation.
    """

    def __init__(
        self,
        layer_sizes: List[int],
        learning_rate: float = 0.005,
        random_state: int = 42,
    ):
        self.layer_sizes = layer_sizes
        self.lr = learning_rate
        self.rng = np.random.RandomState(random_state)

        # Initialize weights (He initialization) and biases (zeros)
        self.weights: List[np.ndarray] = []
        self.biases: List[np.ndarray] = []

        for i in range(len(layer_sizes) - 1):
            fan_in = layer_sizes[i]
            fan_out = layer_sizes[i + 1]
            limit = np.sqrt(2.0 / fan_in)
            w = self.rng.randn(fan_in, fan_out) * limit
            b = np.zeros((1, fan_out))
            self.weights.append(w)
            self.biases.append(b)

        # Adam optimizer state
        self.m_w = [np.zeros_like(w) for w in self.weights]
        self.v_w = [np.zeros_like(w) for w in self.weights]
        self.m_b = [np.zeros_like(b) for b in self.biases]
        self.v_b = [np.zeros_like(b) for b in self.biases]
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.eps = 1e-8
        self.t_step = 0

        # Snapshot of optimal parameters after each task: task_id -> (weights, biases)
        self.task_checkpoints: Dict[int, Tuple[List[np.ndarray], List[np.ndarray]]] = {}
        # Fisher Information Matrix diagonals: task_id -> (fisher_w, fisher_b)
        self.task_fishers: Dict[int, Tuple[List[np.ndarray], List[np.ndarray]]] = {}

    def forward(
        self,
        X: np.ndarray,
        allowed_classes: Optional[List[int]] = None,
    ) -> Tuple[np.ndarray, List[np.ndarray], List[np.ndarray]]:
        """Computes activations and returns (probabilities, hidden_activations, pre_activations)."""
        activations = [X]
        pre_activations = []

        curr = X
        for i in range(len(self.weights) - 1):
            z = np.dot(curr, self.weights[i]) + self.biases[i]
            pre_activations.append(z)
            curr = np.maximum(0, z)  # ReLU
            activations.append(curr)

        # Output layer
        z_out = np.dot(curr, self.weights[-1]) + self.biases[-1]
        pre_activations.append(z_out)

        # If evaluating in Task-IL mode, mask out classes not in this task
        if allowed_classes is not None:
            mask = np.ones(z_out.shape[1], dtype=bool)
            mask[allowed_classes] = False
            z_out = z_out.copy()
            z_out[:, mask] = -1e9

        exp_z = np.exp(z_out - np.max(z_out, axis=1, keepdims=True))
        probs = exp_z / (np.sum(exp_z, axis=1, keepdims=True) + 1e-12)
        activations.append(probs)

        return probs, activations, pre_activations

    def predict(self, X: np.ndarray, allowed_classes: Optional[List[int]] = None) -> np.ndarray:
        """Returns predicted class indices."""
        probs, _, _ = self.forward(X, allowed_classes=allowed_classes)
        return np.argmax(probs, axis=1)

    def evaluate(
        self,
        X: np.ndarray,
        y: np.ndarray,
        allowed_classes: Optional[List[int]] = None,
    ) -> Tuple[float, float]:
        """Calculates (accuracy, cross_entropy_loss)."""
        if len(X) == 0:
            return 0.0, 0.0
        probs, _, _ = self.forward(X, allowed_classes=allowed_classes)
        preds = np.argmax(probs, axis=1)
        acc = float(np.mean(preds == y)) * 100.0

        # Categorical cross entropy
        one_hot = np.zeros_like(probs)
        one_hot[np.arange(len(y)), y] = 1.0
        loss = -float(np.mean(np.sum(one_hot * np.log(probs + 1e-12), axis=1)))
        return acc, loss

    def compute_gradients(
        self,
        X: np.ndarray,
        y: np.ndarray,
        allowed_classes: Optional[List[int]] = None,
        ewc_lambda: float = 0.0,
    ) -> Tuple[List[np.ndarray], List[np.ndarray], float]:
        """
        Computes gradients of Cross Entropy loss + optional EWC quadratic penalty.
        dL/dTheta = dCE/dTheta + lambda * sum_k [ F_k * (Theta - Theta_k*) ]
        """
        n_samples = X.shape[0]
        probs, activations, pre_activations = self.forward(X, allowed_classes=allowed_classes)

        # Compute Cross Entropy Loss
        one_hot = np.zeros_like(probs)
        one_hot[np.arange(n_samples), y] = 1.0
        ce_loss = -float(np.mean(np.sum(one_hot * np.log(probs + 1e-12), axis=1)))

        grad_w = [np.zeros_like(w) for w in self.weights]
        grad_b = [np.zeros_like(b) for b in self.biases]

        # Output layer gradient: (P - Y) / N
        delta = (probs - one_hot) / n_samples
        if allowed_classes is not None:
            mask = np.ones(probs.shape[1], dtype=bool)
            mask[allowed_classes] = False
            delta[:, mask] = 0.0

        grad_w[-1] = np.dot(activations[-2].T, delta)
        grad_b[-1] = np.sum(delta, axis=0, keepdims=True)

        # Backprop through hidden layers
        for layer in range(len(self.weights) - 2, -1, -1):
            delta = np.dot(delta, self.weights[layer + 1].T)
            # ReLU derivative
            delta = delta * (pre_activations[layer] > 0)
            grad_w[layer] = np.dot(activations[layer].T, delta)
            grad_b[layer] = np.sum(delta, axis=0, keepdims=True)

        total_loss = ce_loss

        # Apply EWC regularizer penalty and gradient if active
        if ewc_lambda > 0.0 and len(self.task_fishers) > 0:
            ewc_loss_val = 0.0
            for task_id, (f_w_list, f_b_list) in self.task_fishers.items():
                w_star_list, b_star_list = self.task_checkpoints[task_id]
                for l in range(len(self.weights)):
                    diff_w = self.weights[l] - w_star_list[l]
                    diff_b = self.biases[l] - b_star_list[l]

                    # Quadratic penalty: 0.5 * lambda * F * (theta - theta*)^2
                    ewc_loss_val += 0.5 * ewc_lambda * np.sum(f_w_list[l] * (diff_w ** 2))
                    ewc_loss_val += 0.5 * ewc_lambda * np.sum(f_b_list[l] * (diff_b ** 2))

                    # Gradient: lambda * F * (theta - theta*)
                    grad_w[l] += ewc_lambda * (f_w_list[l] * diff_w)
                    grad_b[l] += ewc_lambda * (f_b_list[l] * diff_b)

            total_loss += ewc_loss_val

        return grad_w, grad_b, total_loss

    def apply_gradients(self, grad_w: List[np.ndarray], grad_b: List[np.ndarray]):
        """Updates parameters using Adam optimizer."""
        self.t_step += 1
        lr_t = self.lr * np.sqrt(1.0 - self.beta2 ** self.t_step) / (1.0 - self.beta1 ** self.t_step)

        for i in range(len(self.weights)):
            # Weight update
            self.m_w[i] = self.beta1 * self.m_w[i] + (1.0 - self.beta1) * grad_w[i]
            self.v_w[i] = self.beta2 * self.v_w[i] + (1.0 - self.beta2) * (grad_w[i] ** 2)
            self.weights[i] -= lr_t * self.m_w[i] / (np.sqrt(self.v_w[i]) + self.eps)

            # Bias update
            self.m_b[i] = self.beta1 * self.m_b[i] + (1.0 - self.beta1) * grad_b[i]
            self.v_b[i] = self.beta2 * self.v_b[i] + (1.0 - self.beta2) * (grad_b[i] ** 2)
            self.biases[i] -= lr_t * self.m_b[i] / (np.sqrt(self.v_b[i]) + self.eps)

    def compute_fisher_information(
        self,
        X: np.ndarray,
        y: np.ndarray,
        allowed_classes: Optional[List[int]] = None,
        num_samples: int = 300,
    ) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Estimates the diagonal elements of the Fisher Information Matrix (FIM) for Task t:
        F_i = (1 / N) * sum_n [ (d log p(y_n | x_n) / d theta_i)^2 ]
        """
        n = min(len(X), num_samples)
        indices = np.random.choice(len(X), size=n, replace=False)

        fisher_w = [np.zeros_like(w) for w in self.weights]
        fisher_b = [np.zeros_like(b) for b in self.biases]

        for idx in indices:
            x_single = X[idx:idx + 1]
            y_single = y[idx:idx + 1]

            probs, acts, pre_acts = self.forward(x_single, allowed_classes=allowed_classes)
            # Derivative of log p(y | x)
            one_hot = np.zeros_like(probs)
            one_hot[0, y_single[0]] = 1.0

            # For log-likelihood, gradient w.r.t logits is (y - p)
            delta = probs - one_hot
            if allowed_classes is not None:
                mask = np.ones(probs.shape[1], dtype=bool)
                mask[allowed_classes] = False
                delta[:, mask] = 0.0

            # Output layer
            gw = np.dot(acts[-2].T, delta)
            gb = np.copy(delta)
            fisher_w[-1] += (gw ** 2)
            fisher_b[-1] += (gb ** 2)

            # Backprop for hidden layers
            for l in range(len(self.weights) - 2, -1, -1):
                delta = np.dot(delta, self.weights[l + 1].T) * (pre_acts[l] > 0)
                gw = np.dot(acts[l].T, delta)
                gb = np.sum(delta, axis=0, keepdims=True)
                fisher_w[l] += (gw ** 2)
                fisher_b[l] += (gb ** 2)

        # Normalize by sample count
        fisher_w = [fw / n for fw in fisher_w]
        fisher_b = [fb / n for fb in fisher_b]

        return fisher_w, fisher_b

    def save_checkpoint(self, task_id: int):
        """Saves optimal weight parameters theta* after completing task_id."""
        self.task_checkpoints[task_id] = (
            [w.copy() for w in self.weights],
            [b.copy() for b in self.biases],
        )

    def register_fisher(self, task_id: int, fisher_w: List[np.ndarray], fisher_b: List[np.ndarray]):
        """Registers Fisher Information Matrix diagonal for task_id."""
        self.task_fishers[task_id] = (fisher_w, fisher_b)

    def get_weight_drift(self, initial_checkpoint_task: int = 0) -> float:
        """Calculates Frobenius norm distance from initial task weights."""
        if initial_checkpoint_task not in self.task_checkpoints:
            return 0.0
        init_w, _ = self.task_checkpoints[initial_checkpoint_task]
        total_sq_diff = 0.0
        for w_curr, w_init in zip(self.weights, init_w):
            total_sq_diff += np.sum((w_curr - w_init) ** 2)
        return float(np.sqrt(total_sq_diff))

    def get_layer_drift_summary(self, baseline_task: int = 0) -> Dict[str, float]:
        """Returns per-layer relative weight drift."""
        if baseline_task not in self.task_checkpoints:
            return {}
        init_w, _ = self.task_checkpoints[baseline_task]
        summary = {}
        for idx, (w_c, w_0) in enumerate(zip(self.weights, init_w)):
            drift = np.linalg.norm(w_c - w_0) / (np.linalg.norm(w_0) + 1e-8)
            summary[f"Layer {idx + 1} (W: {w_c.shape[0]}x{w_c.shape[1]})"] = float(drift * 100.0)
        return summary
