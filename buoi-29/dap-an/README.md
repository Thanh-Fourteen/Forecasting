# dap-an/ — bản đã sửa (KHÔNG vào zip phát học viên)

Cùng tên tệp, cùng chữ ký hàm với `code/`. `python lab.py check --dap-an` phải xanh 6/6.

- `hoc_sau.py`: `hoc_scaler` chỉ học trên `ds < MOC_VAL`; `chia_train_val` chia theo thời gian rồi mới cắt cửa sổ (train: mục tiêu trước
  `MOC_VAL`, val: mục tiêu trong [`MOC_VAL`, `MOC_TEST`)).
- `ve_hinh.py`: sinh `../hinh/*.png` và in mọi con số của tài liệu — chạy trong `lab/`: `python lab.py chay ../dap-an/ve_hinh.py` (~15 phút).
