# ZIJIN AI Memory Workflow

## 1. Capture

保存原始信息，但不要把完整敏感材料提交到公开仓库。公开案例只保留脱敏后的结构化证据摘要。

## 2. Assess

确认：

- 来源与日期
- 参与者及说话人映射
- 交流场景
- 信息完整度
- 隐私等级
- 是否允许公开案例化

## 3. Understand

依次执行：

- `prompts/01_conversation_capture.md`
- `prompts/02_people_memory.md`
- `prompts/03_insight_extractor.md`
- `prompts/04_opportunity_detector.md`
- `prompts/05_case_card.md`

## 4. Store

按案例目录保存六个标准文件，并创建 `manifest.json`。

## 5. Validate

```bash
python ZIJIN-AI-Memory-Skill/scripts/validate_case.py --all
```

校验内容包括：

- 文件完整性
- JSON schema 的关键字段
- case_id 一致性
- 关系类型与证据等级枚举
- 未替换模板占位符
- 公共仓库隐私规则

## 6. Index

```bash
python ZIJIN-AI-Memory-Skill/scripts/build_case_index.py
```

生成 `case_index.json`，供后续检索、统计和案例复用。

## 7. Reflect

多案例积累后执行周/月复盘：高频主题、重复痛点、新增人物、机会变化、认知升级和下一步战略重点。
