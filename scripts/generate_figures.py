"""
Generate Academic Figures for CA3 Deep Learning Report
- Model Architecture & Training Pipeline Block Diagram
- Comparative Experiment Performance Bar Chart (38-Class Baseline vs. Top-15 Model)
- Top-15 Species Split Distribution Chart
"""
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = Path("docs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Block Diagram: Architecture & Data Pipeline
def generate_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.axis('off')
    
    # Colors
    box_color = '#e8f4f8'
    edge_color = '#1f77b4'
    text_color = '#1a252f'
    accent_color = '#2ca02c'
    
    boxes = [
        {"text": "Data Ingestion\n- In-situ Field Photos (Excel)\n- iNaturalist Observations\n(Filtered CC Licenses)", "pos": (0.05, 0.55), "w": 0.22, "h": 0.35, "color": "#eaf2f8"},
        {"text": "Data Curation & Partitioning\n- Label Verification & Quarantine\n- Grouped Splitting (Observation ID)\n- Independent Van Udyan Benchmark (30)", "pos": (0.32, 0.55), "w": 0.24, "h": 0.35, "color": "#eafaf1"},
        {"text": "Preprocessing & Augmentation\n- Input Resizing (224x224x3)\n- EfficientNet Preprocessing [0, 255]\n- Random Flip, Rotation, Zoom (Train Only)", "pos": (0.61, 0.55), "w": 0.22, "h": 0.35, "color": "#fef9e7"},
        {"text": "Backbone & Classifier Head\n- EfficientNetB0 (ImageNet Pretrained)\n- GlobalAveragePooling2D\n- Dense(256) + Dropout(0.35)\n- Softmax (15 Classes)", "pos": (0.18, 0.08), "w": 0.30, "h": 0.35, "color": "#f4ecf7"},
        {"text": "Evaluation & Post-Processing\n- Held-Out Test (143 images)\n- Local Field Benchmark (30 images)\n- Top-1 & Top-3 Accuracy\n- Low-Confidence Filter (<40%)", "pos": (0.54, 0.08), "w": 0.30, "h": 0.35, "color": "#fbeee6"}
    ]
    
    for b in boxes:
        rect = patches.FancyBboxPatch(
            b["pos"], b["w"], b["h"],
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=b["color"],
            edgecolor='#2c3e50',
            linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(
            b["pos"][0] + b["w"]/2, b["pos"][1] + b["h"]/2,
            b["text"],
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=text_color, linespacing=1.4
        )
        
    # Arrows
    arrow_props = dict(facecolor='#2c3e50', edgecolor='#2c3e50', width=1.5, headwidth=8, headlength=8)
    # Box 1 -> Box 2
    ax.annotate('', xy=(0.32, 0.72), xytext=(0.27, 0.72), arrowprops=arrow_props)
    # Box 2 -> Box 3
    ax.annotate('', xy=(0.61, 0.72), xytext=(0.56, 0.72), arrowprops=arrow_props)
    # Box 3 -> Box 4 (downwards curve)
    ax.annotate('', xy=(0.48, 0.25), xytext=(0.72, 0.55),
                arrowprops=dict(facecolor='#2c3e50', edgecolor='#2c3e50', width=1.5, headwidth=8, headlength=8,
                                connectionstyle="arc3,rad=-0.3"))
    # Box 4 -> Box 5
    ax.annotate('', xy=(0.54, 0.25), xytext=(0.48, 0.25), arrowprops=arrow_props)
    
    plt.title("End-to-End Pipeline & Architecture: Van Udyan Plant AI (EfficientNetB0)", fontsize=13, fontweight='bold', pad=20)
    plt.tight_layout()
    out_file = OUTPUT_DIR / "pipeline_architecture_diagram.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_file}")

# 2. Comparative Experiment Results Bar Chart
def generate_comparison_chart():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    
    categories = ['Held-Out Test Top-1', 'Held-Out Test Top-3', 'Local Benchmark Top-1', 'Local Benchmark Top-3']
    
    # Actual verified experimental metrics
    exp1_38_class = [10.53, 21.93, 9.29, 20.00]
    exp2_top15_effnet = [23.78, np.nan, 13.33, 33.33]  # Test Top-3 was not saved in evaluation outputs, marked unrecorded
    
    x = np.arange(len(categories))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, exp1_38_class, width, label='Exp 1: 38-Class Baseline (MobileNetV2)', color='#4a90e2', edgecolor='#1c538c')
    rects2 = ax.bar(x + width/2, [v if not np.isnan(v) else 0 for v in exp2_top15_effnet], width, label='Exp 2: Top-15 Focused Model (EfficientNetB0)', color='#50b86c', edgecolor='#237a3b')
    
    # Value labels
    for rect, val in zip(rects1, exp1_38_class):
        height = rect.get_height()
        ax.annotate(f'{val:.2f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
                    
    for rect, val in zip(rects2, exp2_top15_effnet):
        if not np.isnan(val):
            height = rect.get_height()
            ax.annotate(f'{val:.2f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            ax.annotate('Not Recorded',
                        xy=(rect.get_x() + rect.get_width() / 2, 1),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, fontstyle='italic', color='#7f8c8d')
                        
    ax.set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
    ax.set_title('Empirical Comparison: 38-Class Baseline vs. Top-15 Focused Model', fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 42)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='#f8f9fa', edgecolor='#bdc3c7', fontsize=10)
    
    plt.tight_layout()
    out_file = OUTPUT_DIR / "experimental_accuracy_comparison.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_file}")

# 3. Top-15 Species Split Distribution Chart
def generate_species_split_chart():
    import pandas as pd
    summary_csv = Path("data/processed_top15/top15_species_split_summary.csv")
    if not summary_csv.exists():
        print("Summary CSV missing, skipping species distribution chart.")
        return
        
    df = pd.read_csv(summary_csv)
    # Sort by total images descending
    df['total'] = df['train'] + df['val'] + df['test'] + df['test_van_udyan_benchmark']
    df = df.sort_values(by='total', ascending=True)
    
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    y_pos = np.arange(len(df))
    
    p1 = ax.barh(y_pos, df['train'], label='Train (iNat + Field)', color='#2b5c8f')
    p2 = ax.barh(y_pos, df['val'], left=df['train'], label='Validation (iNat + Field)', color='#5b92e5')
    p3 = ax.barh(y_pos, df['test'], left=df['train']+df['val'], label='Held-Out Test (iNat)', color='#a0c4ff')
    p4 = ax.barh(y_pos, df['test_van_udyan_benchmark'], left=df['train']+df['val']+df['test'], label='Untouched Field Benchmark (2/sp)', color='#e67e22')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['species'], fontsize=9, fontstyle='italic')
    ax.set_xlabel('Total Verified Image Count', fontsize=10, fontweight='bold')
    ax.set_title('Top-15 Van Udyan Dataset Partitioning by Species (Total = 1,008)', fontsize=12, fontweight='bold', pad=15)
    ax.legend(loc='lower right', frameon=True, fontsize=9)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    for i, total in enumerate(df['total']):
        ax.text(total + 1, i, f"{total}", va='center', fontsize=8.5, fontweight='bold', color='#2c3e50')
        
    ax.set_xlim(0, max(df['total']) + 8)
    plt.tight_layout()
    out_file = OUTPUT_DIR / "top15_species_distribution.png"
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Generated {out_file}")

if __name__ == "__main__":
    generate_pipeline_diagram()
    generate_comparison_chart()
    generate_species_split_chart()
