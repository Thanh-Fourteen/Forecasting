"""Chạy RIÊNG từng khối ```python của Phụ lục B (mỗi khối một namespace trắng) — khối nào lỗi là chưa tự chứa."""
import contextlib
import io
import pathlib
import re

md = pathlib.Path(__file__).resolve().parents[1] / "B-xac-suat-toi-thieu.md"
khoi = re.findall(r"```python\n(.*?)```", md.read_text(encoding="utf-8"), re.S)
loi = 0
for i, b in enumerate(khoi):
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(b, f"khoi-{i}", "exec"), {})
        print(f"khối {i:2d}: chạy được")
    except Exception as e:
        loi += 1
        print(f"khối {i:2d}: LỖI {type(e).__name__}: {e}")
print("số khối lỗi:", loi)
