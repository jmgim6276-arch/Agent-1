# Agent-1（财税通三表生成 Skill）> 给小白 AI / 新同学的可落地版本

> **一键生成三张联动 Excel，直接交付给 Agent2 导入**

---

## 🎯 功能概览

| 功能 | 说明 |
|------|------|
| 浏览器自动检测 | 自动检测 Edge/Chrome 浏览器，智能切换 |
| Excel 生成优化 | 移除下拉选项，只保留第二列筛选 |
| 员工姓名来源 | 单据适配人员来自 Sheet1 生成的员工 |
| 单据名称验证 | 从 API 查询已存在名称，自动生成唯一名称 |
| 费用规则优化 | 根据单据类型灵活处理费用限制 |

---

## 📁 快速开始

### 前置条件

1. **Edge 浏览器** 以调试模式启动（可选，Chrome 备用）
   ```bash
   /Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --remote-debugging-port=9223 --remote-allow-origins=*
   ```

2. **登录财税通**
   - 在 Edge 中打开：`https://cst.uf-tree.com`
   - 保持登录状态

### 第一步：预检环境

```bash
python3 scripts/preflight_check.py
```

检查项：
- Edge 调试端口是否可用
- 财税通页面是否已登录
- Token/CompanyId 是否有效
- 员工/部门/角色数据

---

### 第二步：生成三表

```bash
python3 scripts/generate_three_sheets_from_customer_template.py \\
  --template "assets/客户模板.xlsx" \\
  --keep-group-inheritance
```

生成文件：
- `三表联动_客户模板_公司xxxx_时间戳.xlsx`
- `同名.report.json`

三张表：
- **01_添加员工** - 员工信息
- **02_费用科目配置** - 费用科目与角色绑定
- **03_单据表** - 单据模板与可见范围

---

## 🎯 核心功能

### 1. 浏览器自动检测（Edge/Chrome 双支持）
- 优先使用包含财税通页面的浏览器
- 自动检测并切换

### 2. Excel 数据验证移除
- 清除所有下拉选项（数据验证）
- 只保留第二列筛选（是否导入/是否执行/是否创建）

### 3. 员工姓名来源优化
- Sheet2 的"单据适配人员"直接使用 Sheet1 生成的员工姓名
- 不依赖 API 用户列表

### 4. 单据名称验证
- 从 API 查询已存在的单据模板名称
- 自动生成带时间戳的唯一名称（如：20260402_1058_差旅报销单）
- 避免与 API 中的名称冲突

### 5. 费用规则优化
- 仅报销单和批量付款单使用"费用角色限制"
- 借款单、申请单不处理费用限制

### 6. Sheet3 视觉优化
- 可见范围类型可以为空（如"全员"）
- 优化分组显示逻辑

---

## 📂 项目结构

```
Agent-1/
├── SKILL.md                # 技能文档
├── scripts/
│   ├── preflight_check.py      # 环境预检
│   ├── generate_three_sheets_from_customer_template.py  # 主生成脚本
│   └── generate_direct.py       # 直接模式脚本
├── assets/                  # 生成的 Excel 和报告
└── references/              # 字段速查表
```

---

## 🔧 使用方法

### 方式一：标准流程（推荐小白）

```bash
# 1. Edge 浏览器调试模式 + 登录
python3 scripts/preflight_check.py

# 2. 生成三表
python3 scripts/generate_three_sheets_from_customer_template.py \\
  --template "assets/客户模板.xlsx" \\
  --keep-group-inheritance

# 3. 导入三表
cd ~/.openclaw/workspace/finance/agent2
python3 scripts/import_from_agent1.py \\
  --xlsx "/path/to/三表联动_xxxx.xlsx"
```

### 方式二：直接使用 token（快速模式）

```bash
python3 scripts/generate_direct.py
```

---

## 📖 字段说明

| Sheet1 字段 | 说明 |
|---------|------|
| 姓名 | 自动生成，11 位手机号格式 |
| 一级部门名称 | 从 API 动态获取 |
| 单据适配人员 | Sheet1 生成的员工姓名 |
| 单据名称 | 带时间戳的唯一标识 |
| 备注 | 额外的规则说明 |

---

## ⚠️ 注意事项

1. **权限问题**
   - 需要有 `api/member/queryCompany`、`api/member/role/get/tree` 等接口权限
   - Token 需要有效且有 companyId 权限

2. **数据一致性**
   - 单据名称必须与 Sheet3 一一对应
   - "归属单据名称" 和 "单据适配人员" 状态必须统一

3. **表格限制**
   - 某款单、申请单不处理费用限制分支
   - 借款单、申请单的 "费用限制方式" 字段为空

4. **可见范围**
   - "可见范围类型" 为"全员"时，"可见范围对象" 可为空

---

## 📚 常见问题

**Q：跑不起来，提示找不到页面**
- A: 先确认 Edge 是否在 9223 调试模式运行
- A: 检查财税通页面是否登录

**Q：生成失败，提示权限不足**
- A: 需要检查 Token 和 companyId

**Q：单据名称不一致**
- A: Sheet2 的"归属单据名称" 与 Sheet3 的"单据模板名称" 不一致

---

更新内容已在仓库中！查看：
```
https://github.com/jmgim6276-arch/agent1.1
```

