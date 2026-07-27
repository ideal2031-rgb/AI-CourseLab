# ZIJIN AI Memory Skill v0.1

将访谈、聊天、会议和灵感转化为可检索、可复用、可验证的个人知识资产与案例库。

## 定位

本项目不是录音转写器，也不是普通摘要工具。它负责在已有文本基础上完成：

1. 对话整理（Conversation Memory）
2. 人物与关系识别（People Memory）
3. 洞察提炼（Insight Memory）
4. 机会识别（Opportunity Memory）
5. 下一步行动（Next Action）
6. 案例卡与案例索引（Case Card / Case Index）

AI 负责语义分析；仓库脚本负责结构校验、隐私检查和案例索引。v0.1 不包含语音识别、向量数据库或自动调用外部大模型。

## 快速使用

将访谈文本提供给支持 Agent Skill / Prompt Skill 的 AI，并调用 `skill.md`。AI 应按照 `prompts/` 和 `templates/` 生成一个案例目录。

案例完成后运行：

```bash
python ZIJIN-AI-Memory-Skill/scripts/validate_case.py --all
python ZIJIN-AI-Memory-Skill/scripts/build_case_index.py --check
python -m unittest discover -s ZIJIN-AI-Memory-Skill/tests -v
```

## 案例目录

```text
examples/case_xxx/
├── manifest.json
├── conversation_memory.md
├── people_memory.md
├── insight_memory.md
├── opportunity_memory.md
└── case_card.md
```

## 判断原则

- 不默认“交流对象就是客户”。先判断 client、prospective_client、partner、channel、expert、project_owner 或 mixed。
- 区分 confirmed、inferred、hypothesis。
- 机会必须给出证据、约束、风险和下一步动作。
- 公开仓库不得保存完整逐字稿、联系方式、未授权商业数据或敏感个人信息。

## 当前测试案例

- `CASE-001`：网红猫姚总合作访谈（脱敏公开版），验证服务商伙伴关系、联合业务机会和高校实训机会识别。
- `CASE-002`：宜兴紫砂跨境直播拍卖验证项目（脱敏草案），验证产业项目所有者、跨境试点、职业模型和后续高校转化机会识别。

## 测试覆盖

- 企业服务商合作访谈
- 产业资源与跨境经营试点
- 人物关系多重分类
- confirmed / inferred / hypothesis 分层
- 公开案例脱敏
- 案例索引一致性

## 版本边界

v0.1 已覆盖“访谈文本 → 结构化记忆 → 案例卡 → 案例索引 → 自动校验”。语音转写、自动写入 Obsidian/Notion、向量检索和持续人物合并属于后续版本。
