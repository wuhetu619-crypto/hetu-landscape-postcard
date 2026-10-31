# 对标与 v2 升级记录

核验日期：2026-10-31（Asia/Shanghai）。星标取自 GitHub 仓库 API，属于整个仓库，不是单独 Skill 的星标。维护情况同时检查仓库推送与技能目录提交，不能用 `updated_at` 替代代码维护时间。

## 候选比较

| 候选 | 仓库星标 | 核验到的维护 | 匹配与选择 |
| --- | ---: | --- | --- |
| [JimLiu/baoyu-design](https://github.com/JimLiu/baoyu-design) 的 claude-design | 5,516 | 仓库及技能目录 2026-10-31 有提交 | 主要方法对标：设计规则、变体与局部修改；是更广泛的平面设计技能，不是专用撕纸明信片技能 |
| [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) 的 baoyu-cover-image | 27,092 | 仓库最近提交 2026-09-10；该目录最近提交 2026-06-13 | 补充图片维度与生成流程；不能说这个 Skill 本身今天更新 |
| [Whiplashzeb/photo-to-zine-postcard](https://github.com/Whiplashzeb/photo-to-zine-postcard) | 266 | 最近推送 2026-08-07 | 用途更近，但热度与近期维护不如主要对标项；不是撕纸同景版画 |
| [kaijie-czyh/pocket-postcard-skill](https://github.com/kaijie-czyh/pocket-postcard-skill) | 0 | 最近推送 2026-08-04 | 用途相近，不满足高星优先 |

本次没有找到同时具备完全相同撕纸风格、高星和近期提交的专用技能。选择近期维护的高星设计技能作为主要方法对标，辅以图片生成技能；不把通用设计技能包装成现成同款。

## 可追溯版本

- 主要：[claude-design / a977d87](https://github.com/JimLiu/baoyu-design/blob/a977d87d18196be72802813b278d0d6fccdf46fd/skills/claude-design/SKILL.md)，[craft.md](https://github.com/JimLiu/baoyu-design/blob/a977d87d18196be72802813b278d0d6fccdf46fd/skills/claude-design/artifact-type/reference/craft.md)。此提交时间为 2026-10-31 03:25:24 UTC，更新包含编辑器评论协作；不是说所有设计原则在当天新增。
- 补充：[baoyu-cover-image / 1567581](https://github.com/JimLiu/baoyu-skills/blob/1567581c26ec29f4216c6e6835415bf30343b0e3/skills/baoyu-cover-image/SKILL.md)。目录最近记录见 [b0ac523](https://github.com/JimLiu/baoyu-skills/commit/b0ac5233ccc289fefabe4d5b7946bce14e4f9f26)。

## 实际对比与改造

| 维度 | v1 | 对标启发 | v2 的落实 |
| --- | --- | --- | --- |
| 风格组织 | 5 项核心概括 | 小型设计系统与独立设计轴 | 固定核心 + 12 维可调语法 |
| 版式 | 六图对应建议 | 有意义的布局变体 | 6 种骨架，写明适用条件与冲突 |
| 色彩 | 建议 HEX 色板 | 前景/背景/点色分工 | 纸/墨/点色 + 明度、色温、原片适配 |
| 材质 | 撕纸、版画概括 | 细节、层次与质感规则 | 宏观裂口与微纤维、四种印刷语言 |
| 跨界 | 同景衔接原则 | 明确视觉结构与构图意图 | 每张指定 1–3 条结构的起点与去向 |
| 原片保护 | 文字提醒 | 上下文与目标约束 | 内容锚点、保留项、参考角色、裁切降级 |
| 文案 | 极小英文短句 | 文本层级独立控制 | 英短句/中文/无字，尺度与可读性规则 |
| 多图 | 简短调用示例 | 共同设计规则与变体轴 | 系列锁定项、可变项、失败项单独重试 |
| 复用 | 生成后记录提示词 | 生成前保存最终提示词 | 提示词版本、原片对应、实际输出回读 |
| 质量 | 通用检查清单 | 具体执行规则 | 硬性缺陷 + 7 项证据量表 + 有界修正 |
| 发布 | 包含第三方样图 | 资源角色与可移植性 | 公共文字包 + 可选本地参考，不依赖私有路径 |
| 验证 | 结构检查 | 可复查交付 | 结构/脚本/场景审查 + 1 次合成原片实测 |

## 没有照搬的部分

上游的 HTML 画布、编辑器、特定运行时命令、品牌色、强制首次配置、默认审批步骤，以及“不要查看渲染结果”的环境专属限制，都不适合本任务。本项目继续使用 Codex 原生图像编辑与视觉回读，不安装对标技能，不执行其脚本，不新增多代理依赖。

当前只借鉴组织方法并针对明信片独立编写，不把外部文档里的指令当成当前会话命令。署名见仓库第三方说明。
