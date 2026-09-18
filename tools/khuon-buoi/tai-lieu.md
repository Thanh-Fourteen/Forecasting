<!--
KHUÔN tai-lieu.md — xoá mọi khối chú thích HTML như khối này trước khi xuất PDF.
Dùng khuôn:  cp -r tools/khuon-buoi buoi-NN  → sửa lab/nen.toml → python tools/sinh_nen.py NN
Bắt buộc (CLAUDE.md): đủ 9 mục đúng thứ tự dưới đây; 3.500–6.500 chữ ngoài bảng/code (kiem_de_hieu: do_dai); PDF 10–18 trang
(python tools/xuat_pdf.py NN && python tools/xuat_pdf.py --kiem).
GỌN (D13): mỗi ý nói một lần; khuôn khái niệm dưới đây là TRẦN — chỉ "Ví dụ số nhỏ" + "Tóm lại" bắt buộc, bước nào
không thêm hiểu biết thì bỏ (NumPy + thư viện gộp một khối); "Tóm lại" ≤ 3 câu, không chép lại; Lab/Lỗi thường gặp trỏ
về mục lý thuyết thay vì giải lại. Nghiệm thu thêm bước "Rà gọn" (biên tập viên ≤ 3 chỗ thừa).
CHUẨN DỄ HIỂU (quy tắc D1–D13): đọc tools/CHUAN-DE-HIEU.md (có bài mẫu = buổi 1 mục 4.8) và phan-hoi-hoc-vien.md
TRƯỚC khi viết. Người đọc biết Python + toán phổ thông, chưa học thống kê đại học, tự học một mình.
Kiểm máy: python3 tools/kiem_de_hieu.py NN --chi-tiet. Nghiệm thu: BƯỚC CUỐI "Đọc thử" (0 chặn, ≤ 5 khó).
Các nhãn in đậm dưới đây là CỐ ĐỊNH — bộ kiểm và xuat_pdf.py tìm đúng các chữ này.
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
chỗ, mỗi khái niệm một câu định nghĩa bằng lời + một ví dụ số nhỏ. Đặc biệt nhắc lại khái niệm thống kê nền nếu hôm
nay dùng (phân phối, quantile, phương sai, tương quan, kiểm định/p-value, MAE…): đọc thử cho thấy đây là chỗ chặn
nhiều nhất. Kiến thức nền dùng chung có thể trỏ thêm phu-luc/, không trỏ buoi-NN/. -->

## 3. Trạng thái đầu buổi

<!-- Bảng liệt kê CHÍNH XÁC sau `python lab.py up`, lấy từ output thật:
     `bash lab/00-nen/chuan-bi.sh --tom-tat` in sẵn tệp / số dòng / sha256 rút gọn. -->

| Hạng mục | Trạng thái sau `python lab.py up` |
|---|---|
| Dữ liệu | `lab/du-lieu/raw/<bộ>/<tệp>` — … dòng, từ … đến …, sha256 `…` (12 ký tự) |
| Môi trường | Python 3.12, … (phiên bản từ `lab/00-nen/pyproject.toml`) |
| `code/` có gì | … |
| **Đang cố tình sai** | … — **triệu chứng:** … (con số "đẹp giả tạo" thấy được) |
| `python lab.py check` lúc này | ĐỎ: … test hỏng / … test |

## 4. Lý thuyết

<!-- TỐI ĐA 6 mục ### khái niệm chính (D9). Thừa → hộp "Nâng cao" hoặc "Đọc thêm", KHÔNG nén chữ.
     Mỗi khái niệm theo khuôn D2: Vấn đề → Trực giác → Ví dụ số nhỏ tính tay → Hình → Công thức → Nói bằng lời →
     NumPy (chạy trên CHÍNH ví dụ số nhỏ) → Thư viện → Dữ liệu thật → Tóm lại → Tự kiểm tra.
     Khuôn là TRẦN (D13): bắt buộc chỉ Ví dụ số nhỏ + Tóm lại + Tự kiểm tra; bỏ bước không thêm hiểu biết.
     Câu ≤ ~30 chữ; đoạn ≤ 3 con số kết quả (nhiều hơn → bảng); không trích tiếng Anh chưa dịch; không viết tắt tự chế;
     "thiếu/thừa/cao hơn/sai số dương" luôn nói so với cái gì, đơn vị gì (D4, D6, D7).
     Công thức: $…$ trong dòng, $$…$$ khối riêng. Hình sinh bằng dap-an/ve_hinh.py, tiêu đề hình nói KẾT LUẬN. -->

### Từ mới trong buổi

<!-- Mọi thuật ngữ MỚI của buổi (lấy "Nói đơn giản" + "Ví dụ" từ Phụ lục E; thiếu thì thêm vào E trước). -->

| Thuật ngữ | Nghĩa (một câu, lời thường) | Ví dụ |
|---|---|---|
| … | … | … |

### 4.1 Khái niệm thứ nhất

**Vấn đề.** <!-- Câu hỏi thực tế nào cần khái niệm này? -->

> **Mượn trước — <khái niệm của buổi sau>** (buổi N học kỹ)
>
> <!-- Chỉ khi buộc phải dùng khái niệm chưa dạy: 2–4 câu + ví dụ số nhỏ. Không cần thì xoá hộp này. -->

**Trực giác.** <!-- Ví dụ đời thường. -->

**Ví dụ số nhỏ — tự tính tay.** <!-- 5–10 số; tính mẫu ít nhất một dòng; bảng kết quả + "Đọc bảng". -->

| … | … |
|---|---|
| … | … |

**Đọc bảng.** <!-- So dòng nào với dòng nào, kết luận, vì sao. Không đọc lại từng ô. -->

![Tiêu đề nói kết luận](hinh/vi-du.png)

**Cách đọc hình.**

1. **Trục ngang**: …
2. **Trục dọc**: … (đơn vị)
3. **Ký hiệu**: màu/đường/vạch nào là gì.
4. **Nhìn vào đâu**: …
5. **Kết luận**: …

**Công thức.**

$$
\hat{y}_{T+h|T} = y_T
$$

- $\hat{y}_{T+h|T}$: … <!-- mọi ký hiệu, ngay dưới công thức -->

**Nói bằng lời.** <!-- Một câu diễn đạt công thức, CÓ THAY SỐ từ ví dụ nhỏ. -->

**Tự viết bằng NumPy.**

```python
import numpy as np
# chạy trên đúng bộ số của ví dụ nhỏ, in ra đúng các số đã tính tay
```

**Thư viện.** … <!-- lưu ý chỗ thư viện khác cách tính tay (nội suy, mẫu số T hay T−1…) -->

**Dữ liệu thật.** … <!-- con số từ lần chạy thật; bảng + "Đọc bảng" -->

**Tóm lại.** **…**

**Tự kiểm tra.** … <!-- câu hỏi VẬN DỤNG -->

<details>
<summary>Đáp án</summary>

… <!-- kèm nhầm lẫn hay gặp -->

</details>

> **Nâng cao — có thể bỏ qua lần đọc đầu.**
>
> <!-- Dạng tổng quát, lịch sử, bài báo. Không cần thì xoá hộp này. -->

## 5. Lab từng bước

<!-- Mỗi bước (D11): "Mục đích:" (để làm gì, sẽ thấy gì) → lệnh/code chạy được + output THẬT (rút gọn) →
     "Đọc kết quả:" (thấy X nghĩa là Y; thấy Z thì kiểm lại gì). Tham số lạ trong code giải thích bằng comment.
     Bước cuối: sửa chỗ hở, `python lab.py check` chuyển XANH.
     Code của Lab nằm trong code/lab.ipynb (soạn bằng tools/nb.py, commit không output); tài liệu chỉ trỏ "ô bước N"
     và ghi output cần đọc — không chép lại code dài. Không giải thích cờ lệnh: lệnh phức tạp → thêm vào lab.py. -->

Lệnh gõ trong terminal ở thư mục `lab/`. Code của các bước nằm sẵn trong `code/lab.ipynb`.

### Bước 1 — …

**Mục đích:** …

```bash
python lab.py up           # môi trường + dữ liệu, kiểm sha256
python lab.py notebook     # mở code/lab.ipynb
```

**Đọc kết quả:** …

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

- [ ] `python lab.py check` xanh
- [ ] …

## 9. Đọc thêm

<!-- Chương FPP tương ứng (bảng đối chiếu trong lộ trình) + bài báo gốc + tài liệu thư viện, có link. -->

- Hyndman, R.J., Athanasopoulos, G., et al. *Forecasting: Principles and Practice, the Pythonic Way*,
  chương … — https://otexts.com/fpppy/
