---
name: zijin-ai-memory
description: Turn interviews, conversations, meeting notes, and idea fragments into structured people, conversation, insight, opportunity, action, and case-library assets. Use when the user asks to整理访谈、沉淀人物关系、识别合作机会、提炼洞察、建立案例库或复盘成长。
version: 0.1.0
---

# ZIJIN AI Memory Skill

## Mission

将人与人的交流转化为长期可复用的知识资产，而不是只生成摘要。

## Supported inputs

- 访谈逐字稿或摘要
- 微信/聊天记录
- 会议纪要
- 课程讨论与学员反馈
- 灵感碎片

输入必须是文本。若来源是音频，应先完成转写。

## Required pipeline

1. **Source assessment**：判断来源、参与者、场景、时间、隐私等级和信息完整度。
2. **Conversation Memory**：提取事实、议题、共识、分歧、待确认项和行动承诺。
3. **People Memory**：识别人物角色、组织、能力、诉求、关系类型、合作风格和长期价值。
4. **Insight Memory**：提炼可迁移的行业、经营、教育或个人成长洞察。
5. **Opportunity Memory**：识别合作机会，给出证据、阶段、价值、风险、前置条件和下一动作。
6. **Case Card**：形成可进入案例库的聚合卡片。
7. **Validation**：按照 schema 和脚本校验完整性、证据等级与公开安全性。
8. **Indexing**：更新案例索引。

## Relationship classification

必须先分类关系，禁止默认所有对象都是客户：

- `client`：已付费或明确采购方
- `prospective_client`：存在明确采购意向但未成交
- `partner`：共同投入资源与交付
- `channel`：提供客户、平台、政府或市场入口
- `expert`：提供专业知识或行业判断
- `project_owner`：掌握项目、产品、供应链或实施资源
- `mixed`：同时具有两种以上关键关系

## Evidence levels

- `confirmed`：原始材料明确陈述，或有可核验数据/文件支持
- `inferred`：根据多条事实合理推断，必须标注“推断”
- `hypothesis`：待验证假设，不得写成既定事实

## Output rules

每个输出文件必须包含 YAML front matter：

```yaml
---
case_id: CASE-001
asset_type: conversation_memory
privacy: public_safe
---
```

使用 `templates/` 中的结构。不要写入：

- 完整未授权逐字稿
- 电话、微信号、邮箱等联系方式
- 未经授权的合同、报价、账号或客户明细
- 对个人的未经证实负面判断
- 把平台传闻当作事实

## Quality gate

完成后必须满足：

- 人物角色与关系分类准确
- 已确认事实与推断分开
- 至少一个明确的下一步行动
- 机会包含风险和前置条件
- 案例文件通过 `validate_case.py`
- `case_index.json` 与案例目录一致

## Commands

```bash
python ZIJIN-AI-Memory-Skill/scripts/validate_case.py --all
python ZIJIN-AI-Memory-Skill/scripts/build_case_index.py
python -m unittest discover -s ZIJIN-AI-Memory-Skill/tests -v
```
