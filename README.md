# Dữ liệu thực hành FTA4006 — Ngân hàng FTA

Dữ liệu dùng cho phần thực hành của học phần **Ứng dụng công nghệ trong hoạt động ngân hàng thương mại (FTA4006)**, Trường Đại học Đại Nam.

**Toàn bộ số liệu là mô phỏng**, dùng cho học tập. Tên người, tên doanh nghiệp, số giấy tờ, mã số thuế, điện thoại, email đều sinh tự động, không phải dữ liệu của tổ chức hay cá nhân có thật. Ngân hàng FTA là ngân hàng mô phỏng.

- Mốc dữ liệu: 31/12/2026.

## Cấu trúc

```
demo/                                   bộ dữ liệu dùng trên lớp
├── ca_nhan/                            khách hàng cá nhân
│   ├── TU_DIEN_DU_LIEU_CA_NHAN.md      từ điển dữ liệu
│   ├── khach_hang_raw.csv              danh sách khách hàng (chưa làm sạch)
│   ├── so_tiet_kiem.csv                sổ tiền gửi
│   ├── khoan_vay.csv                   hợp đồng vay
│   ├── sao_ke/sao_ke_2026_01.csv … 12  sao kê giao dịch 12 tháng
│   ├── de_nghi_vay_ca_nhan.csv         hồ sơ đề nghị vay
│   ├── bao_cao_cic_ca_nhan.csv         báo cáo thông tin tín dụng
│   ├── danh_sach_canh_bao_ca_nhan.csv  danh sách cảnh báo
│   ├── tai_san_bao_dam_ca_nhan.csv     tài sản bảo đảm
│   └── lich_su_vay_ca_nhan.csv         lịch sử khoản vay, có kết quả trả nợ
├── doanh_nghiep/                       khách hàng doanh nghiệp
│   ├── TU_DIEN_DU_LIEU_DN.md           từ điển dữ liệu
│   ├── doanh_nghiep_raw.csv            hồ sơ doanh nghiệp (chưa làm sạch)
│   ├── bctc_dn.csv                     báo cáo tài chính 2023–2025
│   ├── sao_ke_dn_thang.csv             sao kê theo tháng năm 2026
│   ├── quan_he_tin_dung_dn.csv         quan hệ tín dụng, thông tin CIC
│   ├── danh_sach_canh_bao_dn.csv       danh sách cảnh báo
│   ├── de_nghi_vay_dn.csv              hồ sơ đề nghị cấp hạn mức
│   ├── tai_san_bao_dam_dn.csv          tài sản bảo đảm
│   ├── lich_su_dn.csv                  lịch sử hồ sơ, có kết quả trả nợ
│   └── quy_dinh/nguong_cham_diem_dn.csv  bảng ngưỡng chấm điểm
└── mau/                                bảng mẫu nhỏ cho ví dụ trên lớp
    ├── kh_mau.csv                      7 khách hàng
    ├── gd_t1.csv, gd_t2.csv            giao dịch tháng 1, tháng 2
    ├── vay_mau.csv                     6 hợp đồng vay
    ├── tk_mau.csv                      4 sổ tiền gửi
    ├── dn_mau_ho_so.csv                hồ sơ 4 doanh nghiệp
    ├── dn_mau_bctc.csv                 báo cáo tài chính 2024–2025 của 4 doanh nghiệp
    ├── hs_mau.csv                      5 hồ sơ đề nghị vay cá nhân
    ├── ls_mau.csv                      20 hồ sơ lịch sử: điểm và kết quả trả nợ
    └── diem_mau.csv                    6 điểm, 2 biến, cho ví dụ phân nhóm
```

Kết quả chuẩn từng tiết của bộ lớp nằm trong cây thư mục riêng `ket_qua/` (xem `ket_qua/README.md`):

```
ket_qua/                                kết quả chuẩn, dùng khi vắng tiết trước hoặc chưa làm xong
├── tiet01/khach_hang_sach.csv
├── tiet02/danh_muc_tiet2.csv
├── tiet03/doanh_nghiep_tiet3.csv
├── tiet04/danh_muc_tiet4.csv
├── tiet05/danh_muc_tiet5.csv, doanh_nghiep_tiet5.csv
├── tiet06/ho_so_tiet6.csv, doanh_nghiep_tiet6.csv
└── tiet07/ho_so_tiet7.csv, doanh_nghiep_tiet7.csv
```

Đơn vị tiền:

- Dữ liệu khách hàng cá nhân: **đồng**.
- Dữ liệu doanh nghiệp: **triệu đồng**, trừ khi cột `don_vi` ghi khác.
- Bảng mẫu (`mau/`): **triệu đồng**.

## Đường dẫn đọc trực tiếp

Mỗi tệp đọc được qua đường dẫn dạng:

```
https://raw.githubusercontent.com/anptvnn-fta/fta4006-du-lieu/main/demo/ca_nhan/khach_hang_raw.csv
https://raw.githubusercontent.com/anptvnn-fta/fta4006-du-lieu/main/demo/doanh_nghiep/doanh_nghiep_raw.csv
```

Các tệp lưu dạng UTF-8. Cột số giấy tờ, số điện thoại, mã số thuế có thể bắt đầu bằng chữ số 0. Muốn giữ nguyên các cột này thì đọc dưới dạng chuỗi.
