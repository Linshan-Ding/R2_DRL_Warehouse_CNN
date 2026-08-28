"""重新生成论文图 13 / 图 14（仓库规模敏感性），修正原图的两处标注错误。

原 PDF 的错误（见 manuscript.tex 中对应的 % TODO (AUTHORS) 注释）:
* Aisles.pdf         副标题误为 "Fixed Aisles: N_w = 9"，
                     实际固定的是货架容量 N_l = 20、横扫 N_w；
* Rack Capacity.pdf  横轴刻度误标为 N_w=6/9/12（应为 N_l=10/20/30），
                     副标题误为 "Fixed Rack capacities: N_l = 20"
                     （应为 "Fixed aisle number: N_w = 9"）。

数据来源: paper_assets/fig_data/warehouse_scale.csv —— 从修订稿表 13/14 转录，
原始 run 出自作者的初版管线；四个 RL 基线归档进 baselines/rl/ 之前，本仓库
还不能从头复算这两张图的数据（README 第 10 节缺口 1）。

产出: paper_assets/generated/Aisles.pdf、paper_assets/generated/Rack Capacity.pdf
     （文件名与论文 Figure/ 目录一致，直接覆盖即可）
右键 Run 即可，几秒钟。
"""
from __future__ import annotations

import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "fig_data", "warehouse_scale.csv")
OUT = os.path.join(HERE, "generated")

METHODS = ["SAPPO", "AG-DQN", "HSDDQN", "SOA+A2C", "DRLG"]
COLORS = {
    "SAPPO": "#4878A8",
    "AG-DQN": "#6FA97A",
    "HSDDQN": "#D4A94D",
    "SOA+A2C": "#C96A5B",
    "DRLG": "#8E7CC3",
}

SWEEPS = {
    "aisles": {
        "filename": "Aisles.pdf",
        "title": "Performance under Different Aisle Configurations",
        "subtitle": r"Fixed rack capacity: $N_l$ = 20",
        "tick": lambda x: rf"$N_w$={x}",
    },
    "rack": {
        "filename": "Rack Capacity.pdf",
        "title": "Performance under Different Rack Capacity Configurations",
        "subtitle": r"Fixed aisle number: $N_w$ = 9",
        "tick": lambda x: rf"$N_l$={x}",
    },
}


def load():
    data = {}
    with open(DATA, newline="") as f:
        rows = [r for r in f if not r.startswith("#")]
    for row in csv.DictReader(rows):
        key = (row["sweep"], row["method"])
        data.setdefault(key, []).append(
            (int(row["x"]), float(row["mean_flow_time"]),
             float(row["avg_decision_time_ms"])))
    for key in data:
        data[key].sort()
    return data


def draw(sweep, spec, data):
    fig, (ax_f, ax_d) = plt.subplots(1, 2, figsize=(13.0, 5.2))
    xs = sorted({x for (s, m), pts in data.items() if s == sweep
                 for (x, _, _) in pts})
    for m in METHODS:
        pts = data[(sweep, m)]
        ax_f.plot([p[0] for p in pts], [p[1] for p in pts],
                  marker="o", linewidth=2, markersize=7,
                  color=COLORS[m], label=m, alpha=0.9)
        ax_d.plot([p[0] for p in pts], [p[2] for p in pts],
                  marker="o", linewidth=2, markersize=7,
                  color=COLORS[m], label=m, alpha=0.9)
    for ax, ylabel in ((ax_f, "Mean Flow Time (s)"),
                       (ax_d, "Average Decision Time (ms)")):
        ax.set_xticks(xs)
        ax.set_xticklabels([spec["tick"](x) for x in xs], fontsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.set_ylabel(ylabel, fontsize=14)
        ax.grid(alpha=0.25, linewidth=0.6)
        ax.legend(fontsize=11, framealpha=0.9)
    fig.suptitle(spec["title"], fontsize=17, y=0.99)
    ax_f.set_title(" ")  # 占位，让副标题排在总标题下方
    fig.text(0.5, 0.905, spec["subtitle"], ha="center", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, spec["filename"])
    fig.savefig(path)
    plt.close(fig)
    print(f"  写出 {os.path.relpath(path, os.path.dirname(HERE))}")


def main():
    data = load()
    for sweep, spec in SWEEPS.items():
        draw(sweep, spec, data)
    print("完成。把两个 PDF 覆盖到论文仓库的 Figure/ 目录并删除对应的 TODO 注释。")


if __name__ == "__main__":
    main()
