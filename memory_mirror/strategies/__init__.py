"""
Memory Preservation Strategies Module for MemoryMirror AI.
Includes:
- Naive Sequential Fine-Tuning (Baseline demonstrating catastrophic forgetting)
- Experience Replay (Memory buffer rehearsal)
- Elastic Weight Consolidation (EWC, Fisher Information regularization)
- Joint Multi-Task Training (Theoretical upper-bound)
"""

from .naive import NaiveContinualLearner
from .replay import ExperienceReplayLearner
from .ewc import EWCLearner
from .joint import JointMultiTaskLearner

__all__ = [
    "NaiveContinualLearner",
    "ExperienceReplayLearner",
    "EWCLearner",
    "JointMultiTaskLearner",
]
