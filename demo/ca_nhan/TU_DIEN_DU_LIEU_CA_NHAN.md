# Từ điển dữ liệu khách hàng cá nhân — Ngân hàng FTA

Bộ dùng trên lớp: 200 khách hàng, 256 sổ tiền gửi, 58 hợp đồng vay, 18.823 giao dịch trong 12 tháng năm 2026.

- Mốc dữ liệu: 31/12/2026.
- Đơn vị tiền: **đồng**.
- Mọi số liệu là mô phỏng, không phải dữ liệu thật của tổ chức nào.

## Danh sách tệp

| Tệp | Một dòng là | Dùng ở tiết |
|---|---|---|
| `khach_hang_raw.csv` | 1 khách hàng (bản chưa làm sạch) | 1 |
| `so_tiet_kiem.csv` | 1 sổ tiền gửi | 5, 9 |
| `khoan_vay.csv` | 1 hợp đồng vay tại FTA | 5, 6, 7 |
| `sao_ke/sao_ke_2026_MM.csv` | 1 giao dịch (12 tệp, mỗi tháng 1 tệp) | 2, 5, 6 |
| `de_nghi_vay_ca_nhan.csv` | 1 hồ sơ đề nghị vay | 6 |
| `bao_cao_cic_ca_nhan.csv` | 1 báo cáo thông tin tín dụng của khách có hồ sơ đề nghị | 6 |
| `danh_sach_canh_bao_ca_nhan.csv` | 1 số giấy tờ bị cảnh báo | 5, 6 |
| `tai_san_bao_dam_ca_nhan.csv` | 1 tài sản bảo đảm | 9 |
| `lich_su_vay_ca_nhan.csv` | 1 khoản vay đã giải ngân các năm 2021–2025 | 8 |

## `khach_hang_raw.csv`

Bản này **cố ý để bẩn**: có dòng trùng, có ô để trống, có ngày sinh sai định dạng, có họ tên thừa khoảng trắng và viết hoa toàn bộ.

| Cột | Ý nghĩa |
|---|---|
| `ma_kh` | Mã khách hàng |
| `ho_ten` | Họ và tên |
| `ngay_sinh` | Ngày sinh, dùng để tính tuổi |
| `gioi_tinh` | Nam hoặc Nữ |
| `so_giay_to` | Số giấy tờ định danh |
| `tinh_thanh` | Tỉnh, thành phố |
| `nghe_nghiep` | Nghề nghiệp khai báo |
| `phan_khuc` | Phân khúc đang ghi trong hệ thống, gán từ khi mở quan hệ, nhiều năm chưa rà soát |
| `loai_khach_hang` | Cá nhân |
| `chi_nhanh_quan_ly` | Chi nhánh quản lý |
| `ngay_mo_quan_he` | Ngày mở quan hệ, dùng để tính thâm niên |
| `kenh_dang_ky` | Tại quầy hoặc Trực tuyến |
| `trang_thai` | Đang hoạt động, Ngừng giao dịch, hoặc Đã đóng |
| `canh_bao_gian_lan` | Có hoặc Không: cờ cảnh báo gian lận của FTA |
| `cong_nhan_dac_biet` | Có hoặc Không: khách được khối kinh doanh công nhận theo chương trình riêng |
| `dien_thoai`, `email` | Thông tin liên hệ |

## `so_tiet_kiem.csv`

| Cột | Ý nghĩa |
|---|---|
| `so_so` | Số sổ |
| `ma_kh` | Mã khách hàng |
| `loai_khach_hang`, `chi_nhanh` | Loại khách hàng, chi nhánh mở sổ |
| `so_tien_goc` | Số tiền gửi |
| `ngay_mo_lan_dau` | Ngày mở sổ |
| `ky_han_thang`, `ngay_dao_han` | Kỳ hạn (tháng), ngày đến hạn của kỳ đang chạy tại ngày 31/12/2026. Một kỳ dài 30, 91, 182, 364, 729 ngày ứng với kỳ hạn 1, 3, 6, 12, 24 tháng |
| `tu_dong_tai_tuc` | Có tự động tái tục hay không. Sổ đã qua ít nhất 1 lần đến hạn đều ghi "Có" |
| `hinh_thuc_gui` | Gửi tại quầy hay trực tuyến |
| `ky_thu` | Kỳ gửi thứ mấy của sổ |
| `ngay_hieu_luc_ky_hien_tai` | Ngày bắt đầu kỳ gửi đang chạy |
| `trang_thai` | Trạng thái sổ |

## `khoan_vay.csv`

| Cột | Ý nghĩa |
|---|---|
| `so_hop_dong` | Số hợp đồng |
| `ma_kh` | Mã khách hàng |
| `chi_nhanh` | Chi nhánh cho vay |
| `san_pham_vay` | Sản phẩm vay |
| `ngay_giai_ngan` | Ngày giải ngân |
| `so_tien_vay` | Số tiền vay ban đầu |
| `ky_han_thang` | Kỳ hạn |
| `lai_suat_nam_pct` | Lãi suất năm, tính theo phần trăm |
| `so_ky_da_tra` | Số kỳ đã trả |
| `ky_tra_no_hang_thang` | Số tiền phải trả mỗi kỳ |
| `du_no_goc` | Dư nợ gốc hiện tại |
| `tai_san_bao_dam` | Có hoặc Không |
| `nhom_no`, `so_ngay_qua_han` | Nhóm nợ (1–5) và số ngày quá hạn |
| `ngay_den_han_ky_toi` | Ngày đến hạn của kỳ trả nợ tiếp theo, chỉ có ý nghĩa với khoản đang hiệu lực |
| `trang_thai` | Đang hiệu lực hoặc Đã tất toán |

Khoản đã tất toán giữ nhóm nợ và số ngày quá hạn trong thời hạn lưu lịch sử nợ: 1 năm với nợ nhóm 2; 5 năm với nợ nhóm 3 đến 5, kể từ ngày tất toán. Quá thời hạn đó thì lịch sử đã được xóa.

## `sao_ke/sao_ke_2026_MM.csv`

| Cột | Ý nghĩa |
|---|---|
| `ma_giao_dich` | Mã giao dịch |
| `ngay_gio` | Thời điểm giao dịch |
| `ma_kh` | Mã khách hàng |
| `kenh` | Mobile Banking, Internet Banking, QR Code, ATM, POS, Quầy giao dịch |
| `loai_giao_dich` | Nhận lương, Chuyển khoản đi, Chuyển khoản đến, Rút tiền mặt, Nộp tiền mặt, Thanh toán thẻ, Thanh toán hóa đơn, Nạp tiền điện thoại |
| `so_tien` | Số tiền giao dịch |
| `phi` | Phí của giao dịch |
| `trang_thai` | Thành công hoặc Thất bại |
| `chi_nhanh` | Chi nhánh phát sinh |
| `so_du_sau_giao_dich` | Số dư tài khoản thanh toán ngay sau giao dịch |

Thu nhập lương qua FTA không ghi sẵn ở tệp nào. Thu nhập lương bình quân tháng tính từ các giao dịch "Nhận lương" thành công.

## `de_nghi_vay_ca_nhan.csv`

| Cột | Ý nghĩa |
|---|---|
| `ma_ho_so` | Mã hồ sơ đề nghị |
| `ma_kh` | Mã khách hàng |
| `ngay_de_nghi` | Ngày nộp đề nghị |
| `san_pham` | Vay tiêu dùng tín chấp; Vay mua nhà; Vay mua ô tô; Vay sản xuất kinh doanh; Vay cầm cố sổ tiết kiệm |
| `muc_dich` | Mục đích vay |
| `so_tien_de_nghi` | Số tiền khách hàng đề nghị |
| `ky_han_thang` | Thời hạn vay đề nghị (tháng) |
| `lai_suat_nam_pct` | Lãi suất năm dự kiến của sản phẩm, tính theo phần trăm; trả góp đều hằng tháng |
| `thu_nhap_khai_bao` | Thu nhập tháng do khách tự khai |
| `thu_nhap_khac_xac_minh` | Thu nhập tháng ngoài lương qua FTA đã được xác minh bằng giấy tờ; 0 nếu không có |
| `hinh_thuc_xac_minh` | Lương qua FTA; Lương qua FTA và sao kê ngân hàng khác; Sao kê ngân hàng khác; Giấy tờ kinh doanh, sổ sách thuế; Chưa xác minh |

Thu nhập đã xác minh = lương bình quân tháng qua FTA (tính từ sao kê) + `thu_nhap_khac_xac_minh`.

## `bao_cao_cic_ca_nhan.csv`

Báo cáo thông tin tín dụng tra cứu ngày 31/12/2026 cho khách có hồ sơ đề nghị. Nhóm nợ tính trên mọi tổ chức tín dụng, kể cả FTA.

| Cột | Ý nghĩa |
|---|---|
| `ma_ho_so`, `ma_kh` | Hồ sơ và khách hàng |
| `ngay_bao_cao` | Ngày tra cứu |
| `so_tctd_khac_dang_vay` | Số tổ chức tín dụng khác (ngoài FTA) đang có dư nợ |
| `du_no_tctd_khac` | Dư nợ tại các tổ chức tín dụng khác |
| `nghia_vu_tra_no_thang_tctd_khac` | Số tiền phải trả hằng tháng tại các tổ chức tín dụng khác |
| `nhom_no_hien_tai` | Nhóm nợ cao nhất hiện tại tại mọi tổ chức tín dụng |
| `nhom_no_cao_nhat_con_luu` | Nhóm nợ cao nhất còn lưu trong lịch sử, theo thời hạn lưu (1 năm với nhóm 2; 5 năm với nhóm 3–5) |
| `so_lan_hoi_tin_6_thang` | Số lần tổ chức tín dụng tra cứu thông tin của khách trong 6 tháng |

## `danh_sach_canh_bao_ca_nhan.csv`

| Cột | Ý nghĩa |
|---|---|
| `so_giay_to` | Số giấy tờ định danh bị cảnh báo (có cả người không phải khách hàng FTA) |
| `ly_do_canh_bao` | Lý do |
| `ngay_cap_nhat` | Ngày đưa vào danh sách |

## `tai_san_bao_dam_ca_nhan.csv`

| Cột | Ý nghĩa |
|---|---|
| `ma_ho_so`, `ma_kh` | Hồ sơ và khách hàng |
| `stt_tai_san` | Thứ tự tài sản trong hồ sơ |
| `loai_tai_san` | Bất động sản là nhà ở, đất ở; Phương tiện vận tải mới; Tiền gửi, sổ tiết kiệm bằng đồng Việt Nam tại FTA |
| `ma_loai_tai_san` | Mã viết tắt, cùng bảng mã với dữ liệu doanh nghiệp: `BDS_NHA_O`, `PTVT_MOI`, `TG_FTA` |
| `so_so_tiet_kiem` | Số sổ tiết kiệm được cầm cố (nối sang `so_tiet_kiem.csv`) |
| `chu_so_huu` | Khách hàng, hoặc bên thứ ba (vợ, chồng hoặc người thân) |
| `gia_tri_dinh_gia` | Giá trị do FTA định giá |
| `ngay_dinh_gia` | Ngày định giá |

Vay tiêu dùng tín chấp không có tài sản bảo đảm. Vay mua nhà, vay mua ô tô dùng chính tài sản hình thành từ vốn vay làm bảo đảm.

## `lich_su_vay_ca_nhan.csv`

Khoản vay cá nhân đã giải ngân các năm 2021–2025. Thông tin là thông tin tại thời điểm giải ngân; nhãn là kết quả trả nợ trong 12 tháng sau giải ngân.

| Cột | Ý nghĩa |
|---|---|
| `ma_ho_so`, `nam_giai_ngan` | Mã hồ sơ, năm giải ngân |
| `san_pham`, `tuoi`, `nghe_nghiep` | Sản phẩm, tuổi, nghề nghiệp |
| `thu_nhap_thang` | Thu nhập tháng đã xác minh |
| `co_luong_qua_fta` | Có nhận lương qua FTA hay không |
| `tham_nien_quan_he_thang` | Số tháng quan hệ với FTA |
| `ty_le_nghia_vu_tra_no` | Tổng nghĩa vụ trả nợ hằng tháng (kể cả khoản vay này) / thu nhập |
| `ty_le_cho_vay_tren_tai_san` | Số tiền vay / giá trị tài sản bảo đảm; để trống với vay tín chấp |
| `nhom_no_cao_nhat_con_luu` | Nhóm nợ cao nhất còn lưu theo CIC |
| `so_lan_qua_han_12_thang` | Số lần quá hạn trong 12 tháng trước khi vay |
| `so_ngay_qua_han_lon_nhat` | Số ngày quá hạn lớn nhất trong thời gian CIC còn lưu thông tin; 0 nếu chưa từng quá hạn |
| `da_tung_vay` | Đã từng vay tại FTA hoặc tổ chức tín dụng khác trước khoản vay này hay chưa ("Không" là hồ sơ mỏng) |
| `so_du_tktt_binh_quan_3_thang` | Số dư tài khoản thanh toán bình quân 3 tháng |
| `tien_gui_tiet_kiem` | Tiền gửi tiết kiệm tại FTA lúc giải ngân; 0 nếu không có |
| `co_giao_dich_3_thang` | Có giao dịch trong 3 tháng trước khi giải ngân hay không |
| `xau_12_thang` | 1 nếu khoản vay chuyển sang nhóm 3–5 trong 12 tháng sau giải ngân; 0 nếu không |
