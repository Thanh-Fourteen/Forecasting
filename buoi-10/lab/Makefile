# Lab của buổi. Chạy trong thư mục lab/:
#   make up                 dựng môi trường (uv sync --frozen) + tải dữ liệu, kiểm sha256
#   make check              chấm bài trong code/
#   make check BAI=dap-an   chấm bản đáp án (tác giả)
#   make notebook           mở JupyterLab (tạo .ipynb từ .py nếu chưa có)
#   make down               xoá môi trường + dữ liệu của buổi (cache tải về vẫn giữ)
#
# Chỉ dùng cú pháp GNU Make 3.81 (bản có sẵn trên macOS): không .ONESHELL, không !=, không &:

NEN := 00-nen
BAI ?= code
UV  := env -u VIRTUAL_ENV uv run --no-sync --project $(NEN)

.PHONY: help up check down notebook kiem-nen

help:
	@echo "make up | make check [BAI=dap-an] | make notebook | make down"

up:
	@bash $(NEN)/chuan-bi.sh

kiem-nen:
	@test -x $(NEN)/.venv/bin/python || { echo "Chưa dựng nền — chạy: make up"; exit 1; }

check: kiem-nen
	BAI=$(BAI) $(UV) python -m pytest -q -p no:cacheprovider cham

notebook: kiem-nen
	@for f in ../code/*.py; do \
		test -e "$${f%.py}.ipynb" || $(UV) jupytext --to ipynb "$$f"; \
	done
	$(UV) jupyter lab --ServerApp.root_dir=..

down:
	rm -rf $(NEN)/.venv du-lieu/raw .pytest_cache
	-find . ../code ../dap-an -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null
