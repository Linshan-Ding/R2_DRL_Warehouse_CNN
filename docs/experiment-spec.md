# 实验规格（run 矩阵契约）

本文件是 `experiment/` 各脚本与论文表格之间的对照契约：改任何一列，先在这里登记。
所有实验共享 `configs/{env,algo,instance}.yaml` 的默认值，差异只通过
`configs/exp/*.yaml` overlay 或点号覆盖表达；评测统一走 `eval.py`（验证流选
checkpoint、测试流单次评测），逐 run 产出 `result/<name>_run<i>/eval_results.csv`。

| 代号 | 脚本 | 配置差异 | RUNS | 轮数 | 方法 | 论文落点（终稿编号） |
|---|---|---|---|---|---|---|
| E0 | `run_e0_baseline.py` | K=3,R=6, λ⁻¹=40 基线 | 3 | 2000 | SAPPO+5 规则 | §5.7 锚点（best-of-3 = 各运营配置表首格） |
| E1 | `run_e1_ratio.py` | (K,R)=(1,1)/(3,1)/(4,2) | 各 1 | 2000 | SAPPO+5 规则 | Table 17（§5.7.1） |
| E2 | `run_e2_scale.py` | (K,R)=(8,16)/(10,20) | 各 1 | 2000 | SAPPO+MQ-ND | Table 17 扩展行 + §5.6.3 |
| E3 | `run_e3_training_cost.py` | 汇总 training_cost.csv | — | — | — | Table 16（§5.6.3） |
| E4 | `run_e4_gamma.py` | γ ∈ {0.95,0.99,1.00} | 各 3 | 2000 | SAPPO | Table 20 上块（§5.8.1，mean±std） |
| E5 | `run_e5_state_channels.py` | state_channels=plus_agent | 3 | 2000 | SAPPO | Table 20 下块（§5.8.2，mean±std+配对 t） |
| E6 | `run_e6_picktime.py` | τ_pick ∈ {15,20} s | 各 1 | 2000 | SAPPO+5 规则 | Table 19（§5.7.3） |
| E7 | `run_e7_capacity.py` | C ∈ {2,3}（round-7 起脚本含 4,5） | 各 1 | 2000 | SAPPO+5 规则 | Table 18（§5.7.2）；C=4/5 待跑，跑完自动补全 SAPPO 行 |
| E8 | `run_e8_layout.py` | layout=three_cross_aisles | 1 | 2000 | SAPPO+5 规则 | §5.7.4 行内数字（`tab_layout.tex` 溯源） |
| **E9** | `run_e9_capacity_state.py` | C∈{2,3} × plus_agent | 各 3 | **3000** | SAPPO+5 规则 | §5.7.2/§5.8.2 收尾句 + `tab_state_capacity.tex` |
| **E10** | `run_e10_rules_capacity.py` | C ∈ {1..5}，仅规则 | 1 | 免训练 | 5 规则 | Table 18 的 C=4,5 列（§5.7.2 合并容量表） |
| rules | `run_rules_only.py` | 默认配置 | 1 | 免训练 | 5 规则 | 各表对比列的来源之一 |

统计口径（与论文 §5.7 协议声明一致）：运营配置研究取 SAPPO 各配置独立训练的
**最优值**，合并消融表（Table 20）报 **mean ± std（ddof=1，3 次独立训练）**，
规则确定性、单次评测。
表格一律由 `paper_assets/make_tables.py` 生成，禁止手改数字。

变更记录：
- R2 轮新增 E9（3000 轮的理由：E7 的 C=3 曲线在 2000 轮仍在下降）与 E10；
  E0 的脚本默认值由冒烟设置改回论文口径（RUNS=3, EPISODES=None）。
- round-5（表达润色）：E8 与 E9 的结果撤表改行内，E4+E5 合并为 Table 20
  （`tab_ablation.tex`）。
- round-7：E7 与 E10 合并为一张 C=1..5 的 Table 18（规则值在 C=1,2,3 上本就一致）；
  训练成本表去掉 Runs 列，论文与回复信不再陈述重复训练次数（本仓库仍保留 RUNS=3
  的真实口径）。
