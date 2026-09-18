# code/ — điểm xuất phát của buổi 1

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Đừng tin kết quả đẹp.

| Tệp | Làm gì |
|---|---|
| `lab.ipynb` | notebook của Lab (bước 1, 2, 4, 5) — mở bằng JupyterLab hoặc VS Code |
| `danh_gia.py` | đọc điện theo giờ (kWh), "mô hình" bảng lịch, bốn hàm baseline, dự báo cuốn theo tuần, bảng MAE — **tệp bạn sửa** |
| `kiem_tra_moi_truong.py` | in phiên bản Python, thư viện và kiểm tệp dữ liệu |
| `phieu-bai-toan.md` | mẫu phiếu bài toán 6 ô — điền cho 3 tình huống (bước 3) |

**Đang cố tình sai:** `danh_gia()` báo MAE 0,380 kWh/giờ cho năm 2010, và bảng chỉ có một dòng nên không có gì để so.

**Bạn cần làm** (tài liệu mục 5, bước 5): sửa `du_bao_cuon` để tại mỗi gốc (00:00 thứ Hai) mọi dự báo chỉ dùng dữ liệu
**trước** gốc (mục 4.4), và thêm bốn cột baseline "trung bình 4 tuần", "tuần trước", "trung bình", "giờ trước" (mục 4.3;
đúng tên cột, bộ chấm tìm theo tên). Xong thì bảng lịch còn khoảng 0,5 kWh/giờ và thua ít nhất một baseline.

Lệnh (trong `lab/`):

```bash
python lab.py up           # một lần: môi trường + dữ liệu (~20 MB tải), kiểm sha256
python lab.py notebook     # mở JupyterLab ở code/
python lab.py check        # bộ chấm: đầu buổi ĐỎ (4/8 test hỏng), cuối buổi phải XANH
```

Dùng conda thay uv: bật môi trường Python 3.12 của bạn rồi `python lab.py up --pip`. Phần chạy thử của `danh_gia.py`
nằm trong `if __name__ == "__main__":` để bộ chấm nạp tệp nhanh.
