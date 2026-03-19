# Eval Checklist (Agent1 Skill)

## Functional checks
1. Script runs and outputs xlsx + report json.
2. Data sources are real-query based for roles/users/departments/primary subjects.
3. Sheet2↔Sheet3 mapping is one-to-one.

## Rule checks
1. Step3 doc types limited to 4 classes.
2. Fee limit applies only to 报销单/批量付款单.
3. Group inheritance visual output works when enabled.
4. Sheet2 hierarchy constraints pass:
   - L1/L2 merged
   - L3 unmerged
   - each L2 has >=2 L3
   - L3 globally unique

## Handoff checks
1. Workbook path exists and opens.
2. report json has counts and rule summary.
3. visibility objects are in real queried pools.
