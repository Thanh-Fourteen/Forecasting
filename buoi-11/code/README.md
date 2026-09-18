# code/ — điểm xuất phát của buổi 11

Code **chạy được** nhưng **cố tình sai** đúng chỗ bài học hôm nay sửa. Một chuỗi "sạch" mất đỉnh Tết không phải chuỗi sạch.

| Tệp | Làm gì |
|---|---|
| `bat_thuong.py` | lượt xem vi.wikipedia (tổng + bài "Tết Nguyên Đán"), hành khách hàng không EU27; z-score/IQR/MAD/Hampel/STL robust; gắn nhãn AO–LS–TC–đổi phương sai; PELT + quét penalty; ba cách xử lý COVID |

**Đang cố tình sai** (triệu chứng nhìn thấy, không nói nguyên nhân):
- chuỗi Tết sau khi làm sạch **mất 10 đỉnh** và thủng 54 mốc
- PELT tìm ra **43 điểm gãy** trên chuỗi hàng không — không ai giải thích nổi từng cái
- cảnh báo "đổi phương sai" rải khắp chuỗi, kể cả chỗ không có gì đổi

Chạy:

```bash
cd lab && python lab.py up          # một lần: môi trường + dữ liệu (~1,6 MB)
python lab.py check                 # bộ chấm: đầu buổi ĐỎ (4/12 hỏng), cuối buổi phải XANH
python lab.py notebook              # mở các tệp .py dưới dạng notebook
python lab.py chay ../code/bat_thuong.py
```

Tệp `.py` viết dạng *percent* (`# %%` tách ô): chạy được như script, mở được như notebook.
Mỗi tệp chỉ định nghĩa hàm ở mức module; phần chạy thử đặt trong `if __name__ == "__main__":`.
