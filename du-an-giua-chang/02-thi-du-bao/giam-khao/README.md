# giam-khao/ — KHÔNG vào zip phát học viên

- `loi-giai-mau/du_bao.py`: lời giải mẫu, đủ bậc thang (seasonal naive → hồi quy → LightGBM global → ensemble). Chấm tối thiểu
  (trong `lab/`): `BAI=giam-khao/loi-giai-mau 00-nen/.venv/bin/python -m pytest -q cham` → 6/6 xanh.
- `chay-thu/<nhom>/<moc>/`: các lần nộp và chấm của giám khảo (`bien-ban.json`, `du-bao.csv`, `ket-qua.json`; tệp dữ liệu không commit).
  `loi-giai-mau/2026-09-28` là bài nộp THẬT trước mốc (tạo 2026-09-24 09:25 UTC) — chấm từ 2026-10-09:
  `python lab.py chay ../cong-cu/cham.py --moc 2026-09-28 --nhom loi-giai-mau --ra ../giam-khao/chay-thu`.
