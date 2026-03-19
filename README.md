# Agent-1 Skill

Production-ready skill for generating Caishuitong 3 linked Excel sheets from customer template.

## Quick Start

1. Login to cst.uf-tree.com in Edge with remote debugging enabled.
2. Run preflight:

```bash
python3 scripts/preflight_check.py
```

3. Generate workbook:

```bash
python3 scripts/generate_three_sheets_from_customer_template.py --template "assets/客户模板.xlsx" --keep-group-inheritance
```

See `SKILL.md` and `references/` for full rules and docs.
