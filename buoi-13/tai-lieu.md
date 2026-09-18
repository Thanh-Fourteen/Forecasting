<!--
KHUÔN tai-lieu.md — xoá mọi khối chú thích HTML như khối này trước khi xuất PDF.
Dùng khuôn:  cp -r tools/khuon-buoi buoi-NN  → sửa lab/nen.toml → python tools/sinh_nen.py NN
Bắt buộc (CLAUDE.md): đủ 9 mục đúng thứ tự dưới đây; 2.500–4.000 chữ; PDF 10–16 trang
(python tools/xuat_pdf.py NN && python tools/xuat_pdf.py --kiem).
Mọi lệnh và MỌI con số lấy từ lần chạy thật (ghi seed). Mọi câu lý thuyết có nguồn trong NGHIEN-CUU.md.
Thuật ngữ theo phu-luc/E-tu-dien-thuat-ngu.md. Buổi tự chứa: không trỏ sang thư mục của buổi khác.
-->

# Buổi NN — Tên chủ đề

## 1. Mục tiêu

<!-- 3–5 gạch đầu dòng, mỗi dòng là một việc LÀM ĐƯỢC và KIỂM ĐƯỢC ("tự viết…", "giải thích vì sao…
bằng một con số"), không phải "hiểu về…". Kết bằng sản phẩm của buổi (bảng tổng quan lộ trình). -->

Sau buổi này bạn:

- …

## 2. Nhắc lại buổi trước

<!-- Đủ để KHÔNG cần mở lại buổi trước: định nghĩa, công thức, kết luận cần dùng hôm nay — viết lại tại
chỗ. Kiến thức nền dùng chung thì trỏ phu-luc/ (vd "xem Phụ lục B, mục Quantile"), không trỏ buoi-NN/. -->

## 3. Trạng thái đầu buổi

<!-- Bảng liệt kê CHÍNH XÁC sau `make up`, lấy từ output thật:
     `bash lab/00-nen/chuan-bi.sh --tom-tat` in sẵn tệp / số dòng / sha256 rút gọn. -->

| Hạng mục | Trạng thái sau `make up` |
|---|---|
| Dữ liệu | `lab/du-lieu/raw/<bộ>/<tệp>` — … dòng, từ … đến …, sha256 `…` (12 ký tự) |
| Môi trường | Python 3.12, … (phiên bản từ `lab/00-nen/pyproject.toml`) |
| `code/` có gì | … |
| **Đang cố tình sai** | … — **triệu chứng:** … (con số "đẹp giả tạo" thấy được) |
| `make check` lúc này | ĐỎ: … test hỏng / … test |

## 4. Lý thuyết

<!-- Mỗi khái niệm theo nhịp: trực giác → hình → công thức → tự viết bằng NumPy → thư viện.
     Công thức: $…$ trong dòng, $$…$$ khối riêng. Hình: ![mô tả](hinh/ten.png), sinh bằng dap-an/ve_hinh.py,
     tiêu đề hình nói KẾT LUẬN; dưới mỗi hình ghi "đọc ra gì, ở chỗ nào trên hình". -->

### 4.1 Khái niệm thứ nhất

**Trực giác.** …

![Tiêu đề nói kết luận](hinh/vi-du.png)

**Công thức.**

$$
\hat{y}_{T+h|T} = y_T
$$

**Tự viết bằng NumPy.**

```python
import numpy as np
```

**Thư viện.** …

## 5. Lab từng bước

<!-- Mỗi bước: lệnh/đoạn code chạy được + output THẬT (rút gọn) + câu hỏi "vì sao ra con số này".
     Bước cuối: sửa chỗ hở, `make check` chuyển XANH. -->

### Bước 1 — …

```bash
cd lab && make up
```

## 6. Lỗi thường gặp & cách chẩn đoán

<!-- Lấy từ research (NGHIEN-CUU.md) + chỗ học viên hay tắc. Mỗi dòng có TRIỆU CHỨNG nhìn thấy được. -->

| Triệu chứng | Nguyên nhân | Chẩn đoán | Sửa |
|---|---|---|---|
| … | … | … | … |

## 7. Bài tập về nhà

<!-- 2–4 bài, có bài dùng dữ liệu KHÁC dữ liệu lab (trong du-lieu.toml của buổi), có tiêu chí đạt đo được. -->

1. …

## 8. Tiêu chí "Xong khi"

<!-- Lấy từ "Xong khi" của buổi trong lộ trình, đo được. -->

- [ ] `make check` xanh
- [ ] …

## 9. Đọc thêm

<!-- Chương FPP tương ứng (bảng đối chiếu trong lộ trình) + bài báo gốc + tài liệu thư viện, có link. -->

- Hyndman, R.J., Athanasopoulos, G., et al. *Forecasting: Principles and Practice, the Pythonic Way*,
  chương … — https://otexts.com/fpppy/
