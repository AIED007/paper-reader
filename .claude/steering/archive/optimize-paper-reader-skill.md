# Optimize Paper Reader Skill

## 目标
优化 paper-reader skill 的执行流程，解决以下三个主要问题，提升用户体验和系统稳定性：

1. **提前模板检查**：将模板缺失检查移至流程最前端，避免执行耗时任务后才报错
2. **增强数据注入校验**：在 JSON 注入和文件创建之间增加有效性校验机制
3. **泛化适用领域**：将硬编码的 `aiedImplications` 替换为 `practicalImplications`，并允许动态指定领域

## 实现步骤
- [x] 步骤 1：定位并修改核心脚本/Skill 文件中的阶段划分逻辑
  - 将模板（HTML结构）检查移动到 Step 1 之前或 Step 1 的第一部分
- [x] 步骤 2：在生成 JSON 数据和创建 HTML 文件之间加入验证逻辑
  - 解析并验证生成的 JSON 数据
  - 检查文章数量和关键字段是否存在
- [x] 步骤 3：修改提示词和数据结构
  - 将 `aiedImplications` 修改为 `practicalImplications`
  - 在 Step 1 添加领域询问（默认值为 AI-EdTech）
- [x] 步骤 4：更新 Quality Standards（可选增强）
  - 添加 Quiz distractor 的长度限制要求 (15 words)
  - 添加 keyQuotes 的长度限制要求 (40 words / 2-3 lines)

## 状态
**已完成**

## 更改细节
- 修改了 `SKILL.md`，调整了流程顺序。
- 添加了更严格的 JSON 验证步骤和字段映射。
