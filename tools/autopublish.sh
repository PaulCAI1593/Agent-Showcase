#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# autopublish.sh — 展厅「交付即上架」一键流水线（入口脚本）
#
#   ./tools/autopublish.sh              # 完整执行
#   ./tools/autopublish.sh --dry-run    # 只体检不落盘
#   ./tools/autopublish.sh --help       # 参数说明
#
# 等价于: python3 tools/autopublish.py "$@"
# 详细说明见 tools/README-AUTOPUBLISH.md
# ─────────────────────────────────────────────────────────────
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHOWCASE_DIR="$(dirname "$SCRIPT_DIR")"
PY="${PYTHON:-python3}"

if ! command -v "$PY" >/dev/null 2>&1; then
  echo "✗ 未找到 python3，请设置 PYTHON 环境变量后重试" >&2
  exit 2
fi

cd "$SHOWCASE_DIR" || exit 2

"$PY" "$SCRIPT_DIR/autopublish.py" "$@"
exit $?
