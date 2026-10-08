# Dữ liệu thực hành FTA4006 — Ngân hàng FTA

Dữ liệu dùng cho phần thực hành của học phần **Ứng dụng công nghệ trong hoạt động ngân hàng thương mại (FTA4006)**, Trường Đại học Đại Nam.

**Toàn bộ số liệu là mô phỏng**, dùng cho học tập. Tên người, tên doanh nghiệp, số giấy tờ, mã số thuế, điện thoại, email đều sinh tự động, không phải dữ liệu của tổ chức hay cá nhân có thật. Ngân hàng FTA là ngân hàng mô phỏng.

- Mốc dữ liệu: 31/12/2026.

## Cấu trúc

```
lop_mau_nho/                         bộ dữ liệu dùng trên lớp
├── TU_DIEN_DU_LIEU_CA_NHAN.md       từ điển dữ liệu khách hàng cá nhân
├── khach_hang_raw.csv               danh sách khách hàng cá nhân (chưa làm sạch)
├── so_tiet_kiem.csv                 sổ tiền gửi
├── khoan_vay.csv                    hợp đồng vay
├── sao_ke/sao_ke_2026_01.csv …12    sao kê giao dịch 12 tháng
├── de_nghi_vay_ca_nhan.csv          hồ sơ đề nghị vay
├── bao_cao_cic_ca_nhan.csv          báo cáo thông tin tín dụng
├── danh_sach_canh_bao_ca_nhan.csv   danh sách cảnh báo
├── tai_san_bao_dam_ca_nhan.csv      tài sản bảo đảm
├── lich_su_vay_ca_nhan.csv          lịch sử khoản vay, có kết quả trả nợ
└── doanh_nghiep/                    khách hàng doanh nghiệp (tách riêng)
    ├── TU_DIEN_DU_LIEU_DN.md
    ├── doanh_nghiep_raw.csv, bctc_dn.csv, sao_ke_dn_thang.csv
    ├── quan_he_tin_dung_dn.csv, danh_sach_canh_bao_dn.csv
    ├── de_nghi_vay_dn.csv, tai_san_bao_dam_dn.csv, lich_su_dn.csv
    └── quy_dinh/nguong_cham_diem_dn.csv
```

Đơn vị tiền:

- Dữ liệu khách hàng cá nhân: **đồng**.
- Dữ liệu doanh nghiệp: **triệu đồng**, trừ khi cột `don_vi` ghi khác.

## Đọc dữ liệu trong notebook

```python
import pandas as pd
DU_LIEU = (
  "https://raw.githubusercontent.com"
  "/anptvnn-fta/fta4006-du-lieu/main"
  "/lop_mau_nho/")
kh_raw = pd.read_csv(DU_LIEU + "khach_hang_raw.csv")
dn_raw = pd.read_csv(DU_LIEU + "doanh_nghiep/doanh_nghiep_raw.csv")
```

Các tệp lưu dạng UTF-8. Cột số giấy tờ, số điện thoại, mã số thuế có thể bắt đầu bằng chữ số 0. Muốn giữ nguyên các cột này thì đọc dưới dạng chuỗi, ví dụ `dtype={"so_giay_to": str}`.
