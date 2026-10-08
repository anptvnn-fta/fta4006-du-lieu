# Từ điển dữ liệu khách hàng doanh nghiệp — Ngân hàng FTA

Toàn bộ số liệu là **mô phỏng**, dùng cho học tập. Tên doanh nghiệp, mã số thuế, người đại diện, điện thoại, email đều sinh tự động; mã số thuế bắt đầu bằng chữ số 9 để không trùng mã số thuế thật.

- Mốc dữ liệu: 31/12/2026.
- Báo cáo tài chính: các năm 2023, 2024, 2025.
- Đơn vị tiền: **triệu đồng**, trừ khi cột `don_vi` ghi khác.
- Dữ liệu khách hàng doanh nghiệp tách riêng với dữ liệu khách hàng cá nhân.

## Danh sách tệp

| Tệp | Một dòng là | Dùng ở tiết |
|---|---|---|
| `doanh_nghiep_raw.csv` | 1 doanh nghiệp (bản chưa làm sạch) | 3, 5, 6, 7, 9 |
| `bctc_dn.csv` | 1 doanh nghiệp × 1 năm báo cáo | 3, 5, 7, 9 |
| `sao_ke_dn_thang.csv` | 1 doanh nghiệp × 1 tháng năm 2026 | 7 |
| `quan_he_tin_dung_dn.csv` | 1 doanh nghiệp | 5, 6, 7, 9 |
| `danh_sach_canh_bao_dn.csv` | 1 mã số thuế | 5, 6 |
| `de_nghi_vay_dn.csv` | 1 hồ sơ đề nghị cấp hạn mức | 7, 9 |
| `tai_san_bao_dam_dn.csv` | 1 tài sản bảo đảm | 9 |
| `lich_su_dn.csv` | 1 hồ sơ đã được cấp hạn mức các năm 2021–2025 | 8 |
| `quy_dinh/nguong_cham_diem_dn.csv` | 1 chỉ tiêu × 1 ngành × 1 quy mô | 6 |
| `quy_dinh/ty_le_cho_vay_tsbd.csv` | 1 loại tài sản bảo đảm | 9 |

## `doanh_nghiep_raw.csv`

Bản chưa làm sạch: có dòng trùng, có cách ghi ngành không thống nhất, có tên ghi thừa khoảng trắng.

| Cột | Ý nghĩa |
|---|---|
| `ma_kh` | Mã khách hàng doanh nghiệp tại FTA, dạng DN00001 |
| `ten_doanh_nghiep` | Tên doanh nghiệp |
| `ma_so_thue` | Mã số thuế (10 chữ số, mô phỏng) |
| `loai_hinh_doanh_nghiep` | Công ty TNHH một thành viên; Công ty TNHH hai thành viên trở lên; Công ty cổ phần; Doanh nghiệp tư nhân |
| `loai_hinh_so_huu` | Nhà nước; Ngoài nhà nước; Có vốn đầu tư nước ngoài |
| `nganh_chinh` | Ngành, nghề kinh doanh chính đã đăng ký, theo 4 ngành chấm điểm của FTA: Thương mại và dịch vụ; Công nghiệp; Xây dựng; Nông, lâm nghiệp và thủy sản |
| `tieu_nhom_nganh` | Tiểu nhóm để phân tích (không dùng để chấm điểm), ví dụ "Bán buôn, bán lẻ", "Dịch vụ khác" |
| `nam_thanh_lap` | Năm thành lập |
| `lao_dong_bhxh_binh_quan` | Số lao động tham gia bảo hiểm xã hội bình quân năm 2025 (người) |
| `tinh_thanh` | Tỉnh, thành nơi đặt trụ sở |
| `chi_nhanh_quan_ly` | Chi nhánh FTA quản lý khách hàng |
| `ngay_mo_quan_he` | Ngày bắt đầu quan hệ với FTA |
| `nguoi_dai_dien_theo_phap_luat` | Họ tên người đại diện theo pháp luật |
| `kinh_nghiem_dieu_hanh_nam` | Số năm kinh nghiệm của người điều hành trong ngành |
| `che_do_ke_toan` | Chế độ kế toán áp dụng cho các năm 2023–2025 |
| `co_kiem_toan` | Báo cáo tài chính có được kiểm toán độc lập: Có / Không |
| `nhom_bao_cao` | Đủ: có báo cáo tài chính từ 2 năm liền kề trở lên. Không đủ: chưa đủ 2 năm báo cáo, hoặc chỉ có tờ khai thuế |
| `trang_thai` | Đang hoạt động; Ngừng giao dịch; Đã đóng |
| `dien_thoai`, `email` | Liên hệ |

## `bctc_dn.csv`

Báo cáo tài chính rút gọn. Doanh nghiệp chỉ có tờ khai thuế thì chỉ có cột doanh thu thuần.

| Cột | Ý nghĩa |
|---|---|
| `ma_kh`, `nam` | Mã khách hàng, năm báo cáo |
| `nguon_so_lieu` | BCTC đã kiểm toán; BCTC chưa kiểm toán; Tờ khai thuế |
| `don_vi` | Đơn vị của các cột số trên dòng: triệu đồng hoặc đồng |
| `tien` | Tiền và các khoản tương đương tiền |
| `phai_thu_khach_hang` | Phải thu ngắn hạn của khách hàng |
| `hang_ton_kho` | Hàng tồn kho |
| `tai_san_ngan_han_khac` | Tài sản ngắn hạn khác |
| `tai_san_ngan_han` | Tổng tài sản ngắn hạn |
| `tai_san_co_dinh` | Tài sản cố định |
| `tai_san_dai_han_khac` | Tài sản dài hạn khác |
| `tai_san_dai_han` | Tổng tài sản dài hạn |
| `tong_tai_san` | Tổng tài sản |
| `phai_tra_nguoi_ban` | Phải trả người bán ngắn hạn |
| `vay_ngan_han` | Vay và nợ thuê tài chính ngắn hạn |
| `no_ngan_han_khac` | Nợ ngắn hạn khác |
| `no_ngan_han` | Tổng nợ ngắn hạn |
| `vay_dai_han` | Vay và nợ thuê tài chính dài hạn |
| `no_dai_han_khac` | Nợ dài hạn khác |
| `no_dai_han` | Tổng nợ dài hạn |
| `no_phai_tra` | Tổng nợ phải trả |
| `von_chu_so_huu` | Vốn chủ sở hữu (có thể âm) |
| `tong_nguon_von` | Tổng nguồn vốn, bằng tổng tài sản |
| `doanh_thu_thuan` | Doanh thu thuần về bán hàng và cung cấp dịch vụ |
| `gia_von_hang_ban` | Giá vốn hàng bán |
| `loi_nhuan_gop` | Lợi nhuận gộp |
| `chi_phi_ban_hang_quan_ly` | Chi phí bán hàng và chi phí quản lý doanh nghiệp |
| `chi_phi_lai_vay` | Chi phí lãi vay |
| `loi_nhuan_truoc_thue` | Tổng lợi nhuận kế toán trước thuế |
| `chi_phi_thue_tndn` | Chi phí thuế thu nhập doanh nghiệp |
| `loi_nhuan_sau_thue` | Lợi nhuận sau thuế |
| `khau_hao` | Khấu hao tài sản cố định trong năm |

Báo cáo rút gọn chỉ còn các dòng cần cho thẩm định. Quan hệ giữa các cột:

- Tổng tài sản = tài sản ngắn hạn + tài sản dài hạn.
- Nợ phải trả = nợ ngắn hạn + nợ dài hạn.
- Tổng nguồn vốn = nợ phải trả + vốn chủ sở hữu.
- Lợi nhuận trước thuế = lợi nhuận gộp − chi phí bán hàng và quản lý − chi phí lãi vay.

## `sao_ke_dn_thang.csv`

| Cột | Ý nghĩa |
|---|---|
| `ma_kh`, `thang` | Mã khách hàng, tháng (2026-01 … 2026-12) |
| `tien_vao` | Tổng tiền vào tài khoản thanh toán tại FTA trong tháng |
| `tien_ra` | Tổng tiền ra trong tháng |
| `so_du_cuoi_thang` | Số dư cuối tháng |

## `quan_he_tin_dung_dn.csv`

Số liệu tại 31/12/2026. Nhóm nợ theo số ngày quá hạn: nhóm 1 dưới 10 ngày; nhóm 2 từ 10 đến 90 ngày; nhóm 3 từ 91 đến 180 ngày; nhóm 4 từ 181 đến 360 ngày; nhóm 5 trên 360 ngày (Thông tư 31/2024/TT-NHNN, Điều 10).

| Cột | Ý nghĩa |
|---|---|
| `so_tctd_dang_vay` | Số tổ chức tín dụng đang có dư nợ, kể cả FTA |
| `du_no_tai_fta` | Dư nợ tại FTA |
| `du_no_tctd_khac` | Dư nợ tại các tổ chức tín dụng khác (theo CIC) |
| `tong_du_no` | Tổng dư nợ tại các tổ chức tín dụng |
| `nhom_no_fta` | Nhóm nợ do FTA tự phân loại; để trống nếu không có dư nợ tại FTA |
| `so_ngay_qua_han_fta` | Số ngày quá hạn hiện tại tại FTA |
| `nhom_no_cic` | Nhóm nợ cao nhất tại các tổ chức tín dụng theo CIC, kỳ gần nhất |
| `nhom_no_cic_cao_nhat_36_thang` | Nhóm nợ cao nhất theo CIC trong 36 tháng gần nhất |
| `du_no_qua_han` | Tổng dư nợ quá hạn tại các tổ chức tín dụng |
| `so_lan_qua_han_12_thang` | Số lần phát sinh quá hạn tại FTA trong 12 tháng |
| `so_ngay_qua_han_lon_nhat_12_thang` | Số ngày quá hạn lớn nhất tại FTA trong 12 tháng |

## `danh_sach_canh_bao_dn.csv`

| Cột | Ý nghĩa |
|---|---|
| `ma_so_thue` | Mã số thuế bị cảnh báo (có cả doanh nghiệp không phải khách hàng FTA) |
| `ly_do_canh_bao` | Lý do |
| `ngay_cap_nhat` | Ngày đưa vào danh sách |

## `de_nghi_vay_dn.csv`

| Cột | Ý nghĩa |
|---|---|
| `ma_ho_so`, `ma_kh` | Mã hồ sơ đề nghị, mã khách hàng |
| `ngay_de_nghi` | Ngày nộp đề nghị |
| `san_pham` | Cho vay theo hạn mức bổ sung vốn lưu động |
| `so_tien_de_nghi` | Hạn mức khách hàng đề nghị |
| `thoi_han_han_muc_thang` | Thời hạn duy trì hạn mức (tháng) |
| `doanh_thu_ke_hoach` | Doanh thu kế hoạch năm 2027 |
| `chi_phi_san_xuat_kinh_doanh_ke_hoach` | Chi phí sản xuất kinh doanh kế hoạch năm 2027 (giá vốn và chi phí bán hàng, quản lý) |
| `von_huy_dong_khac_ke_hoach` | Vốn vay tổ chức tín dụng khác và vốn huy động khác dự kiến dùng cho phương án |

## `tai_san_bao_dam_dn.csv`

| Cột | Ý nghĩa |
|---|---|
| `ma_ho_so`, `ma_kh` | Hồ sơ đề nghị và khách hàng |
| `stt_tai_san` | Thứ tự tài sản trong hồ sơ |
| `loai_tai_san` | Loại tài sản theo bảng tỷ lệ cho vay tối đa của FTA |
| `chu_so_huu` | Doanh nghiệp, hoặc bên thứ ba (người đại diện theo pháp luật) |
| `gia_tri_dinh_gia` | Giá trị do FTA định giá |
| `ngay_dinh_gia` | Ngày định giá |

## `lich_su_dn.csv`

Hồ sơ đã được cấp hạn mức các năm 2021–2025 (hạng từ B trở lên tại thời điểm cấp). Nhãn là kết quả trả nợ trong 12 tháng sau khi cấp.

| Cột | Ý nghĩa |
|---|---|
| `ma_ho_so`, `nam_cap_tin_dung` | Mã hồ sơ, năm cấp hạn mức |
| `nganh_chinh`, `quy_mo`, `nhom_bao_cao`, `co_kiem_toan` | Như ở hồ sơ doanh nghiệp |
| `tt_hien_hanh` … `ln_vcsh` | 11 chỉ tiêu tài chính tại thời điểm cấp (tỷ số, kỳ thu tiền tính bằng ngày) |
| `nhom_no_cic_cao_nhat_36_thang`, `so_lan_qua_han_12_thang` | Lịch sử tín dụng tại thời điểm cấp |
| `diem_tai_chinh`, `diem_phi_tai_chinh`, `diem_tin_dung`, `hang_tin_dung` | Kết quả bảng chấm điểm của FTA tại thời điểm cấp |
| `xau_12_thang` | 1 nếu khoản vay chuyển sang nhóm 3–5 trong 12 tháng sau khi cấp; 0 nếu không |

## `quy_dinh/nguong_cham_diem_dn.csv`

Bảng ngưỡng chấm điểm tài chính của Quy định nội bộ mô phỏng của Ngân hàng FTA.

| Cột | Ý nghĩa |
|---|---|
| `nganh`, `quy_mo`, `chi_tieu` | Ngành, quy mô, mã chỉ tiêu |
| `A`, `B`, `C`, `D` | Ngưỡng chấm. Chỉ tiêu càng cao càng tốt: từ A trở lên 100 điểm, từ B 80, từ C 60, từ D 40, dưới D 20. Chỉ tiêu càng thấp càng tốt thì đọc ngược lại |

## `quy_dinh/ty_le_cho_vay_tsbd.csv`

Tỷ lệ cho vay tối đa trên giá trị tài sản bảo đảm theo loại tài sản, theo Quy định nội bộ mô phỏng của Ngân hàng FTA (quy định doanh nghiệp, mục A7).

| Cột | Ý nghĩa |
|---|---|
| `loai_tai_san` | Loại tài sản bảo đảm, ghi như cột `loai_tai_san` của `tai_san_bao_dam_dn.csv` |
| `ty_le_cho_vay_toi_da` | Giá trị bảo đảm được tính = giá trị định giá × tỷ lệ này |
