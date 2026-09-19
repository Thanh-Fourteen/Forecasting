# %% [markdown]
# # Chấm tự động phần "phát hiện lỗi cài sẵn" (30/100 điểm) — GIÁM KHẢO GIỮ
#
#     cd lab && python lab.py chay \
#         ../giam-khao/cham_phat_hien.py ../bai-nop/nguyen-van-a/bao-cao-loi.json
#
# Học viên nộp `bao-cao-loi.json` dạng:
#
#     {"loi": [{"loai": "doi_don_vi", "tep": "noi-bai", "cot": "temperature",
#               "tu": "2025-04-01", "den": "2025-12-31",
#               "bang_chung": "mức nhảy 45,2 °C tại 2025-04-01, biên độ ngày ×1,8"}]}
#
# Một mục chỉ được tính là "tìm thấy" khi đúng loại, đúng tệp VÀ khoảng thời gian chồng lên lỗi thật
# (nới ±3 ngày). Khi đó: 5 điểm = **3 tìm thấy + 1 đúng cột + 1 hai đầu khoảng lệch ≤ 3 ngày**.
# Mọi mục khác là báo lỗi không có thật: **−2 điểm** mỗi cái (tối đa trừ 6). Đề đã nêu sáu loại lỗi,
# nên chỉ khớp loại thì ai liệt kê đủ sáu loại cũng được điểm — phải khớp cả tệp và khoảng.

# %%
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

GIAM_KHAO = Path(__file__).resolve().parent
DIEM_MOI_LOI = 5
DIEM_BAO_SAI = -2
TRU_TOI_DA = -6
DUNG_SAI_NGAY = 3

# Học viên có thể gọi tên khác — chấp nhận các từ đồng nghĩa hay gặp.
DONG_NGHIA = {
    "doi_don_vi": {"doi_don_vi", "don_vi", "unit", "unit_change", "doi_thang_do", "f_sang_c"},
    "cam_bien_dung_yen": {"cam_bien_dung_yen", "dung_yen", "stuck", "stuck_sensor", "mac_ket", "gia_tri_lap"},
    "lech_mui_gio": {"lech_mui_gio", "mui_gio", "timezone", "tz", "lech_gio", "doi_mui_gio"},
    "dong_trung_lap": {"dong_trung_lap", "trung_lap", "duplicate", "trung_moc", "lap_dong"},
    "ngay_gia_0": {"ngay_gia_0", "gia_tri_0", "zero", "ngay_0", "so_0_gia", "sentinel_0"},
    "doi_nhan_thoi_gian": {"doi_nhan_thoi_gian", "doi_nhan", "shift", "lech_nhan", "doi_ngay", "dich_1_ngay"},
}


def _chuan(ten: str) -> str:
    ten = (ten or "").strip().lower().replace("-", "_").replace(" ", "_")
    for chuan, bo in DONG_NGHIA.items():
        if ten in bo:
            return chuan
    return ten


def _trong_khoang(bao: dict, that: dict) -> bool:
    try:
        bt, bd = pd.Timestamp(bao.get("tu")), pd.Timestamp(bao.get("den"))
        tt, td = pd.Timestamp(that["tu"]), pd.Timestamp(that["den"])
    except (ValueError, TypeError):
        return False
    return (abs((bt - tt).days) <= DUNG_SAI_NGAY) and (abs((bd - td).days) <= DUNG_SAI_NGAY)


def _chong_len(bao: dict, that: dict) -> bool:
    try:
        bt, bd = pd.Timestamp(bao.get("tu")), pd.Timestamp(bao.get("den"))
        tt, td = pd.Timestamp(that["tu"]), pd.Timestamp(that["den"])
    except (ValueError, TypeError):
        return False
    noi = pd.Timedelta(days=DUNG_SAI_NGAY)
    return bt <= td + noi and bd >= tt - noi


def cham(bao_cao: dict, dap_an: dict) -> dict:
    that = {d["loai"]: d for d in dap_an["loi"]}
    da_dung: set[str] = set()
    chi_tiet, bao_sai = [], []
    for muc in bao_cao.get("loi", []):
        loai = _chuan(muc.get("loai", ""))
        g = that.get(loai)
        if g is None or _chuan(muc.get("tep", "")) != _chuan(g["tep"]) or not _chong_len(muc, g):
            bao_sai.append(muc.get("loai"))
            continue
        if loai in da_dung:  # báo trùng một lỗi không được cộng hai lần
            continue
        da_dung.add(loai)
        diem = 3
        dung_cot = g["cot"] == "*" or _chuan(muc.get("cot", "")) == _chuan(g["cot"])
        if dung_cot:
            diem += 1
        dung_khoang = _trong_khoang(muc, g)
        if dung_khoang:
            diem += 1
        chi_tiet.append({"ma": g["ma"], "loại": loai, "điểm": diem, "đúng cột": dung_cot,
                         "đúng khoảng thời gian": dung_khoang,
                         "có bằng chứng": bool(str(muc.get("bang_chung", "")).strip())})

    sot = [d["ma"] for d in dap_an["loi"] if d["loai"] not in da_dung]
    diem_tim = sum(c["điểm"] for c in chi_tiet)
    tru = max(TRU_TOI_DA, DIEM_BAO_SAI * len(bao_sai))
    return {"điểm phát hiện lỗi (tối đa 30)": max(0, diem_tim + tru),
            "số lỗi tìm đúng": len(chi_tiet), "trên tổng": len(dap_an["loi"]),
            "bỏ sót": sot, "báo lỗi không có thật": bao_sai, "trừ điểm": tru,
            "chi tiết": chi_tiet,
            "thiếu bằng chứng": [c["ma"] for c in chi_tiet if not c["có bằng chứng"]]}


# %%
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Chấm phần phát hiện lỗi cài sẵn của dự án giữa chặng 1")
    ap.add_argument("bao_cao", help="bao-cao-loi.json của học viên")
    ap.add_argument("--dap-an", default=str(GIAM_KHAO / "dap_an_loi.json"))
    t = ap.parse_args()
    kq = cham(json.loads(Path(t.bao_cao).read_text(encoding="utf-8")),
              json.loads(Path(t.dap_an).read_text(encoding="utf-8")))
    print(json.dumps(kq, ensure_ascii=False, indent=2))
