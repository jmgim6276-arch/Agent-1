# Agent-1（财税通三表生成 Skill）

> 给小白 AI / 新同学的可落地版本：登录财税通后，一键生成可给 Agent2 执行的三张表。

---

## 1. 这个仓库能做什么

本仓库只做一件事：

**基于客户确认模板 + 实时接口数据，生成三张联动 Excel：**
1. `01_添加员工`
2. `02_费用科目配置`
3. `03_单据表`

并且自动遵守项目硬规则（名称映射、费用限制、合并规则等）。

---

## 2. 适用场景

- 你要给 Agent2 提供可执行输入表
- 你要批量验证不同账号下三表生成质量
- 你不想手填角色/员工/部门映射

---

## 3. 前置条件（必须）

1. 已安装 Python 3.9+
2. 已安装依赖：

```bash
pip3 install openpyxl requests websocket-client
```

3. Edge 以调试模式启动（Mac 示例）：

```bash
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --remote-debugging-port=9223 --remote-allow-origins=*
```

4. 在 Edge 中登录：`https://cst.uf-tree.com`

---

## 4. 一键使用（推荐）

### 第一步：预检环境

```bash
python3 scripts/preflight_check.py
```

预检会检查：
- 调试端口是否可用
- 登录态是否可读（token/companyId）
- 关键接口是否可访问（员工/部门/角色/一级科目/审批流）

### 第二步：生成三表

```bash
python3 scripts/generate_three_sheets_from_customer_template.py \
  --template "assets/客户模板.xlsx" \
  --keep-group-inheritance
```

生成结果：
- `三表联动_客户模板_公司xxxx_时间戳.xlsx`
- `同名.report.json`

---

## 5. 关键业务规则（已写死在脚本里）

### 5.1 Step3 单据大类限制
仅允许：
- 报销单
- 借款单
- 批量付款单
- 申请单

### 5.2 费用限制适用范围
仅适用于：
- 报销单
- 批量付款单

借款单、申请单不处理费用限制。

### 5.3 Sheet2 ↔ Sheet3 映射
- Sheet2 `归属单据名称` 必须与 Sheet3 `单据模板名称` 一一对应
- 脚本内置强校验，不一致直接报错

### 5.4 费用限制二选一
仅当同时满足：
1. `归属单据名称` 非空
2. `单据适配人员` 非空

才走：`费用角色限制`，否则只能：`直接限制末级费用科目`。

### 5.5 第二张表层级规则
- 一级、二级可合并
- 三级不合并
- 每个二级下至少 2 个三级
- 三级科目全局不重复
- 同一单据名称的“单据适配人员”状态统一（全有或全无）

### 5.6 第三张表分组继承
- 开启 `--keep-group-inheritance` 时，分组按向下继承视觉输出（后续行可空）

---

## 6. 字段来源说明（最常问）

### 必须来自接口查询
- 企业名称（登录态）
- 部门（queryDepartments）
- 员工（queryCompany）
- 角色（role/get/tree）
- 一级费用科目（queryFeeTemplate）
- 审批流（queryWorkFlow）

### 允许规则生成
- 测试员工姓名、手机号
- 二级/三级费用科目（但必须满足层级规则）
- 备注字段

详细表格见：`references/字段速查.md`

---

## 7. 仓库结构

```text
Agent-1/
├── SKILL.md
├── scripts/
│   ├── preflight_check.py
│   └── generate_three_sheets_from_customer_template.py
├── assets/
│   └── 客户模板.xlsx
├── references/
│   ├── API接口资料.md
│   ├── 实操手册.md
│   ├── 字段速查.md
│   ├── eval-checklist.md
│   └── test-cases.jsonl
└── README.md
```

---

## 8. 常见问题

### Q1：跑不起来，提示找不到页面
先确认 Edge 是否用 9223 启动，并且页面已登录财税通。

### Q2：可见范围对象映射失败
通常是账号权限或数据不足，先跑 `preflight_check.py` 看角色/员工/部门数量。

### Q3：生成成功但 Agent2 执行失败
优先检查：
1. Sheet2/Sheet3 名称映射是否一致
2. 第二张表人员状态是否统一
3. 第三张表可见范围对象是否真实可查

---

## 9. 发布给客户前检查清单

- [ ] 预检全绿（preflight 全通过）
- [ ] 成功生成 xlsx + report
- [ ] Sheet2↔Sheet3 名称一一对应
- [ ] Sheet2 合并规则正确
- [ ] 可见范围对象来自真实接口
- [ ] report 中规则摘要正确

---

如果你是第一次接触本项目，建议阅读顺序：
1. `references/字段速查.md`
2. `references/实操手册.md`
3. `references/API接口资料.md`
