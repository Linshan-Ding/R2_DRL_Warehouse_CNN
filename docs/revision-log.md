# 修订日志（第二轮返修 R2）

意见编号 ↔ 证据 ↔ 回复信位置 ↔ 修订稿落点 ↔ 状态。与论文仓库
`R2_Jiajin_Li_Dynamic_Order_Picking_CAIE` 的 `claude/paper-revision-rebuttal-b6slds`
分支对应；回复信为 `response_letter/Response_Letter.tex`。

修订稿标注约定：第一轮（R1）的蓝色标注已清除，**本轮全部改动以蓝色标注**
（与回复信封面声明一致）。

| 编号 | 意见要点 | 证据（实验 → 生成表格） | 回复信 | 修订稿落点（表号为终稿编号） | 状态 |
|---|---|---|---|---|---|
| R1.1 | 人机角色 + depot 场景 | 纯写作（E1/E7 数据支撑"最有效方式"） | Rev.1 Comment 1 | §3.1 角色表（Table 2）+ FIFO 说明；Fig. 2 重绘 | **已改稿**；Fig. 2 待作者 |
| R1.2 | 1:1 / 1:n / n:1 配比 | E0+E1+E2 → `tab_ratio.tex` | Rev.1 Comment 2 | §5.7.1（Table 16） | **已改稿** |
| R1.3 | 货架间移动 | E8 → `tab_layout.tex` | Rev.1 Comment 3 | Eq.(2) 后两情形说明 + §5.7.4（Table 19）；Fig. 2 标注路径 | **已改稿**；Fig. 2 待作者 |
| R1.4 | 货架层高 | E6 → `tab_picktime.tex` | Rev.1 Comment 4 | 新假设 (A8) + §5.7.3（Table 18）+ 结论 limitations | **已改稿** |
| R1.5 | 载运容量 | E7 + E10 规则扫描 + E9 → `tab_capacity.tex` / `tab_capacity_rules_sweep.tex` / `tab_state_capacity.tex` | Rev.1 Comment 5 | (A1) 一般化 + 新 Eq.(8) 容量约束 + 记号表 + §5.7.2（Table 17）| **已定稿**（E9 结果已回填收尾段） |
| R1.6 | 更大规模 | E2+E3 → `tab_training_cost.tex` | Rev.1 Comment 6 | §5.6.3（Table 15）+ §5.7.1 扩展规模行 | **已改稿** |
| R2.1 | 重训 vs 迁移 + 成本 | E3 → `tab_training_cost.tex` | Rev.2 Comment 1 | §5.6 开头 from-scratch 声明；§5.6.2 迁移措辞收窄 | **已改稿** |
| R2.2 | 调参预算 | 纯写作 | Rev.2 Comment 2 | §5.4 末句改写 + Table 8 脚注 + 结论 limitations | **已改稿** |
| R2.3 | γ 与 telescoping | E4 → `tab_gamma.tex` | Rev.2 Comment 3 | §4.4 Abel 展开（Eq. 18）+ §5.8.1（Table 20） | **已改稿** |
| R2.4 | 状态充分性 | E5 + E9 → `tab_state.tex`（p = 0.317）/ `tab_state_capacity.tex` | Rev.2 Comment 4 | §4.2–4.3 观测形式化 + 信息表（Table 4）+ §5.8.2（Tables 21–22） | **已定稿**（E9 已回填：C∈{2,3} 下六通道一致改善 −7.2%/−3.8%，仍逊于 MQ-MinRQ；附预算警告） |
| — | 决策时间口径（作者主动修正） | 作者初版管线测量（本仓库 `decision_time_ms` 口径不同，见 README §8/§10） | 封面 main changes 第 9 条 | 全部对比表 D̄ 列换新数据、表头加单位（F̄ 秒 / D̄ 毫秒）、§5.3 等叙述重写 | **已改稿** |

## 统计口径（第二轮确认）

- 运营配置表（Tables 16–19）：SAPPO 取各配置独立训练的**最优值**（与全文口径一致），不报标准差；规则确定性单次评测。
- 消融表（Tables 20–21）：保留 **mean ± std（3 次独立训练）**——论证依赖方差与配对检验。
- 补充实验数字只在新流水线内部自洽比较，不与主表（Tables 7/9）逐数字对照。

## 待办

实验类待办已全部完成（E10 于 2026-08-28、E9 于 2026-08-29 回填；图 13/14 已替换；
论文中新增 Table 22 后附录算例表顺延为 Table 23）。剩余均为人工项：

1. **待作者**：重绘 Fig. 2（depot + 两类示例路径）；填 Manuscript ID；
   归档四个 RL 基线到 `baselines/rl/`（Data availability 可信度所系）；
   终稿后核对回复信页码。
2. （可选）`run_e9_capacity_state.py` 打开 `BUDGET_MATCHED_BASE` 补跑 base 状态的
   3000 轮对照，把 E9 改善完全归因到通道而非预算；现稿已按预算警告口径如实表述，
   此项不阻塞投稿。

## 一致性声明

- 回复信与论文补充实验表格的所有数字由 `paper_assets/make_tables.py` 从
  `result/` 的 CSV 生成；生成片段与 manuscript.tex 对应表格逐字 diff 一致
  是验收标准（本轮已验证 7/7 张表通过）。
- 审稿意见在回复信中逐字照录（11/11）。
