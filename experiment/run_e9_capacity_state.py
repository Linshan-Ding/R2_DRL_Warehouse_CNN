"""E9 载运容量 x 状态通道 —— 回复信中两处 "待 E9 定稿" 段落的数据来源。

动机（见 docs/revision-log.md 的 R1.5 / R2.4 两行）:
E7 显示 C = 3 时 SAPPO 落后于队列均衡规则 MQ-MinRQ，而 E5 显示在 C = 1 下
额外的 per-robot 通道没有显著收益（p = 0.317）。两个结论合起来提出了一个
可检验的假设——批量化拉长并异化了每台机器人的剩余行程，正是 per-robot
信息开始起作用的领域。E9 在 C ∈ {2, 3} 下训练 plus_agent 状态（6 通道），
与 E7 的 base 状态（4 通道）对比，直接回答这个假设。

两种结果都可以写进论文:
* plus_agent 在 C > 1 下显著改善 -> 支持 "批量化使 per-robot 信息变得关键"，
  回复信 R1-C5 / R2-C4 的收尾句按此定稿；
* 无显著差异 -> 说明瓶颈在策略/路由结构而非信息可见性，同样如实报告。

训练轮数默认 3000（高于全局默认 2000）: E7 的 C = 3 训练曲线在 2000 轮时仍在
下降（2256 -> 1959），加长预算避免把 "训练不足" 误判成 "信息不足"。若要做
预算严格对齐的对比，把下面 BUDGET_MATCHED_BASE 打开，让 base 状态在同样的
3000 轮下重训一遍。

产出: result/e9_c2_plus_run*/、result/e9_c3_plus_run*/ 下的 eval_results.csv
     （打开 BUDGET_MATCHED_BASE 后还有 result/e9_c2_base_run*/ 等）
随后: 右键运行 paper_assets/make_tables.py，同步论文 5.7.2 / 5.8.2 的收尾句
耗时: 每配置每次训练约 2.5-4 小时（GPU）；RUNS = 3 时共 6 次训练。
"""
import _bootstrap  # noqa: F401  必须最先导入

from _runner import DEFAULT_METHODS, run_experiment

# ==================== 配置区（改完右键 Run） ====================
CONFIGS = [
    # 名字, 叠加的 overlay 列表（后者覆盖前者；这里叠加 = 容量 x 状态通道）
    ("e9_c2_plus", ["configs/exp/e7_capacity_2.yaml",
                    "configs/exp/e5_state_plus_agent.yaml"]),
    ("e9_c3_plus", ["configs/exp/e7_capacity_3.yaml",
                    "configs/exp/e5_state_plus_agent.yaml"]),
]
BUDGET_MATCHED_BASE = False   # True 时补跑 base 状态的 3000 轮对照
RUNS = 3                      # 论文级消融 >= 3 次独立训练
EPISODES = 3000               # 高于默认 2000，理由见文件头
METHODS = list(DEFAULT_METHODS)
TIERS = ["main"]
# ==============================================================

_BASE_CONFIGS = [
    ("e9_c2_base", ["configs/exp/e7_capacity_2.yaml"]),
    ("e9_c3_base", ["configs/exp/e7_capacity_3.yaml"]),
]


def main(configs=None, runs=RUNS, episodes=EPISODES, methods=METHODS, tiers=TIERS):
    if configs is None:
        configs = list(CONFIGS) + (_BASE_CONFIGS if BUDGET_MATCHED_BASE else [])
    run_dirs = []
    for name, overlays in configs:
        run_dirs += run_experiment(name=name, overlays=overlays, runs=runs,
                                   episodes=episodes, methods=methods, tiers=tiers)
    return run_dirs


if __name__ == "__main__":
    main()
