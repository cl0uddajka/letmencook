# Đồng bộ giá chợ vào game — v0.7.0

## Tình trạng thực tế

5 bản ghi lịch sử tại Bà Chiểu hiện KHÔNG đạt tiêu chuẩn phát hành. Hà Nội chưa có dữ liệu đạt. Bảng public/prices/latest.json có hai vùng nhưng danh sách giá trống. Game dùng giá mô phỏng cho đến khi có dữ liệu hợp lệ. Không có bảo đảm rằng mỗi ngày Internet sẽ cung cấp đủ giá khảo sát.

## Quy trình

1. Lịch Codex lúc 07:15 giờ Việt Nam tìm nguồn, kiểm tra và cập nhật data/market-prices/latest.json. Lịch này cần môi trường Codex có thể thực thi và truy cập mạng; không phải máy chủ hoạt động liên tục.
2. Sau khi kiểm tra nguồn, quy cách hàng và đơn vị, bản ghi có approved=true, reviewed_by, surveyed_on thực tế. Ngày đăng báo không thay thế ngày khảo sát. Không duyệt chỉ để làm đầy bảng.
3. Chạy XuatGiaGame.cmd hoặc python pipeline/publish_prices.py. Kết quả: public/prices/latest.json, quality-report.json và history/YYYY-MM-DD.json.
4. Bộ xuất chỉ nhận giá bán lẻ chợ, ngày khảo sát hôm nay hoặc hai ngày trước, tối thiểu hai chợ độc lập cùng mặt hàng/quy cách. Trung vị theo từng chợ rồi trung vị giữa các chợ. Khác quy cách hoặc chênh lệch quá lớn bị loại. Đây là tiêu chí thận trọng của dự án, không phải chứng nhận giá chính thức.
5. Game tải JSON khi mở và kiểm tra lại mỗi giờ trong lúc chạy. Tải thành công được lưu cục bộ. Giá mới chỉ áp dụng khi mở bảng chọn món tại nhà; giữ nguyên giá trong chuyến đi. Hết hạn hoặc lỗi thì mặt hàng quay về giá mô phỏng ở lần áp dụng tiếp theo.

## GitHub

Đã kết nối repository công khai https://github.com/cl0uddajka/letmencook, nhánh main. Đã đẩy bảng JSON và workflow. Giữ nguyên file datamarket hiện có.

Tạo repository công khai chuyên cho giá rồi đưa lên: pipeline/publish_prices.py, pipeline/test_publish_prices.py, data/market-prices/latest.json, public/prices và workflow. Đừng đưa khóa ký, password.dpapi, dữ liệu người chơi hay toàn bộ thư mục cá nhân lên GitHub. Bật Actions với quyền Read and write cho workflow. Mỗi lần push dữ liệu nguồn hoặc chạy workflow thủ công, workflow kiểm tra rồi commit bảng giá xuất ra.

Workflow không tự tìm bài báo. Lịch Codex đảm nhiệm nghiên cứu nguồn; việc đẩy kết quả lên GitHub cần repo/quyền đã kết nối. Nếu chưa kết nối thì chỉ cập nhật file local, game chưa có nguồn mạng.

Địa chỉ mẫu (thay OWNER, REPO, BRANCH thực):

https://raw.githubusercontent.com/cl0uddajka/letmencook/main/public/prices/latest.json

Trong game: về nhà → Chọn món → Khu vực & giá chợ → chọn Hà Nội hoặc TP.HCM → dán URL HTTPS → Lưu & tải. Chờ tải rồi mở lại bảng chọn món để áp dụng. URL phải trả JSON trực tiếp, không phải trang xem file github.com. Không nhập token; game chỉ dùng endpoint công khai. Có thể dùng HTTPS hosting khác thay GitHub.

## Thông tin cần biết

- Bảng trên HUD hiển thị khu vực và số mặt hàng có giá tham khảo.
- Mặt hàng chưa có dữ liệu dùng giá mô phỏng, không được quảng bá là giá thực tế.
- Giá chuẩn kg/lít/quả được đổi sang lượng bán của game; các sạp vẫn có chênh lệch mô phỏng như trước.
- Có thể cập nhật dữ liệu mà không build lại APK khi đã cấu hình URL.
- Bản này thêm quyền Internet. Endpoint nhìn thấy IP và thông tin kết nối khi game tải file, nhưng game không gửi ví, túi đồ hay món chọn. Chính sách riêng tư/Data safety cần phản ánh việc tải dữ liệu và nhà cung cấp hosting trước khi phát hành.
- Đã kiểm tra Godot tải được JSON thật từ GitHub qua HTTPS. Chưa thử trên điện thoại thật.

## Trạng thái triển khai hiện tại

Game mặc định dùng URL raw GitHub ở trên. Lịch Codex 07:15 tìm nguồn, xuất và chạy pipeline/publish_github.py để đẩy dữ liệu mỗi ngày. Máy cần sẵn sàng cho Codex chạy; GitHub Workflow chỉ tái xuất khi nhận dữ liệu mới hoặc chạy thủ công, không tự nghiên cứu giá. Chạy XuatGiaGame.cmd chỉ xuất local; chạy python pipeline/publish_github.py sẽ xuất và đẩy dữ liệu đã được cho phép. Bảng hiện trống vì không có giá đạt ngưỡng, không phải lỗi kết nối.
