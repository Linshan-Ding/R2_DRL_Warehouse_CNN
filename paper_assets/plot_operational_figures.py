"""生成论文 5.7 节两张新数据图（第二轮返修，round-5 增补）。

* ratio-sensitivity.pdf    —— 5.7.1 配比研究（Fig.~\\ref{fig:ratio_sensitivity}）
  左联：SAPPO 与最优规则的最优平均流程时间（哑铃图，对数横轴——量级跨 260~11000 s）；
  右联：SAPPO 相对最优规则的 Gap（发散条形，蓝=SAPPO 占优 / 橙=规则占优）。
  数据与 tab_ratio.tex 同源同口径（lam40，SAPPO 取独立训练最优，规则确定性单评）。

* capacity-sensitivity.pdf —— 5.7.2 容量研究（Fig.~\\ref{fig:capacity_sensitivity}）
  五条规则在 C=1..5 的扫描曲线（result/rules_c*，E10）+ SAPPO 在 C=1..3 的
  最优值散点（e0 / e7_c2 / e7_c3），与 tab_capacity.tex 及正文扫描句同源。

配色为经校验的分类色板（相邻对 CVD ΔE 与常视力下限均通过，白底），
图内数值与生成表格逐字同源——运行后与 manuscript.tex 中蓝色数字核对即可。
产出: paper_assets/generated/{ratio,capacity}-sensitivity.{pdf,png}
（PDF 覆盖到论文仓库 Figure/ 目录；PNG 仅供快速目检。）右键 Run 即可。
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

from make_tables import RULES, rules_at, sappo_best  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "generated")

# 经 dataviz 校验的分类色板（白底）：槽位次序即图例次序，不得循环复用。
BLUE = "#2a78d6"    # SAPPO
ORANGE = "#eb6834"  # 最优规则 / 规则占优
RULE_COLORS = {
    "MQ-ND": "#eb6834",
    "MQ-MinRQ": "#1baf7a",
    "MQ-MI": "#eda100",
    "MI-MinRQ": "#e87ba4",
    "MI-MI": "#008300",
}
RULE_MARKERS = {"MQ-ND": "s", "MQ-MinRQ": "o", "MQ-MI": "^",
                "MI-MinRQ": "v", "MI-MI": "D"}
GRAY_CONNECT = "#c3c2b7"
INK_MUTED = "#52514e"

RATIO_CONFIGS = [
    ("1:1", "e1_k1r1"),
    ("3:1", "e1_k3r1"),
    ("4:2", "e1_k4r2"),
    ("3:6", "e0"),
    ("8:16", "e2_k8r16"),
    ("10:20", "e2_k10r20"),
]
ANCHOR = "3:6"


def _save(fig, stem):
    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        path = os.path.join(OUT, f"{stem}.{ext}")
        fig.savefig(path, dpi=150)
        print(f"  写出 {os.path.relpath(path, os.path.dirname(HERE))}")
    plt.close(fig)


def fig_ratio():
    rows = []
    for label, prefix in RATIO_CONFIGS:
        sappo = sappo_best(prefix, "lam40")
        rules = rules_at(prefix, "lam40")
        if sappo is None or not rules:
            print(f"  [跳过] ratio 图: 缺少 result/{prefix}_run*")
            return
        best = min(rules, key=rules.get)
        gap = (rules[best] - sappo) / rules[best] * 100
        rows.append((label, sappo, rules[best], gap))
        print(f"    {label:>6}: SAPPO {sappo:.1f}  best rule {best} "
              f"{rules[best]:.1f}  gap {gap:+.1f}%")

    fig, (ax_f, ax_g) = plt.subplots(
        1, 2, figsize=(13.0, 5.2), gridspec_kw={"width_ratios": [1.5, 1.0]})
    ys = range(len(rows))

    # 左联：哑铃图（对数横轴，位置编码而非长度编码）
    for y, (label, sappo, rule, _) in zip(ys, rows):
        ax_f.plot([sappo, rule], [y, y], color=GRAY_CONNECT,
                  linewidth=1.6, zorder=1)
    ax_f.scatter([r[1] for r in rows], list(ys), s=110, color=BLUE,
                 edgecolors="white", linewidths=1.4, zorder=3,
                 label="SAPPO", marker="o")
    ax_f.scatter([r[2] for r in rows], list(ys), s=95, color=ORANGE,
                 edgecolors="white", linewidths=1.4, zorder=3,
                 label="Best dispatching rule", marker="s")
    anchor_idx = [r[0] for r in rows].index(ANCHOR)
    a_sappo, a_rule = rows[anchor_idx][1], rows[anchor_idx][2]
    ax_f.annotate(f"{a_sappo:,.1f}", (a_sappo, anchor_idx),
                  textcoords="offset points", xytext=(-8, -1),
                  ha="right", va="center", fontsize=10.5, color=INK_MUTED)
    ax_f.annotate(f"{a_rule:,.1f}", (a_rule, anchor_idx),
                  textcoords="offset points", xytext=(9, -1),
                  ha="left", va="center", fontsize=10.5, color=INK_MUTED)
    ax_f.set_xscale("log")
    ax_f.set_xticks([300, 1000, 3000, 10000])
    ax_f.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax_f.set_xlim(200, 17000)
    ax_f.set_yticks(list(ys))
    ax_f.set_yticklabels([r[0] for r in rows], fontsize=12)
    ax_f.get_yticklabels()[anchor_idx].set_fontweight("bold")
    ax_f.invert_yaxis()
    ax_f.set_xlabel("Best mean flow time (s, log scale)", fontsize=13)
    ax_f.set_ylabel("Picker-to-robot ratio $K{:}R$", fontsize=13)
    ax_f.tick_params(axis="x", labelsize=11)
    ax_f.grid(axis="x", alpha=0.25, linewidth=0.6)
    ax_f.legend(fontsize=11, framealpha=0.9, loc="lower right")

    # 右联：Gap 发散条形（蓝=SAPPO 占优，橙=规则占优，0 为中性基线）
    gaps = [r[3] for r in rows]
    colors = [BLUE if g > 0 else (ORANGE if g < 0 else GRAY_CONNECT)
              for g in gaps]
    ax_g.barh(list(ys), gaps, height=0.52, color=colors, zorder=3)
    ax_g.axvline(0, color=GRAY_CONNECT, linewidth=1.0, zorder=2)
    for y, g in zip(ys, gaps):
        ax_g.annotate(f"{g:+.1f}%", (g, y),
                      textcoords="offset points",
                      xytext=(6 if g >= 0 else -6, 0),
                      ha="left" if g >= 0 else "right", va="center",
                      fontsize=10.5, color=INK_MUTED)
    ax_g.set_yticks(list(ys))
    ax_g.set_yticklabels([])
    ax_g.invert_yaxis()
    ax_g.set_xlim(-11, 19)
    ax_g.set_xlabel("Gap of SAPPO to the best rule (%)", fontsize=13)
    ax_g.tick_params(axis="x", labelsize=11)
    ax_g.grid(axis="x", alpha=0.25, linewidth=0.6)
    ax_g.annotate("SAPPO better", xy=(0.97, 0.03), xycoords="axes fraction",
                  ha="right", va="bottom", fontsize=10, color=INK_MUTED)
    ax_g.annotate("rule better", xy=(0.03, 0.03), xycoords="axes fraction",
                  ha="left", va="bottom", fontsize=10, color=INK_MUTED)

    fig.suptitle("Performance under Different Picker-to-Robot Ratios",
                 fontsize=17, y=0.99)
    fig.text(0.5, 0.905, r"$1/\lambda$ = 40 stream", ha="center", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    _save(fig, "ratio-sensitivity")


def fig_capacity():
    caps = [1, 2, 3, 4, 5]
    per_c = {}
    for c in caps:
        rules = rules_at(f"rules_c{c}", "lam40")
        if not rules:
            print(f"  [跳过] capacity 图: 缺少 result/rules_c{c}")
            return
        per_c[c] = rules
    sappo_pts = []
    for c, prefix in ((1, "e0"), (2, "e7_c2"), (3, "e7_c3")):
        v = sappo_best(prefix, "lam40")
        if v is None:
            print(f"  [跳过] capacity 图: 缺少 result/{prefix}_run*")
            return
        sappo_pts.append((c, v))
    print("    best rule per C:",
          ", ".join(f"C={c} {min(per_c[c].values()):.1f}" for c in caps))
    print("    SAPPO:", ", ".join(f"C={c} {v:.1f}" for c, v in sappo_pts))

    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    for rule in RULES:
        emphasized = rule == "MQ-MinRQ"
        ax.plot(caps, [per_c[c][rule] for c in caps],
                marker=RULE_MARKERS[rule], markersize=8 if emphasized else 7,
                linewidth=2.6 if emphasized else 1.8,
                color=RULE_COLORS[rule], label=rule,
                markeredgecolor="white", markeredgewidth=1.2,
                alpha=1.0 if emphasized else 0.85, zorder=3)
    ax.plot([c for c, _ in sappo_pts], [v for _, v in sappo_pts],
            linestyle=(0, (4, 2)), linewidth=2.4, color=BLUE, marker="o",
            markersize=9, markeredgecolor="white", markeredgewidth=1.4,
            label="SAPPO ($C \\leq 3$)", zorder=4)
    ax.annotate("SAPPO", xy=sappo_pts[-1], textcoords="offset points",
                xytext=(10, 4), fontsize=11, color=INK_MUTED)
    ax.annotate("MQ-MinRQ", xy=(5, per_c[5]["MQ-MinRQ"]),
                textcoords="offset points", xytext=(-2, -18),
                ha="right", fontsize=11, color=INK_MUTED)
    ax.set_xticks(caps)
    ax.set_xlabel("Single-trip carrying capacity $C$", fontsize=13)
    ax.set_ylabel("Best mean flow time (s)", fontsize=13)
    ax.tick_params(labelsize=11)
    ax.grid(alpha=0.25, linewidth=0.6)
    handles, labels = ax.get_legend_handles_labels()
    order = ["SAPPO ($C \\leq 3$)"] + list(RULES)
    pairs = sorted(zip(labels, handles), key=lambda lh: order.index(lh[0]))
    ax.legend([h for _, h in pairs], [l for l, _ in pairs],
              fontsize=10, framealpha=0.9, loc="upper left", ncol=2)
    ax.set_title("Effect of the Single-Trip Carrying Capacity", fontsize=16,
                 pad=26)
    ax.text(0.5, 1.02, r"$1/\lambda$ = 40 stream, dispatching rules swept"
            r" over $C$ = 1–5", transform=ax.transAxes, ha="center",
            fontsize=12)
    fig.tight_layout()
    _save(fig, "capacity-sensitivity")


def main():
    print("ratio 图:")
    fig_ratio()
    print("capacity 图:")
    fig_capacity()
    print("完成。把两个 PDF 覆盖到论文仓库 Figure/ 目录"
          "（文件名 ratio-sensitivity.pdf / capacity-sensitivity.pdf）。")


if __name__ == "__main__":
    main()
