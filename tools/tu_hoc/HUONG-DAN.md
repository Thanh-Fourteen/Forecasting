# Notebook tự học — hướng dẫn soạn

`buoi-NN/tu-hoc.ipynb` là bản **ôn gọn, dễ hiểu, đủ ý** của một buổi: lý thuyết viết lại + code đáp án chạy trên dữ
liệu thật, tự chứa (không import `dap-an/`, `code/`, `tv`). Nguồn là `tools/tu_hoc/buoi_NN.py`; notebook được
commit (không output, ảnh nhúng sẵn) nhưng `dong_goi.py` lọc khỏi zip phát cho học viên vì chứa code đáp án.

## Quy trình một buổi

```bash
python tools/tu_hoc/sinh.py --thieu            # buổi đã soạn mà chưa có notebook — việc nền đầu mọi phase (quy-uoc.md)
python tools/tu_hoc/moi_truong.py N            # môi trường + kernel dùng chung của hồ sơ buổi N (một lần)
python tools/tu_hoc/sinh.py N --khung          # dựng tools/tu_hoc/buoi_NN.py từ tai-lieu.md, chỗ cần viết ghi TODO
#   … viết nội dung: thay mọi TODO; thêm mô tả bộ dữ liệu mới vào du_lieu.toml nếu sinh.py báo thiếu
python tools/tu_hoc/sinh.py N --chay           # sinh + chạy hết các ô, in output → so từng con số với tai-lieu.md
python tools/tu_hoc/sinh.py --tat-ca --chay    # sinh lại mọi buổi đã có (sau khi sửa sinh.py)
```

Nguồn để viết: `buoi-NN/tai-lieu.md` (ý và con số), `buoi-NN/dap-an/*.py` (code đúng — chép phần cần vào ô, bỏ phụ
thuộc `tv`), `dap-an/vi_du_nho.py` (số của ví dụ tay), `NGHIEN-CUU.md` (cách tính các con số dữ liệu thật).

## Văn phong (người dùng chốt 2026-09-28)

- **Viết lại, không chép tài liệu.** Mở bằng "**Một câu:**" tóm cả buổi + tình huống thật; bảng các phần.
- **Mỗi phần** `## N. <tiêu đề nói KẾT LUẬN>` theo khuôn **Vấn đề.** → **Lý do.** → **Kết quả.** (1–2 ô code chạy thật,
  rồi 1–3 câu đọc kết quả) → **Bài học.** Mỗi bước 1–3 câu; một ví dụ cho một ý; không lặp ý giữa các phần.
- **Khái niệm mới**: mỗi từ trong bảng "Từ mới trong buổi" có một `nb.khai_niem(ten, en, la_gi, vi_du, de_lam_gi)`,
  gọi ngay trước `nb.md` của phần dùng nó lần đầu (hộp hiện sau "Vấn đề", trước "Lý do"). Hộp mở bằng
  "**tên** · *English*" — không lặp nhãn "Khái niệm mới". Ví dụ có số cụ thể; "để làm gì" nói nó giúp gì cho dự báo.
  Hộp đã định nghĩa thì thân bài không định nghĩa lại.
- **Hình (quy tắc D14)**: khái niệm có hình dạng (phân phối, histogram, mùa vụ, dự báo cuốn, giờ mùa hè…) có một mục
  trong bảng `HINH = {tên hộp: {"doc": …, "sau": …, "ve": code}}`:
  - `ve`: code matplotlib vẽ lên `ax` có sẵn (hoặc tự `fig, ... = plt.subplots(...)`), dữ liệu tự tạo có seed, tiêu đề
    hình nói kết luận;
  - `doc`: "Cách đọc hình" 1–2 câu (trục + kết luận; ≤ 3 con số);
  - `sau`: đoạn văn trong `tai-lieu.md` (xuất hiện đúng 1 lần) — hình chèn ngay sau đoạn đó; `None` nếu tài liệu đã có
    hình cùng ý (hình chỉ vào notebook).

  sinh.py ghi `buoi-NN/dap-an/ve_hinh_khai_niem.py` (tự chứa, chạy lại được), vẽ `buoi-NN/hinh/kn-*.png`, nhúng vào hộp
  notebook, chèn (lại) vào `tai-lieu.md` và **xuất lại PDF** khi tài liệu đổi. Chạy lại không chèn trùng. **Xem lại từng
  hình** (trong notebook và PDF) trước khi giao; `kiem_de_hieu.py N` không được có lỗi mới do hình.
- **Con số**: mọi số trong phần chữ lấy từ output thật (`--chay`); số minh hoạ tự đặt thì ghi "(số minh hoạ)".
- **Không câu meta**: không nói import gì, kernel, đường dẫn repo, "mục 4.3", "Lab bước N", `lab.py check`.

## sinh.py tự kiểm (dừng nếu sai)

| Kiểm | Khai báo trong buoi_NN.py |
|---|---|
| mọi mục `### 4.x` và mọi bài tập về nhà có phần tương ứng | `DU_Y = {"4.1": 1, …, "BT1": 7, "BT2": "lý do bỏ"}` |
| phần lý thuyết đủ 4 nhãn Vấn đề / Lý do / Kết quả / Bài học | — |
| mọi từ mới có hộp khái niệm | `BO_TU = {"từ": "lý do bỏ"}` nếu cố ý bỏ |
| tên trong `HINH` khớp một hộp | `HINH = {tên hộp: code}` |
| bộ dữ liệu có mô tả | `tools/tu_hoc/du_lieu.toml` (khoá = tên bộ, hoặc mẫu `*` cho một họ) |
| không còn `TODO` | — |

## Môi trường

Ba hồ sơ dùng chung (`moi_truong.py --liet-ke`): `pandas3`, `nixtla` (pandas 2.3.3), `autogluon`. Venv ở
`~/.cache/khoa-forecasting/tu-hoc/<hồ sơ>/`, kernel `khoa-tu-hoc-<hồ sơ>` ghi sẵn trong notebook. Phiên bản lấy từ
`tools/nen/phien-ban.toml` nên số khớp venv của lab. `--chay` chạy dưới `systemd-run MemoryMax=6G`.
