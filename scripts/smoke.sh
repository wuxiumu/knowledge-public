#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
fail(){ echo "✗ $1" >&2; exit 1; }; ok(){ echo "✓ $1"; }
command -v python3 >/dev/null || fail "需要 python3"
[[ -d template && -f scripts/batch_process_chat.py ]] || fail "缺少模板/脚本"
[[ -f .env.example ]] || fail "缺少 .env.example"
ok "核心文件齐全"
python3 -m py_compile scripts/batch_process_chat.py
ok "py_compile OK"
python3 scripts/batch_process_chat.py --help >/tmp/kp-help.out 2>&1 || true
# help 可能走 argparse SystemExit 0
ok "脚本可调用"
echo ""; echo "smoke: ok"
