# Công cụ nghiên cứu giá chợ dân sinh

Mở **ToolGiaCho.cmd**. Đây là công cụ độc lập: không sửa game, không build, không ghi public/prices, không tự push lên GitHub.

## Cách dùng

1. Bấm **Tìm bài và lấy dữ liệu**. Công cụ đọc RSS công khai của Tuổi Trẻ, Thanh Niên và những bài gốc đã cấu hình. Mỗi nguồn giới hạn số bài, kiểm tra robots.txt và giãn thời gian truy cập.
2. Chọn bài. Bảng hiện vùng được nhắc tới, ngày đăng, những cụm giá có đơn vị và các điểm cần kiểm tra.
3. Bấm **Mở bài gốc để kiểm tra**. Xác nhận đó là giá bán lẻ tại chợ cụ thể, không phải giá đầu mối, siêu thị hoặc mức tăng/giảm.
4. Nhập khu vực, chợ, mặt hàng, quy cách, ngày khảo sát thực tế, khoảng giá, đơn vị, người đối chiếu. Không rõ ngày khảo sát thì để bài trong danh sách chờ; không lấy ngày đăng thay thế.
5. Đánh dấu đã đối chiếu và bấm **Lưu giá đã đối chiếu**. Kết quả nằm trong verified.csv và verified.json cạnh danh sách ứng viên.

## Độ chính xác và giới hạn

- candidates.json/CSV là bài cần kiểm tra, KHÔNG phải bảng giá được xác nhận. Một số tiền xuất hiện có thể là giá cũ, mức tăng hoặc giá sản phẩm khác; vì vậy công cụ không tự ghép sản phẩm/giá/chợ bằng suy đoán.
- reviewed_today chỉ có nghĩa người đối chiếu đã ghi ngày khảo sát hôm nay. Không chứng minh đây là giá giao dịch của mọi sạp hay giá trung bình thành phố. verified dựa vào việc đối chiếu của người dùng, không phải chứng nhận độc lập.
- Giữ nguyên bó/mớ/gói, không tự đổi kg. Giữ khoảng thấp–cao; không ép thành một mức giá.
- Ngày đăng, ngày khảo sát và lúc truy cập là các trường riêng. Dữ liệu cũ được gắn reviewed_historical, không đổi ngày mới.
- Nguồn hỏng, chặn hoặc thay cấu trúc được ghi trong errors; bài không phù hợp trong skipped. Có thể một ngày không tìm được bài mới hoặc không xác minh được giá nào.
- RSS chỉ là những bài gần đây do báo cung cấp, không bao phủ toàn Internet. Các seed_urls là bài lịch sử để đối chiếu; không coi là dữ liệu hôm nay. Facebook đăng nhập/nhóm riêng không được tự động đọc.
- Không lưu toàn bài hoặc thông tin cá nhân; lưu tiêu đề, URL, các cụm số tiền/đơn vị, băm nội dung và trạng thái. Bài cùng nội dung có cờ duplicate_content trong lần chạy; bản ghi duyệt cùng bài/chợ/mặt hàng/quy cách/ngày/đơn vị được cập nhật thay vì nhân đôi trong file hiện tại.

## File và lịch chạy

Kết quả riêng cho mỗi lần chạy: research/market/YYYY-MM-DD/HH-MM-SS-…/.
Tại đó có candidates.json, candidates.csv; verified.json/CSV xuất hiện sau khi đối chiếu. research/market/last-run.json trỏ tới lần chạy gần nhất.

Từ 27/09/2026, người dùng cho phép lịch Codex 07:15 nghiên cứu và xuất giá đã xác minh lên feed game GitHub. Chỉ xuất khi đủ điều kiện publisher: ngày khảo sát trong hai ngày, ít nhất hai chợ độc lập cùng quy cách và đơn vị. Không có giá đủ điều kiện thì giữ giá mô phỏng. Cần môi trường Codex có thể thực thi lúc đó; công cụ GUI không tự chạy nền khi đóng.

Chạy không mở giao diện: `python pipeline/market_research.py --run`.
Sửa nguồn trong pipeline/market_research_sources.json. Chỉ thêm URL HTTPS trong allowed_hosts và kiểm tra bộ chọn thân bài khi đổi website. Máy hiện tại đã có Python, tkinter và beautifulsoup4; không cần tài khoản API.

Phiên này không hoàn tác những thay đổi game đã có trước đó; chỉ dừng việc chỉnh game và tự xuất dữ liệu vào game. Các file nguồn và bản build game được giữ nguyên trong lần làm công cụ này.
