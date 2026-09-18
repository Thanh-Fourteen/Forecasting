#!/usr/bin/env bash
# SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/sinh_nen.py rồi chạy lại tool.
# Dựng nền của buoi-08: môi trường Python chốt phiên bản + dữ liệu đã kiểm sha256.
#     bash lab/00-nen/chuan-bi.sh [--tom-tat]        (make up gọi lệnh này)
set -euo pipefail
NEN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
unset VIRTUAL_ENV  # venv đang bật ở nơi khác sẽ bị uv bỏ qua kèm cảnh báo — gỡ cho gọn

if ! command -v uv >/dev/null 2>&1; then
    echo "✗ Chưa có uv. Cài:  curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    echo "  (hướng dẫn: https://docs.astral.sh/uv/getting-started/installation/)" >&2
    exit 1
fi

echo "==> Môi trường Python theo uv.lock (uv sync --frozen)"
uv sync --frozen --project "$NEN"

echo "==> Dữ liệu (tải hoặc lấy từ cache, kiểm sha256)"
uv run --no-sync --project "$NEN" python "$NEN/lay_du_lieu.py" "$NEN/du-lieu.toml" "$@"

echo "==> Xong nền buoi-08"
