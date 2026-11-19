"""
MemoryMirror AI - CLI Demonstration Script
SparkX 3.0 | International Project Innovation Challenge
Team Leader: Gauri Dwivedi | Team Member: Nuka Devashmitha Reddy
"""

import sys
import numpy as np
from memory_mirror.datasets import DatasetManager
from memory_mirror.evaluation import EvaluationEngine
from memory_mirror.advisor import ContinualLearningAdvisor


def print_banner():
    banner = r"""
  __  __                               __  __ _                     _    ___ 
 |  \/  |                             |  \/  (_)                   | |  / _ \
 | \  / | ___ _ __ ___   ___  _ __ _   | \  / |_ _ __ _ __ ___  _ __| | / /_\ \
 | |\/| |/ _ \ '_ ` _ \ / _ \| '__| | | |/\| | | '__| '__/ _ \| '__| | |  _  |
 | |  | |  __/ | | | | | (_) | |  | |_| |  | | | |  | | | (_) | |  |_| | | | |
 |_|  |_|\___|_| |_| |_|\___/|_|   \__, |_|  |_|_|  |_|  \___/|_|  (_)_| |_|
                                    __/ |                                    
                                   |___/                                     
    Intelligent Continual Learning & Memory Retention Monitoring System
    SparkX 3.0 International Project Innovation Challenge
    Team: Gauri Dwivedi (Leader) & Nuka Devashmitha Reddy
    """
    print(banner)


def main():
    print_banner()
    benchmark_name = "Split MNIST Digits (2 Tasks: 0-4 vs 5-9)"
    print(f"[*] Loading Sequential Benchmark: {benchmark_name}")
    tasks = DatasetManager.load_task_sequence(benchmark_name)

    for t in tasks:
        print(f"    - [{t.name}]: {len(t.X_train)} train samples, {len(t.X_test)} test samples, classes: {t.classes}")

    print("\n" + "=" * 75)
    print(" 1. RUNNING NAIVE FINE-TUNING (BASELINE: CATASTROPHIC FORGETTING DEMO)")
    print("=" * 75)

    naive_res = EvaluationEngine.run_strategy(
        strategy_type="Naive",
        tasks=tasks,
        benchmark_name=benchmark_name,
        epochs_per_task=15,
        batch_size=32,
        lr=0.005,
    )

    print("\n[+] Sequential Evaluation Matrix R (Naive):")
    print(naive_res.to_dataframe().to_string())

    print(f"\n[+] Final Average Accuracy: {naive_res.final_avg_accuracy:.2f}%")
    print(f"[+] Average Forgetting Measure (F): {naive_res.avg_forgetting:.2f} pts")
    print(f"[+] Backward Transfer (BWT): {naive_res.backward_transfer:+.2f} pts")

    print("\n[+] Forgetting Alerts Detected:")
    for alert in naive_res.alerts:
        print(f"    {alert.message}")

    print("\n" + "=" * 75)
    print(" 2. RUNNING MEMORY PRESERVATION: ELASTIC WEIGHT CONSOLIDATION (EWC)")
    print("=" * 75)

    ewc_res = EvaluationEngine.run_strategy(
        strategy_type="EWC",
        tasks=tasks,
        benchmark_name=benchmark_name,
        epochs_per_task=15,
        batch_size=32,
        lr=0.005,
        ewc_lambda=1000.0,
    )

    print("\n[+] Sequential Evaluation Matrix R (EWC):")
    print(ewc_res.to_dataframe().to_string())

    print(f"\n[+] Final Average Accuracy: {ewc_res.final_avg_accuracy:.2f}%")
    print(f"[+] Average Forgetting Measure (F): {ewc_res.avg_forgetting:.2f} pts")
    print(f"[+] Backward Transfer (BWT): {ewc_res.backward_transfer:+.2f} pts")

    print("\n" + "=" * 75)
    print(" 3. COMPARATIVE RETENTION SUMMARY (NAIVE vs EWC)")
    print("=" * 75)
    task1_name = tasks[0].name
    naive_t1_drop = naive_res.R_matrix[0, 0] - naive_res.R_matrix[1, 0]
    ewc_t1_drop = ewc_res.R_matrix[0, 0] - ewc_res.R_matrix[1, 0]

    print(f"  • {task1_name} Initial Peak:   {naive_res.R_matrix[0, 0]:.1f}%")
    print(f"  • {task1_name} After Task B (Naive): {naive_res.R_matrix[1, 0]:.1f}%  (Drop: -{naive_t1_drop:.1f} pts) ⚠️")
    print(f"  • {task1_name} After Task B (EWC):   {ewc_res.R_matrix[1, 0]:.1f}%  (Drop: -{ewc_t1_drop:.1f} pts) ✅")
    print(f"  • Memory Retention Boost with EWC: +{naive_t1_drop - ewc_t1_drop:.1f} percentage points preserved!")

    print("\n" + "=" * 75)
    print(" 4. ANALYTICAL AI ADVISOR DIAGNOSIS")
    print("=" * 75)
    diagnosis = ContinualLearningAdvisor.generate_diagnosis(naive_res)
    print(f"  • Retention Health Score: {diagnosis['health_score']}/100 [{diagnosis['grade']}]")
    print(f"  • Diagnosis: {diagnosis['diagnosis_summary']}")
    print(f"  • Plasticity-Stability: {diagnosis['plasticity_stability_tradeoff']}")
    print("  • Automated Recommendations:")
    for rec in diagnosis["recommendations"]:
        print(f"    - [{rec.priority} | {rec.category}]: {rec.action}")
        print(f"      Rationale: {rec.rationale}")

    print("\n✅ Verification complete! Launch Streamlit app using: streamlit run app.py")


if __name__ == "__main__":
    main()
