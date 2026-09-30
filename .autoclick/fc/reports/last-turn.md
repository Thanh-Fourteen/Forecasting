# lượt gần nhất

_2026-09-29 16:25:21_

Tôi đã sửa slide 82 trong v2.

- **Phần tính tay:** xoá hẳn bảng và đoạn tính r1, r2, theo ý bạn.
- **Tiêu đề mới:** "Ba hình dạng ACF cần nhận ra", câu nhớ nhanh giữ nguyên.
- **Hình minh họa:** ba cột nhiễu trắng / random walk / mùa vụ 24 giờ. Hàng trên là chuỗi, hàng dưới là ACF của chuỗi đó, dải xám là ±1,96/√T. Ở chuỗi mùa vụ, ACF có đỉnh ở 24, 48 và âm ở 12, 36.
- **Ba thẻ dưới hình:** rút ngắn thẻ nhiễu trắng để không tràn chữ khi mở bằng PowerPoint.
- **Lời thuyết trình và bài đọc kèm:** viết lại theo hình mới.

Trong `buoi-07/hinh/` không có hình nào vẽ đủ cả ba dạng cạnh nhau. Vì vậy script tự vẽ hình này mỗi lần sinh slide, từ ba chuỗi mô phỏng có seed 7, giống cách nó đang vẽ ảnh công thức. Hình này chưa có trong `tai-lieu.md` của buổi 7.

Tôi đã sinh lại bộ slide (vẫn 259 slide) và xem hình render của slide 82. Lint không báo lỗi.

Thay đổi này và phần sửa buổi 7 lúc nãy đều **chưa commit**. Bạn xem lại slide 82 trong PowerPoint, được thì tôi commit và push.
