# Optimize Paper Reader Skill

## 目标
优化 paper-reader skill 的执行流程，解决以下三个主要问题，提升用户体验和系统稳定性：

1. **提前模板检查**：将模板缺失检查移至流程最前端，避免执行耗时任务后才报错
2. **增强数据注入校验**：在 JSON 注入和文件创建之间增加有效性校验机制
3. **泛化适用领域**：将硬编码的 `aiedImplications` 替换为 `practicalImplications`，并允许动态指定领域

## 实现步骤
- [ ] 步骤 1：定位并修改核心脚本/Skill 文件中的阶段划分逻辑
  - 将模板（HTML结构）检查移动到 Step 1 之前或 Step 1 的第一部分
- [ ] 步骤 2：在生成 JSON 数据和创建 HTML 文件之间加入验证逻辑
  - 解析并验证生成的 JSON 数据
  - 检查文章数量和关键字段是否存在
- [ ] 步骤 3：修改提示词和数据结构
  - 将 `aiedImplications` 修改为 `practicalImplications`
  - 在 Step 1 添加领域询问（默认值为 AI-EdTech）
- [ ] 步骤 4：更新 Quality Standards（可选增强）
  - 添加 Quiz distractor 的长度限制要求
  - 添加 keyQuotes 的长度限制要求

## 涉及文件
- 待探索确定（可能在 `skills/` 或 `.claude/skills/` 等目录下）

## 测试计划
1. 验证没有模板时是否能在前期报错
2. 验证生成有缺陷 JSON 时是否能抛出合适的异常而不是创建损坏的 HTML
3. 验证非教育类论文是否能生成合适的 implications
4. 验证生成的 HTML 在浏览器中正常工作
