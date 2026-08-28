"""E10 规则 x 载运容量扫描 C = 1..5 —— 论文 5.7.2 节 "U 形曲线" 的数据来源。

E7 只覆盖 C ∈ {1, 2, 3}，其中只有队列均衡规则 MQ-MinRQ 从批量化中获益
（1823.3 -> 1618.0 -> 1485.8）。论文 5.7.2 断言 "规则的收益曲线呈 U 形、
最低点在 C = 3 附近"，这需要 C = 4、5 的数据点支撑——本脚本把五条规则在
C = 1..5 下全部评一遍。规则是确定性的、无需训练，全程分钟级。

产出: result/rules_c1/ ... result/rules_c5/ 下的 eval_results.csv
随后: 右键运行 paper_assets/make_tables.py，
     生成的 tab_capacity_rules_sweep.tex 用来回填论文 5.7.2 的
     "% TODO (AUTHORS): add the C=4/5 rule-sweep results" 段落
耗时: 约 5-10 分钟（CPU 即可）。
"""
import _bootstrap  # noqa: F401  必须最先导入

from _runner import RULES_ONLY, run_experiment

# ==================== 配置区（改完右键 Run） ====================
CAPACITIES = [1, 2, 3, 4, 5]
METHODS = list(RULES_ONLY)   # 五条组合规则；SAPPO 需要训练，不在本脚本范围
TIERS = ["main"]
# ==============================================================


def main(capacities=CAPACITIES, methods=METHODS, tiers=TIERS):
    run_dirs = []
    for c in capacities:
        run_dirs += run_experiment(
            name=f"rules_c{c}",
            overlays=[],
            runs=1,
            methods=methods,
            tiers=tiers,
            train_first=False,
            overrides={"env.robot_capacity": c},
        )
    return run_dirs


if __name__ == "__main__":
    main()
