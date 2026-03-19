#!/usr/bin/env python3
"""
Preflight check for Agent1 skill portability.
Checks:
1) CDP port reachable (9223)
2) cst.uf-tree.com page attached
3) token/companyId readable from localStorage
4) key APIs reachable and minimally valid

Exit code 0 = pass, 1 = fail
"""

import json
import sys
import time
import requests
import websocket

BASE_URL = "https://cst.uf-tree.com"
CDP_LIST = "http://localhost:9223/json/list"


def fail(msg):
    print(f"❌ {msg}")
    return False


def ok(msg):
    print(f"✅ {msg}")
    return True


def get_auth():
    pages = requests.get(CDP_LIST, timeout=6).json()
    ws_url = None
    for p in pages:
        if "cst.uf-tree.com" in p.get("url", ""):
            ws_url = p.get("webSocketDebuggerUrl")
            break
    if not ws_url:
        raise RuntimeError("未发现 cst.uf-tree.com 页面")

    ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
    ws.send(json.dumps({
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": "(function(){const v=localStorage.getItem('vuex');if(!v)return null;const d=JSON.parse(v);return {token:d.user?.token, companyId:d.user?.company?.id, companyName:d.user?.company?.name};})()",
            "returnByValue": True,
        },
    }))
    raw = ws.recv()
    ws.close()

    value = json.loads(raw).get("result", {}).get("result", {}).get("value")
    if not value or not value.get("token") or not value.get("companyId"):
        raise RuntimeError("读取 token/companyId 失败（请确认已登录）")
    return value


def api_get(token, endpoint, params):
    return requests.get(
        f"{BASE_URL}{endpoint}",
        headers={"x-token": token, "Content-Type": "application/json"},
        params=params,
        timeout=15,
    ).json()


def api_post(token, endpoint, payload):
    return requests.post(
        f"{BASE_URL}{endpoint}",
        headers={"x-token": token, "Content-Type": "application/json"},
        json=payload,
        timeout=15,
    ).json()


def main():
    all_ok = True

    # 1) CDP reachable
    try:
        pages = requests.get(CDP_LIST, timeout=6).json()
        all_ok &= ok(f"CDP 可用，页面数: {len(pages)}")
    except Exception as e:
        fail(f"无法访问 CDP 9223: {e}")
        return 1

    # 2-3) auth
    try:
        auth = get_auth()
        token = auth["token"]
        cid = auth["companyId"]
        cname = auth.get("companyName", "")
        all_ok &= ok(f"登录态可读: companyId={cid}, companyName={cname}")
    except Exception as e:
        fail(str(e))
        return 1

    # 4) APIs
    checks = []
    try:
        r = api_post(token, "/api/member/department/queryCompany", {"companyId": cid})
        users = (r.get("result", {}) or {}).get("users", []) or []
        checks.append((len(users) > 0, f"queryCompany 用户数={len(users)}"))
    except Exception as e:
        checks.append((False, f"queryCompany 异常: {e}"))

    try:
        r = api_get(token, "/api/member/department/queryDepartments", {"companyId": cid})
        deps = r.get("result", []) or []
        checks.append((len(deps) > 0, f"queryDepartments 部门数={len(deps)}"))
    except Exception as e:
        checks.append((False, f"queryDepartments 异常: {e}"))

    try:
        r = api_get(token, "/api/member/role/get/tree", {"companyId": cid})
        tree = r.get("result", []) or []
        role_count = sum(len(x.get("children") or []) for x in tree)
        checks.append((role_count > 0, f"role/get/tree 角色数={role_count}"))
    except Exception as e:
        checks.append((False, f"role/get/tree 异常: {e}"))

    try:
        r = api_get(token, "/api/bill/feeTemplate/queryFeeTemplate", {"companyId": cid, "status": 1, "pageSize": 5000})
        rows = r.get("result", []) or []
        pcount = len([x for x in rows if x.get("parentId") == -1])
        checks.append((pcount > 0, f"queryFeeTemplate 一级科目数={pcount}"))
    except Exception as e:
        checks.append((False, f"queryFeeTemplate 异常: {e}"))

    try:
        r = api_get(token, "/api/bpm/workflow/queryWorkFlow", {"companyId": cid, "t": int(time.time() * 1000)})
        wfs = r.get("result", []) or []
        checks.append((True, f"queryWorkFlow 可用，返回 {len(wfs)} 条"))
    except Exception as e:
        checks.append((False, f"queryWorkFlow 异常: {e}"))

    for passed, msg in checks:
        if passed:
            ok(msg)
        else:
            fail(msg)
            all_ok = False

    print("\n---- PRECHECK RESULT ----")
    if all_ok:
        ok("全部通过，可执行生成脚本")
        return 0
    else:
        fail("存在失败项，请先修复环境再生成")
        return 1


if __name__ == "__main__":
    sys.exit(main())
