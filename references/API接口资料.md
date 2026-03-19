# Agent1 API 接口资料（完整版）

> 面向：小白 AI / 新接手同学
> 
> 目的：仅靠本文件即可接入财税通查询接口并生成三表

---

## 0. 总览

Agent1 生成三表所需最小接口：

1. 获取登录态（token/companyId/companyName）
2. 组织与员工：`queryCompany`
3. 部门：`queryDepartments`
4. 角色：`role/get/tree`
5. 一级科目：`queryFeeTemplate`
6. 审批流查询：`queryWorkFlow`（仅查询）
7. 单据分组查询（可选验收）：`queryTemplateTree`

---

## 1) 登录态获取（浏览器 localStorage）

### 1.1 前提
Edge 启动参数：

```bash
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --remote-debugging-port=9223 --remote-allow-origins=*
```

### 1.2 读取表达式

```js
(function(){
  const v = localStorage.getItem('vuex');
  if(!v) return null;
  const d = JSON.parse(v);
  return {
    token: d.user?.token,
    companyId: d.user?.company?.id,
    companyName: d.user?.company?.name
  };
})()
```

---

## 2) 组织+员工接口（核心）

### POST `/api/member/department/queryCompany`

用途：
- 拿员工列表（`users[].nickName`）
- 可作为公司组织主入口

请求：

```json
{
  "companyId": 7061
}
```

响应关键字段：
- `result.users[].id`
- `result.users[].nickName`

映射：
- 员工名称 -> userId

---

## 3) 部门接口

### GET `/api/member/department/queryDepartments`

用途：
- 第一张表一级部门候选
- 第三张表可见范围（部门）候选

请求参数：
- `companyId`

响应关键字段：
- `result[].id`
- `result[].title`

映射：
- 部门名称 -> departmentId

---

## 4) 角色接口

### GET `/api/member/role/get/tree`

用途：
- 第三张表可见范围（角色）候选

请求参数：
- `companyId`

响应关键字段：
- `result[].name`（角色分类）
- `result[].children[].name`
- `result[].children[].id`

映射：
- 角色名称 -> roleId

注意：
- 费用角色组与可见范围角色概念不同，不要混用。

---

## 5) 一级科目接口

### GET `/api/bill/feeTemplate/queryFeeTemplate`

用途：
- 第二张表的一级费用科目候选（优先复用真实科目）

请求参数：
- `companyId`
- `status=1`
- `pageSize=5000`

响应关键字段：
- `result[].parentId == -1` 的记录是一级科目
- `result[].name`

---

## 6) 审批流接口（Step2.5 前置依赖）

### GET `/api/bpm/workflow/queryWorkFlow`

用途：
- 查询“通用审批流”是否存在
- 读取 workflow 名称（和后续 Agent2 引用保持一致）

请求参数：
- `companyId`
- `t=<timestamp>`

关键字段：
- `result[].tpName`
- `result[].id`（workflowId）

说明：
- Agent1 默认只查询，不创建。

---

## 7) 单据分组接口（验收可选）

### GET `/api/bill/template/queryTemplateTree`

用途：
- 验证当前系统已有分组
- 可辅助第三张表分组命名策略

请求参数：
- `companyId`
- `t=<timestamp>`

关键字段：
- `result[].id`
- `result[].name`
- `result[].children`

---

## 8) 请求头规范

```http
x-token: <token>
Content-Type: application/json
```

---

## 9) 三表字段来源矩阵

| 表 | 字段 | 来源 | 是否可随机 |
|---|---|---|---|
| 01_添加员工 | 企业名称 | 登录态 companyName | 否 |
| 01_添加员工 | 一级部门名称 | queryDepartments.title | 否 |
| 01_添加员工 | 姓名/手机号 | 规则生成（唯一） | 是 |
| 02_费用科目配置 | 一级费用科目 | queryFeeTemplate 一级 | 否（优先真实） |
| 02_费用科目配置 | 二级/三级费用科目 | 规则生成 | 是 |
| 02_费用科目配置 | 单据适配人员 | queryCompany.users.nickName | 否 |
| 03_单据表 | 可见范围类型 | 固定枚举 角色/员工/部门 | 否 |
| 03_单据表 | 可见范围对象 | 角色/员工/部门真实查询结果 | 否 |
| 03_单据表 | 单据模板名称 | 来自 Sheet2 归属单据名称映射 | 否 |

---

## 10) 规则校验清单（生成后必须过）

1. Sheet2 归属单据名称 与 Sheet3 单据模板名称一一对应
2. Step3 单据大类仅 4 类（报销单、借款单、批量付款单、申请单）
3. 费用限制只作用于 报销单/批量付款单
4. 同一单据名称在 Sheet2 的人员状态统一（全有或全无）
5. 二级科目下至少 2 个三级科目
6. 三级科目全局不重复
7. 可见范围对象可在接口结果中查到

---

## 11) 错误码与常见报错

| 现象 | 原因 | 处理 |
|---|---|---|
| 登录失效 | token 过期 | 重新登录再跑 |
| WS 403 | 未加 remote-allow-origins | 用启动参数重启 Edge |
| 角色/部门/员工为空 | companyId 错误或权限问题 | 检查登录态 companyId |
| 映射校验失败 | Sheet2/Sheet3 名称不一致 | 统一名称后重跑 |

---

## 12) 推荐脚本

- 主脚本：`scripts/generate_three_sheets_from_customer_template.py`
- 一键运行见 README
