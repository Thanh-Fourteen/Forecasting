"""Test cho tools/kiem_de_hieu.py — chỉ thư viện chuẩn.

    .venv/bin/python tools/test_kiem_de_hieu.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import kiem_de_hieu as k  # noqa: E402

TN = [
    k.ThuatNgu(dang=["quantile", "phân vị"], buoi_min=2, ten="quantile"),
    k.ThuatNgu(dang=["baseline"], buoi_min=1, ten="baseline"),
    k.ThuatNgu(dang=["mean absolute error"], buoi_min=1, ten="MAE"),
]

TOT = """# Buổi 1 — Thử

## 1. Mục tiêu

Học một điều.

## 2. Nhắc lại buổi trước

Không có.

## 4. Lý thuyết

### Từ mới trong buổi

| Thuật ngữ | Nghĩa | Ví dụ |
|---|---|---|
| baseline | cách dự báo đơn giản để so | lấy số tuần trước |
| MAE | sai lệch trung bình, bỏ dấu | 2 và 4 → 3 |

### 4.1 Baseline

Baseline là cách dự báo đơn giản nhất để so sánh.

> **Mượn trước — quantile.** Quantile 0,8 là mốc mà 80% giá trị nằm dưới. Buổi 2 học kỹ.

$$
\\hat y = y_{t-1}
$$

- $\\hat y$ là dự báo.

**Nói bằng lời.** Dự báo ngày mai bằng số hôm nay: hôm nay 5 thì mai đoán 5.

![Hình thử](hinh/a.png)

**Cách đọc hình.** Trục ngang là ngày.

| Cách | MAE |
|---|---|
| A | 1,2 |
| B | 3,4 |

**Đọc bảng.** A tốt hơn B.

**Tóm lại.** Luôn có baseline.

**Tự kiểm tra.** Baseline để làm gì?

## 5. Lab từng bước

### Bước 1 — Chạy

**Mục đích:** thấy MAE.

**Đọc kết quả:** thấy 1,2 là đúng.

## 9. Đọc thêm

"This is a long English sentence that should not be flagged here at all" — nằm ở Đọc thêm.
"""


def ma(van_ban, so_buoi=1):
    return [v.ma for v in k.kiem_tai_lieu(van_ban, so_buoi, TN, set())]


class KiemTaiLieu(unittest.TestCase):
    def test_tai_lieu_tot_khong_vi_pham(self):
        self.assertEqual(ma(TOT), [])

    def test_thieu_bang_tu_moi(self):
        self.assertIn("tu_moi", ma(TOT.replace("### Từ mới trong buổi", "### Bảng khác")))

    def test_thuat_ngu_buoi_nay_chua_vao_bang(self):
        vb = TOT.replace("| baseline | cách dự báo đơn giản để so | lấy số tuần trước |\n", "")
        self.assertIn("chua_bang", ma(vb))

    def test_thuat_ngu_buoi_sau_thieu_muon_truoc(self):
        vb = TOT.replace("> **Mượn trước — quantile.** Quantile 0,8 là mốc mà 80% giá trị nằm dưới. Buổi 2 học kỹ.",
                         "Dùng quantile để chọn.")
        self.assertIn("muon_truoc", ma(vb))
        self.assertNotIn("muon_truoc", ma(vb, so_buoi=2))   # buổi 2 dạy chính nó

    def test_cong_thuc_thieu_noi_bang_loi(self):
        self.assertIn("cong_thuc", ma(TOT.replace("**Nói bằng lời.**", "Vậy là")))

    def test_hinh_thieu_cach_doc(self):
        self.assertIn("hinh", ma(TOT.replace("**Cách đọc hình.**", "**Đọc hình.**")))

    def test_bang_ket_qua_thieu_doc_bang(self):
        self.assertIn("bang", ma(TOT.replace("**Đọc bảng.** A tốt hơn B.", "Thế thôi.")))

    def test_tom_lai_va_tu_kiem(self):
        vb = TOT.replace("**Tóm lại.** Luôn có baseline.", "").replace("**Tự kiểm tra.** Baseline để làm gì?", "")
        self.assertIn("tom_lai", ma(vb))
        self.assertIn("tu_kiem", ma(vb))

    def test_qua_nhieu_khai_niem(self):
        them = "".join(f"\n### 4.{i} Mục {i}\n\n**Tóm lại.** x.\n\n**Tự kiểm tra.** y?\n" for i in range(2, 9))
        vb = TOT.replace("## 5. Lab từng bước", them + "\n## 5. Lab từng bước")
        self.assertEqual(ma(vb).count("khai_niem"), 2)       # 8 mục → vượt 2

    def test_lab_thieu_muc_dich(self):
        self.assertIn("lab", ma(TOT.replace("**Mục đích:** thấy MAE.", "")))

    def test_cau_dai(self):
        cau = "Đây là " + "một câu rất dài " * 12 + "kết thúc."
        self.assertIn("cau_dai", ma(TOT.replace("Baseline là cách dự báo đơn giản nhất để so sánh.", cau)))

    def test_nhieu_so_nhung_khong_tinh_ngay_va_tham_chieu(self):
        self.assertIn("nhieu_so", ma(TOT.replace("Trục ngang là ngày.", "MAE 1,2; chi phí 3,4; tỷ lệ 5,6%; trễ 7,8 giờ.")))
        # ngày tháng, giờ, "buổi 2", "mục 4.8" không làm vượt ngưỡng
        vb = TOT.replace("Trục ngang là ngày.", "Ngày 25/10/2010 lúc 00:00, xem buổi 2 và mục 4.8, giá 1,5.")
        self.assertNotIn("nhieu_so", ma(vb))

    def test_tieng_anh_chua_dich(self):
        vb = TOT.replace("Baseline là cách dự báo đơn giản nhất để so sánh.",
                         'FPP viết "the average value of the forecast distribution is used".')
        self.assertIn("tieng_anh", ma(vb))
        vb2 = vb.replace("is used\".", "is used\" (dịch: giá trị trung bình).")
        self.assertNotIn("tieng_anh", ma(vb2))

    def test_viet_tat_tu_che(self):
        vb = TOT.replace("Baseline là cách dự báo đơn giản nhất để so sánh.", "Dùng TB 4 tuần làm baseline.")
        self.assertIn("viet_tat", ma(vb))

    def test_code_block_bi_bo_qua(self):
        vb = TOT.replace("## 9. Đọc thêm", "```python\nx = 'TB XYZW' + \"a b c d e f g h\"\n```\n\n## 9. Đọc thêm")
        self.assertEqual(ma(vb), [])


class KiemGon(unittest.TestCase):
    """D13 — câu rỗng, lặp ý."""

    def test_cau_rong(self):
        vb = TOT.replace("Baseline là cách dự báo đơn giản nhất để so sánh.",
                         "Như đã nói ở trên, baseline là cách dự báo đơn giản nhất để so sánh.")
        self.assertIn("cau_rong", ma(vb))
        vb2 = TOT.replace("Baseline là cách dự báo đơn giản nhất để so sánh.", "Ta tiến hành phân tích dữ liệu.")
        self.assertIn("cau_rong", ma(vb2))

    def test_tom_lai_chep_lai_cau_trong_muc(self):
        cau = "Baseline là cách dự báo đơn giản nhất mà ai cũng làm được để so sánh với mô hình."
        vb = TOT.replace("Baseline là cách dự báo đơn giản nhất để so sánh.", cau)
        self.assertNotIn("lap_y", ma(vb))
        self.assertIn("lap_y", ma(vb.replace("**Tóm lại.** Luôn có baseline.", "**Tóm lại.** " + cau)))

    def test_hai_doan_gan_trung(self):
        doan = ("Chấm trên chính dữ liệu đã dùng để khớp mô hình luôn cho sai số nhỏ hơn thật, "
                "vì mô hình đã nhìn thấy một phần đáp án trước khi bị chấm điểm.")
        vb = TOT.replace("Baseline là cách dự báo đơn giản nhất để so sánh.", doan)
        self.assertNotIn("lap_y", ma(vb))
        vb2 = vb.replace("**Mục đích:** thấy MAE.", "**Mục đích:** thấy MAE.\n\n" + doan)
        self.assertIn("lap_y", ma(vb2))


class KiemQuiz(unittest.TestCase):
    def test_dap_an_ngan(self):
        q = "**Câu 1.** Hỏi?\n\n- A. x\n- B. y\n\n<details>\n<summary>Đáp án</summary>\n\n**B.**\n\n</details>\n"
        self.assertEqual([v.ma for v in k.kiem_quiz(q)], ["quiz"])

    def test_dap_an_tot(self):
        q = ("**Câu 1.** Hỏi?\n\n- A. x\n- B. y\n\n<details>\n<summary>Đáp án</summary>\n\n"
             "**B.** Vì y đúng với định nghĩa trong mục 4.1 của buổi học hôm nay. A sai vì x chỉ đúng khi dữ liệu "
             "không có mùa vụ, mà chuỗi điện luôn có mùa vụ ngày.\n\n</details>\n")
        self.assertEqual(k.kiem_quiz(q), [])

    def test_khong_noi_lua_chon_khac(self):
        q = ("**Câu 1.** Hỏi?\n\n- A. x\n- B. y\n\n<details>\n<summary>Đáp án</summary>\n\n"
             "**B.** Vì y đúng với định nghĩa trong mục 4.1 của buổi học hôm nay, được chứng minh bằng thí "
             "nghiệm có số liệu thật.\n\n</details>\n")
        self.assertEqual([v.ma for v in k.kiem_quiz(q)], ["quiz"])


class DoDai(unittest.TestCase):
    def test_khong_dem_bang_va_code(self):
        vb = "một hai ba\n| a | b | c |\n```\nx = 1 2 3\n```\nbốn năm"
        self.assertEqual(k.dem_chu(vb), 5)


class PhuLucE(unittest.TestCase):
    def test_doc_bang_nhieu_cot(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("| Tiếng Anh | Viết trong khoá | Nói đơn giản | Ví dụ | Buổi |\n|---|---|---|---|---|\n"
                    "| quantile | quantile (phân vị) | mốc | 1..5 → 4,2 | 2, 25 |\n"
                    "| mean absolute error, MAE | MAE | sai trung bình | 2,4 → 3 | 1 |\n")
        tn, vt = k.doc_phu_luc_e(Path(f.name))
        self.assertEqual([t.buoi_min for t in tn], [2, 1])
        self.assertIn("phân vị", tn[0].dang)
        self.assertIn("MAE", vt)
        Path(f.name).unlink()

    def test_phu_luc_that_doc_duoc(self):
        tn, _ = k.doc_phu_luc_e()
        self.assertGreater(len(tn), 100)


if __name__ == "__main__":
    unittest.main()
