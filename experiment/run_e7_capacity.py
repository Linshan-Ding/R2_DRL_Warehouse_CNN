"""E7 机器人单次载运能力 —— 回应 Reviewer #1，本轮唯一的真实建模改动。

已投稿版本的假设 (A1) 把 AMR 锁死为"一次一单"，全文和代码里都没有任何容量参数。
现在引入单次载运订单数上限 C: depot 处一次绑定至多 C 个待分配订单，必访点取并集，
返回时按订单数结算打包时间。C = 1 与原实现逐事件完全等价（run_00_selfcheck 第 3 项
就在断言这件事），所以这是模型的推广而不是替换。

结论方向不可预设。参考数据: 在规则 MQ-ND、lam40、K=3/R=6 下，
C=1 时 F = 1892.17，C=2 时 F = 1948.98，反而变差 3%——C 变大会拉长单台机器人的路径，
若不配套路径优化，F 未必单调改善。这本身是有价值的发现，但写回复信时不能提前
假定"性能随 C 提升"，要等这个实验的 SAPPO 结果出来再定调。

C = 4、5 于第七轮补入: 论文的容量表把五条确定性规则铺满 C = 1..5（E10），
SAPPO 行原先只到 C = 3、C = 4/5 留空，而载运容量正是 Reviewer #1 点名的维度。
两个新配置沿用与 C = 2/3 完全相同的预算（RUNS=1、2000 轮）——该表比较的是容量，
同一行内预算必须固定，否则数值差异会混入预算差异；大容量收敛更慢这一点照旧
在表注里如实说明，不靠加轮数掩盖。

产出: result/e7_c2_run*/ ... result/e7_c5_run*/ 下的 eval_results.csv
随后: 右键运行 paper_assets/make_tables.py —— tab_capacity.tex 会自动补全
     SAPPO 行的 C=4/5 两格（缺目录时写 "--"，不需要改代码）
耗时: 每个配置一次训练约 3.3 h（RTX 4060 Laptop，见论文训练成本表），
     只跑 C=4/5 约 7 GPU 小时；纯 CPU 则以天计。
"""
import _bootstrap  # noqa: F401  必须最先导入

from _runner import DEFAULT_METHODS, run_experiment

# ==================== 配置区（改完右键 Run） ====================
CONFIGS = [
    # 已跑完（result/ 里已有结果）；只补 C=4/5 时把这两行注释掉即可
    ("e7_c2", "configs/exp/e7_capacity_2.yaml"),
    ("e7_c3", "configs/exp/e7_capacity_3.yaml"),
    ("e7_c4", "configs/exp/e7_capacity_4.yaml"),
    ("e7_c5", "configs/exp/e7_capacity_5.yaml"),
]
RUNS = 1
EPISODES = None
METHODS = list(DEFAULT_METHODS)
TIERS = ["main"]
# ==============================================================


def main(configs=CONFIGS, runs=RUNS, episodes=EPISODES, methods=METHODS, tiers=TIERS):
    run_dirs = []
    for name, overlay in configs:
        run_dirs += run_experiment(name=name, overlays=[overlay], runs=runs,
                                   episodes=episodes, methods=methods, tiers=tiers)
    return run_dirs


if __name__ == "__main__":
    main()
