---
name: agent1-three-sheet-generator
description: Generate Caishuitong Agent1 three linked Excel sheets from a customer-approved template using real API query data (company, departments, users, roles, primary fee subjects, workflow). Use when preparing Agent2-importable templates, validating Sheet2↔Sheet3 name mapping, enforcing fee-limit decision rules, and preserving customer template style with merged-cell hierarchy in Sheet2.
---

# Agent1 Three-Sheet Generator

Use this skill to generate a **single executable three-sheet workbook** for the Caishuitong project, based on the customer-approved template.

## Execute

Run preflight first:

```bash
python3 scripts/preflight_check.py
```

If preflight passes, run generator:

```bash
python3 scripts/generate_three_sheets_from_customer_template.py \
  --template "assets/客户模板.xlsx" \
  --keep-group-inheritance
```

Optional custom output path:

```bash
python3 scripts/generate_three_sheets_from_customer_template.py \
  --template "assets/客户模板.xlsx" \
  --output "/tmp/三表联动_输出.xlsx" \
  --keep-group-inheritance
```

## Enforce rules

Enforce these project rules strictly:

1. Use Step3 doc types only: 报销单 / 借款单 / 批量付款单 / 申请单.
2. Apply fee-limit logic only to 报销单 and 批量付款单.
3. Inherit Sheet3 group downward when group cell is empty (visual inheritance mode).
4. Map Sheet2 `归属单据名称` one-to-one to Sheet3 `单据模板名称`.
5. Choose `费用角色限制` only when `归属单据名称` and `单据适配人员` are both non-empty.
6. Use `直接限制末级费用科目` otherwise.
7. Use workflow by reference only (Step2.5 query result), do not create in Step3.

## Produce Sheet2 hierarchy correctly

Generate Sheet2 with hierarchy constraints:

1. Keep level-3 subjects unmerged.
2. Merge level-2 and level-1 cells for contiguous blocks.
3. Keep at least 2 level-3 subjects under each level-2 subject.
4. Keep level-3 subjects globally unique.
5. Keep `单据适配人员` state consistent per `归属单据名称` (all rows have people or all rows empty).

## Require real query sources

Use real query data for:

- company info (login state)
- departments
- users
- roles
- primary fee subjects
- workflow query

Do not use hand-written placeholders for visibility objects.

## Read references when needed

Read these files for details:

- `references/API接口资料.md` for endpoint details and field mapping.
- `references/实操手册.md` for step-by-step operation and troubleshooting.
- `references/Agent1-README.md` for project context and handoff checks.
- `references/test-cases.jsonl` for trigger/eval test prompts.
- `references/eval-checklist.md` for quality gates before handoff.
- `references/字段速查.md` for a one-page field source/rule cheat sheet.

## Iterate with the new Skill-Creator style

Follow this loop when improving this skill:

1. Run a small batch with current script.
2. Evaluate with `references/eval-checklist.md`.
3. Collect failures and classify (data source / rule logic / formatting).
4. Patch script or wording.
5. Re-run test cases in `references/test-cases.jsonl`.
6. Summarize deltas and only then publish.

## Output expectations

Return:

1. Generated `.xlsx` path
2. Generated `.report.json` path
3. Quick validation summary:
   - Sheet2↔Sheet3 mapping pass/fail
   - visibility object source pass/fail
   - Sheet2 hierarchy constraints pass/fail
