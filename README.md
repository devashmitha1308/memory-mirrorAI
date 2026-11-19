# MemoryMirror AI 🪞

> **"Teach AI Something New, Without Making It Forget the Old."**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Charts-Plotly-3F4F75.svg)](https://plotly.com/)
[![Project](https://img.shields.io/badge/Innovation_Challenge-SparkX_3.0-purple.svg)]()

MemoryMirror AI is an intelligent continual learning and memory retention monitoring system designed to detect, measure, and prevent **catastrophic forgetting** in sequential neural network learning.

---

## 👥 Project Team & Innovation Challenge
- **Event:** SPARKX 3.0 International Project Innovation Challenge
- **Category:** Novel Product-Based Innovation
- **Team Leader:** Gauri Dwivedi
- **Team Member:** Nuka Devashmitha Reddy

---

## 🎯 The Core Problem: Catastrophic Forgetting
When an artificial intelligence model is trained sequentially on new tasks, standard gradient updates overwrite previously acquired knowledge representations. 

For instance:
1. An AI model learns to recognize digits 0–4 (Task A) with 95%+ accuracy.
2. The model is subsequently trained on digits 5–9 (Task B).
3. Upon re-testing Task A, performance degrades significantly (e.g., dropping to ~60%—a 35-point loss).

**MemoryMirror AI** continuously audits the model's knowledge retention across all past tasks at every learning milestone.

---

## 🏗️ System Architecture

```
[ Dataset Manager ]
       │  (Split Tasks: A, B, ...)
       ▼
[ Sequential Training Engine ] ◄──► [ Memory Preservation Module ]
       │                              ├── Naive Fine-Tuning
       ▼                              ├── Experience Replay (Rehearsal Buffer)
[ Model Evaluation Engine ]            ├── Elastic Weight Consolidation (EWC)
       │                              └── Joint Multi-Task Oracle
       ▼
[ Forgetting Detection Engine ]
       │  (Forgetting Score, BWT, FWT, Alerts)
       ▼
[ Interactive Analytics Dashboard & AI Advisor ]
```

### Key Modules:
1. **Dataset Manager:** Partitions datasets into sequential streams (Split MNIST 0-4 vs 5-9, 5-Task Incremental Digits, and Non-Stationary Drift benchmarks).
2. **Sequential Training Engine:** Continual multi-layer neural network with Fisher Information extraction and exact gradient optimization.
3. **Model Evaluation Engine:** Computes the comprehensive $R_{i,j}$ continual learning evaluation matrix across all stages.
4. **Forgetting Detection Engine:** 
   - $\text{Forgetting} = \text{Best Previous Accuracy} - \text{Current Accuracy}$
   - **Average Accuracy ($A_k$):** $\frac{1}{k} \sum_{j=1}^k R_{k,j}$
   - **Average Forgetting ($F_k$):** $\frac{1}{k-1} \sum_{j=1}^{k-1} f_j^k$
   - **Backward Transfer ($\text{BWT}$):** $\frac{1}{T-1} \sum_{j=1}^{T-1} (R_{T,j} - R_{j,j})$
5. **Memory Preservation Module:**
   - **Naive Fine-Tuning:** Unconstrained sequential baseline exhibiting catastrophic forgetting.
   - **Experience Replay:** Stores exemplar prototypes in an episodic memory mirror and rehearses them during subsequent task learning.
   - **Elastic Weight Consolidation (EWC):** Uses the diagonal of the Fisher Information Matrix (FIM) to shield crucial synaptic weights with quadratic stiffness.
   - **Joint Multi-Task Training:** Simultaneous co-training representing the multi-task theoretical upper bound.
6. **Analytics Dashboard & AI Advisor:** Interactive Streamlit web interface featuring retention timelines, degradation waterfalls, Fisher stiffness heatmaps, and prescriptive diagnostic guidance.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed.

### 2. Clone Repository
```bash
git clone https://github.com/devashmitha/memory-mirror-ai.git
cd memory-mirror-ai
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Interactive Web Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 5. Run CLI Benchmark & Verification
```bash
python run_demo.py
```

### 6. Run Automated Test Suite
```bash
python -m unittest discover tests
```

---

## 📊 Sample Experiment Results (Split Digits)

| Strategy | Task A (Initial) | Task A (Retained) | Drop / Forgetting | Final Avg Acc | BWT |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Naive Fine-Tuning** | 100.0% | 85.0% | **-15.0 pts (Alert)** | 92.0% | -15.0 pts |
| **Elastic Weight Consolidation (EWC)** | 100.0% | 95.1% | **-4.9 pts** | 96.9% | -4.9 pts |
| **Experience Replay** | 100.0% | 96.5% | **-3.5 pts** | 97.8% | -3.5 pts |
| **Joint Multi-Task (Oracle)** | 100.0% | 98.2% | **-1.8 pts** | 98.9% | -1.8 pts |

---

## 📄 License
This project is developed for academic and research presentation in the SparkX 3.0 Challenge. Open source under the MIT License.
