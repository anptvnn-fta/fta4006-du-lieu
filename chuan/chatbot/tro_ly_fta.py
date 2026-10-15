# -*- coding: utf-8 -*-
"""Trợ lý ảo của Ngân hàng FTA — bản giới thiệu cho tiết 10 (Bài 3).

Một câu hỏi đi qua 4 bước:
  1. Nhận diện ý định: hồi quy logistic trên đặc trưng ký tự (TF-IDF), học từ bộ câu mẫu có nhãn.
  2. Kiểm tra: vai người hỏi có được dùng ý định đó không; khách hàng đã xác thực chưa.
  3. Truy xuất dữ liệu: lấy đúng số liệu của danh mục (kết quả tiết 5 và tiết 9, dữ liệu gốc của ngân hàng).
  4. Sinh câu trả lời: điền số liệu vào câu mẫu; nếu bật Gemini thì Gemini diễn đạt lại,
     sau đó kiểm tra lại mọi con số, sai thì dùng câu mẫu.

Dùng:
    import tro_ly_fta
    bot = tro_ly_fta.TroLy(DU_LIEU)          # DU_LIEU: thư mục "chuan/" trên kho GitHub của học phần
    bot.xac_thuc("KH003862", "7297", "1976-09-01")
    bot.hoi("Số dư tài khoản của tôi?")
    bot.hoi("Bao nhiêu khách đang xa dần?", vai="marketing")
"""
import os
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

MOC = pd.Timestamp("2026-12-31")                 # ngày dữ liệu
NGUONG_TIN_CAY = 0.30                           # dưới ngưỡng thì coi là chưa hiểu câu hỏi
SO_LAN_SAI_TOI_DA = 3                           # xác thực sai 3 lần thì khóa phiên
THAM_QUYEN_CHI_NHANH = 20_000                   # triệu đồng; trên mức này trình hội sở (quy định A8, B7.4)
MO_HINH_GEMINI = "gemini-flash-latest"

TEN_VAI = {"khach_hang": "khách hàng", "marketing": "chuyên viên marketing",
           "chuyen_vien": "chuyên viên tín dụng"}
# Phân quyền: mỗi vai chỉ được dùng một số ý định (giả định của Ngân hàng FTA)
QUYEN = {
    "khach_hang": {"chao_hoi", "so_du", "tiet_kiem", "khoan_vay", "ho_so_vay", "giao_dich",
                   "chuyen_chuyen_vien"},
    "marketing": {"chao_hoi", "thong_ke_nhom", "soan_tin"},
    "chuyen_vien": {"chao_hoi", "tra_cuu_ho_so", "tra_cuu_dn", "danh_sach_ho_so"},
}
# Ý định cần xác thực khách hàng trước khi trả lời
CAN_XAC_THUC = {"so_du", "tiet_kiem", "khoan_vay", "ho_so_vay", "giao_dich"}


def tien(x):
    """Số tiền (đồng) viết theo kiểu Việt Nam: 1.234.567 đồng."""
    return f"{x:,.0f}".replace(",", ".") + " đồng"


def trieu(x):
    """Số tiền tính bằng triệu đồng: 1.234,5 triệu đồng."""
    s = f"{x:,.1f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return (s[:-2] if s.endswith(",0") else s) + " triệu đồng"


def so(x, le=0):
    """Số viết theo kiểu Việt Nam: dấu chấm nghìn, dấu phẩy thập phân."""
    return f"{x:,.{le}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def lam_sach(cau):
    """Thay mã cụ thể bằng nhãn chung, để mô hình học mẫu câu chứ không học từng mã."""
    cau = re.sub(r"HS(CN|DN)\d+", " mã hồ sơ ", cau, flags=re.I)
    cau = re.sub(r"KH\d+", " mã khách hàng ", cau, flags=re.I)
    return re.sub(r"DN\d+", " mã doanh nghiệp ", cau, flags=re.I)


def ngay(x):
    return pd.Timestamp(x).strftime("%d/%m/%Y")


class TroLy:
    # ------------------------------------------------------------------ 0. Nạp dữ liệu
    def __init__(self, du_lieu, thu_muc=".", dung_gemini=False):
        """du_lieu: đường dẫn thư mục chuan/ của kho dữ liệu; thu_muc: nơi có tệp kết quả của sinh viên."""
        self.du_lieu, self.thu_muc = du_lieu, Path(thu_muc)
        self.dung_gemini = dung_gemini
        self.dm = self._doc("danh_muc_tiet5.csv", "ket_qua/tiet05/",
                            dtype={"so_giay_to": str, "dien_thoai": str})
        self.hs = self._doc("ho_so_tiet9.csv", "ket_qua/tiet09/", dtype={"so_giay_to": str})
        self.dn = self._doc("doanh_nghiep_tiet9.csv", "ket_qua/tiet09/",
                            dtype={"ma_so_thue": str, "dien_thoai": str})
        self.so = pd.read_csv(du_lieu + "ca_nhan/so_tiet_kiem.csv")
        self.vay = pd.read_csv(du_lieu + "ca_nhan/khoan_vay.csv")
        self.cau_mau = pd.read_csv(du_lieu + "chatbot/cau_mau_y_dinh.csv")
        self._sao_ke = None                     # đọc khi cần (12 tệp)
        self.mo_hinh = self._huan_luyen()
        self.chi_nhanh = sorted(self.dm["chi_nhanh_quan_ly"].unique())
        self.ten_nhom = sorted(self.dm["ten_nhom"].unique())
        self.khach, self._sai, self._phieu = None, 0, []
        print(f"Trợ lý ảo FTA: {so(len(self.dm))} khách hàng cá nhân, {len(self.hs)} hồ sơ vay, "
              f"{so(len(self.dn))} doanh nghiệp; {self.cau_mau['y_dinh'].nunique()} ý định, "
              f"{len(self.cau_mau)} câu mẫu.")

    def _doc(self, ten, thu_muc_kq, **kw):
        """Ưu tiên tệp kết quả sinh viên đã làm; không có thì lấy kết quả chuẩn trên kho."""
        p = self.thu_muc / ten
        return pd.read_csv(p if p.exists() else self.du_lieu + thu_muc_kq + ten, **kw)

    @property
    def sao_ke(self):
        if self._sao_ke is None:
            cot = ["ngay_gio", "ma_kh", "kenh", "loai_giao_dich", "so_tien", "trang_thai",
                   "so_du_sau_giao_dich"]
            ds = [pd.read_csv(self.du_lieu + f"ca_nhan/sao_ke/sao_ke_2026_{t:02d}.csv.gz", usecols=cot)
                  for t in range(1, 13)]
            sk = pd.concat(ds, ignore_index=True)
            self._sao_ke = sk[sk["trang_thai"] == "Thành công"].sort_values("ngay_gio")
        return self._sao_ke

    # ------------------------------------------------------------------ 1. Nhận diện ý định
    def _huan_luyen(self):
        """Hồi quy logistic nhiều lớp trên TF-IDF của cụm 2–4 ký tự (chịu được gõ không dấu, sai chính tả nhẹ)."""
        mo_hinh = make_pipeline(
            TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), lowercase=True),
            LogisticRegression(max_iter=2000, C=10))
        mo_hinh.fit(self.cau_mau["cau"].map(lam_sach), self.cau_mau["y_dinh"])
        return mo_hinh

    def nhan_dien(self, cau):
        """Trả về (ý định, độ tin cậy). Độ tin cậy là xác suất lớn nhất của hồi quy logistic."""
        p = self.mo_hinh.predict_proba([lam_sach(cau)])[0]
        i = int(np.argmax(p))
        return self.mo_hinh.classes_[i], round(float(p[i]), 2)

    # ------------------------------------------------------------------ 2. Xác thực, phân quyền
    def xac_thuc(self, ma_kh, bon_so_cuoi, ngay_sinh):
        """Khách hàng xác thực bằng mã khách hàng, 4 số cuối giấy tờ tùy thân, ngày sinh."""
        if self._sai >= SO_LAN_SAI_TOI_DA:
            print("Phiên đã bị khóa do xác thực sai 3 lần. Vui lòng liên hệ chi nhánh.")
            return False
        k = self.dm[self.dm["ma_kh"] == ma_kh]
        dung = (len(k) == 1 and str(k["so_giay_to"].iloc[0])[-4:] == str(bon_so_cuoi)
                and str(k["ngay_sinh"].iloc[0]) == str(ngay_sinh))
        if not dung:
            self._sai += 1
            print(f"Thông tin xác thực chưa đúng (lần {self._sai}/{SO_LAN_SAI_TOI_DA}).")
            return False
        if k["trang_thai"].iloc[0] == "Đã đóng":
            print("Quan hệ của quý khách với Ngân hàng FTA đã đóng; vui lòng liên hệ chi nhánh.")
            return False
        self.khach, self._sai = k.iloc[0], 0
        print(f"Xác thực thành công: {ma_kh} – {self.khach['ho_ten']}.")
        return True

    def dang_xuat(self):
        self.khach = None
        print("Đã kết thúc phiên của khách hàng.")

    def _xung_ho(self):
        return "anh" if self.khach is not None and self.khach["gioi_tinh"] == "Nam" else "chị"

    # ------------------------------------------------------------------ 3. Truy xuất dữ liệu
    def _ma(self, cau, mau):
        m = re.findall(mau, cau.upper())
        return m[0] if m else None

    def _tim_chi_nhanh(self, cau):
        c = cau.lower()
        return next((cn for cn in self.chi_nhanh if cn.lower().replace("cn ", "") in c), None)

    def _tim_nhom(self, cau):
        c = cau.lower()
        return next((n for n in self.ten_nhom if n.lower() in c), None)

    def _so_du(self, kh):
        g = self.sao_ke[self.sao_ke["ma_kh"] == kh]
        so = self.so[(self.so["ma_kh"] == kh) & (self.so["trang_thai"] == "Đang hiệu lực")]
        cuoi = f"Số dư tài khoản thanh toán sau giao dịch gần nhất ({ngay(g['ngay_gio'].iloc[-1])}) là " \
               f"{tien(g['so_du_sau_giao_dich'].iloc[-1])}." if len(g) else "Tài khoản chưa có giao dịch."
        them = f" Ngoài ra {self._xung_ho()} có {len(so)} sổ tiết kiệm đang hiệu lực, tổng gốc " \
               f"{tien(so['so_tien_goc'].sum())}." if len(so) else ""
        return cuoi + them, "sao kê 12 tháng và sổ tiết kiệm"

    def _tiet_kiem(self, kh):
        so = self.so[(self.so["ma_kh"] == kh) & (self.so["trang_thai"] == "Đang hiệu lực")]
        if not len(so):
            return f"{self._xung_ho().capitalize()} hiện không có sổ tiết kiệm đang hiệu lực.", "sổ tiết kiệm"
        dong = [f"sổ {r.so_so}: gốc {tien(r.so_tien_goc)}, kỳ hạn {r.ky_han_thang} tháng, lãi suất "
                f"{str(r.lai_suat_nam_pct).replace('.', ',')}%/năm, đến hạn {ngay(r.ngay_dao_han)}"
                for r in so.itertuples()]
        return f"{self._xung_ho().capitalize()} có {len(so)} sổ tiết kiệm đang hiệu lực: " + "; ".join(dong) + ".", \
            "sổ tiết kiệm"

    def _khoan_vay(self, kh):
        v = self.vay[(self.vay["ma_kh"] == kh) & (self.vay["trang_thai"] == "Đang hiệu lực")]
        if not len(v):
            return f"{self._xung_ho().capitalize()} hiện không có khoản vay đang hiệu lực tại Ngân hàng FTA.", \
                "khoản vay"
        dong = [f"hợp đồng {r.so_hop_dong} ({r.san_pham_vay}): dư nợ gốc {tien(r.du_no_goc)}, kỳ trả "
                f"{tien(r.ky_tra_no_hang_thang)}, kỳ tới ngày {ngay(r.ngay_den_han_ky_toi)}"
                for r in v.itertuples()]
        return "Khoản vay đang hiệu lực – " + "; ".join(dong) + ".", "khoản vay"

    def _ho_so_vay(self, kh):
        h = self.hs[self.hs["ma_kh"] == kh]
        if not len(h):
            return f"Ngân hàng FTA chưa nhận hồ sơ đề nghị vay nào của {self._xung_ho()}.", "hồ sơ đề nghị vay"
        dong = [f"hồ sơ {r.ma_ho_so} ({r.san_pham}, đề nghị {tien(r.so_tien_de_nghi)}, nộp ngày "
                f"{ngay(r.ngay_de_nghi)})" for r in h.itertuples()]
        # Hạng, điểm, hạn mức đề xuất là thông tin nội bộ, chưa phải quyết định: không cung cấp cho khách.
        return ("Ngân hàng FTA đã nhận " + "; ".join(dong) + ". Hồ sơ đang được thẩm định, chưa có quyết định "
                "cho vay; ngân hàng sẽ thông báo kết quả cho " + self._xung_ho() + "."), "hồ sơ đề nghị vay"

    def _giao_dich(self, kh):
        g = self.sao_ke[self.sao_ke["ma_kh"] == kh].tail(3)
        if not len(g):
            return "Tài khoản chưa có giao dịch.", "sao kê"
        dong = [f"{ngay(r.ngay_gio)} {r.loai_giao_dich} {tien(r.so_tien)} ({r.kenh})" for r in g.itertuples()]
        return "3 giao dịch thành công gần nhất: " + "; ".join(dong) + ".", "sao kê 12 tháng"

    def _chuyen_chuyen_vien(self, cau):
        ma = f"PC{len(self._phieu) + 1:04d}"
        self._phieu.append(dict(ma_phieu=ma, ma_kh="chưa xác thực" if self.khach is None else self.khach["ma_kh"],
                                noi_dung=cau))
        return (f"Em đã chuyển yêu cầu tới chuyên viên, mã phiếu {ma}. Nếu mất thẻ hoặc nghi bị lừa đảo, quý "
                "khách gọi ngay tổng đài để khóa thẻ, tài khoản hoặc đến chi nhánh gần nhất."), "tạo phiếu chuyển chuyên viên"

    def _thong_ke_nhom(self, cau):
        d = self.dm[self.dm["trang_thai"] != "Đã đóng"]          # chỉ khách đang có quan hệ
        cn, nhom, c = self._tim_chi_nhanh(cau), self._tim_nhom(cau), cau.lower()
        if cn:
            d = d[d["chi_nhanh_quan_ly"] == cn]
        pham_vi = cn or "Toàn hệ thống"
        if "ưu tiên" in c:
            d = d[d["khach_uu_tien"] == "Có"]
        if nhom:
            d = d[d["ten_nhom"] == nhom]
        loai = ("khách hàng ưu tiên " if "ưu tiên" in c else "") + (f"nhóm {nhom}" if nhom else "")
        if not cn and "chi nhánh" in c:
            dem, ten = d["chi_nhanh_quan_ly"].value_counts(), "chi nhánh"
        elif nhom or loai:
            return f"{pham_vi}: {so(len(d))} {loai.strip() or 'khách hàng'} đang có quan hệ.", \
                "danh mục tiết 5, chỉ số đếm"
        elif "doanh số" in c:
            dem, ten = d["nhom_doanh_so"].value_counts(), "nhóm doanh số"
        else:
            dem, ten = d["ten_nhom"].value_counts(), "nhóm hành vi"
        dong = "; ".join(f"{k} {so(v)}" for k, v in dem.items())
        return f"{pham_vi}, {loai.strip() + ', ' if loai else ''}theo {ten}: {dong}.", \
            "danh mục tiết 5, chỉ số đếm"

    def _soan_tin(self, cau):
        nhom = self._tim_nhom(cau)
        d = self.dm[self.dm["trang_thai"] != "Đã đóng"]
        if nhom:
            d = d[d["ten_nhom"] == nhom]
        dac_diem = (f"{so(len(d))} khách hàng; bình quân {so(d['gd_bq_thang'].mean(), 1)} giao dịch/tháng; "
                    f"tỷ trọng kênh số {so(d['ty_trong_kenh_so'].mean(), 2)}; "
                    f"{so(d['thang_tu_gd_cuoi'].mean(), 1)} tháng từ giao dịch cuối")
        mau = {
            "Đang xa dần": "Ngân hàng FTA trân trọng cảm ơn quý khách đã đồng hành. Mời quý khách tiếp tục giao "
                           "dịch nhanh, an toàn qua Mobile Banking hoặc ghé chi nhánh gần nhất để được tư vấn.",
            "Mới mở quan hệ": "Chào mừng quý khách đến với Ngân hàng FTA. Quý khách có thể chuyển tiền, thanh toán "
                              "hóa đơn ngay trên Mobile Banking; chuyên viên luôn sẵn sàng hỗ trợ tại chi nhánh.",
            "Quầy truyền thống": "Ngân hàng FTA mời quý khách trải nghiệm Mobile Banking: chuyển khoản, thanh toán "
                                 "hóa đơn mọi lúc. Chuyên viên tại chi nhánh sẵn sàng hướng dẫn cài đặt.",
        }.get(nhom, "Ngân hàng FTA trân trọng cảm ơn quý khách. Mời quý khách liên hệ chi nhánh hoặc Mobile "
                    "Banking để được tư vấn sản phẩm phù hợp.")
        self._dac_diem_nhom = (nhom or "khách hàng đang có quan hệ", dac_diem)
        return mau, f"đặc điểm nhóm ({dac_diem})"

    def _tra_cuu_ho_so(self, cau):
        ma_hs, ma_kh = self._ma(cau, r"HSCN\d{5}"), self._ma(cau, r"KH\d{6}")
        h = self.hs[self.hs["ma_ho_so"] == ma_hs] if ma_hs else self.hs[self.hs["ma_kh"] == ma_kh]
        if not len(h):
            return "Vui lòng nêu mã hồ sơ (HSCN…) hoặc mã khách hàng (KH…) có hồ sơ đề nghị vay.", "—"
        r = h.iloc[0]
        ten = self.dm.loc[self.dm["ma_kh"] == r["ma_kh"], "ho_ten"].iloc[0]
        dau = (f"{r['ma_ho_so']} – {ten}, {r['san_pham']}, đề nghị {trieu(r['so_tien_de_nghi'] / 1e6)}: "
               f"điểm {str(round(r['diem_tin_dung'], 1)).replace('.', ',')}, hạng {r['hang_tin_dung']}; ")
        if r["ket_qua_so_bo"] == "Dừng":
            return dau + f"dừng ở thẩm định sơ bộ ({r['ly_do_dung']}), hạn mức đề xuất 0.", "kết quả tiết 9"
        return dau + (f"hạn mức đề xuất {trieu(r['han_muc'] / 1e6)}, thời hạn {int(r['thoi_han'])} tháng; "
                      f"{r['ly_do_han_muc'].lower()}. Thẩm quyền: giám đốc chi nhánh."), "kết quả tiết 9"

    def _tra_cuu_dn(self, cau):
        ma = self._ma(cau, r"DN\d{5}")
        d = self.dn[self.dn["ma_kh"] == ma]
        if not len(d):
            return "Vui lòng nêu mã doanh nghiệp (DN…).", "—"
        r = d.iloc[0]
        dau = (f"{ma} – {r['ten_doanh_nghiep']} ({r['quy_mo']}, {r['nganh_chinh']}): điểm "
               f"{str(round(r['diem_tin_dung'], 1)).replace('.', ',')}, hạng {r['hang_tin_dung']}; ")
        if pd.isna(r["ma_ho_so"]):
            return dau + "không có hồ sơ đề nghị cấp hạn mức.", "kết quả tiết 9"
        tq = "trình hội sở" if r["han_muc"] > THAM_QUYEN_CHI_NHANH else "giám đốc chi nhánh"
        return dau + (f"hồ sơ {r['ma_ho_so']} đề nghị {trieu(r['so_tien_de_nghi'])}, hạn mức đề xuất "
                      f"{trieu(r['han_muc'])}; {r['ly_do_han_muc'].lower()}. Thẩm quyền: {tq}."), "kết quả tiết 9"

    def _danh_sach_ho_so(self, cau):
        if "doanh nghiệp" in cau.lower():
            d = self.dn[self.dn["ma_ho_so"].notna()]
            dem = d["ly_do_han_muc"].str.split(":").str[0].value_counts()
            hs = (d["han_muc"] > THAM_QUYEN_CHI_NHANH).sum()
            return (f"{len(d)} hồ sơ doanh nghiệp; {hs} hồ sơ trên 20 tỷ đồng phải trình hội sở. Theo lý do: "
                    + "; ".join(f"{k} {v}" for k, v in dem.items()) + "."), "kết quả tiết 9"
        dem = self.hs["ly_do_han_muc"].str.split(":").str[0].value_counts()
        co = (self.hs["han_muc"] > 0).sum()
        return (f"{len(self.hs)} hồ sơ cá nhân, {co} hồ sơ được đề xuất hạn mức, tổng "
                f"{trieu(self.hs['han_muc'].sum() / 1e6)}. Theo lý do: "
                + "; ".join(f"{k} {v}" for k, v in dem.items()) + "."), "kết quả tiết 9"

    # ------------------------------------------------------------------ 4. Sinh câu trả lời
    def _gemini(self, yeu_cau):
        key = os.environ.get("GEMINI_API_KEY")
        if not (self.dung_gemini and key):
            return None
        try:
            if getattr(self, "_gemini_client", None) is None:
                from google import genai
                self._gemini_client = genai.Client(api_key=key)      # giữ kết nối để dùng lại
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                kq = self._gemini_client.models.generate_content(model=MO_HINH_GEMINI, contents=yeu_cau)
            return kq.text.strip()
        except Exception as e:                                   # mất mạng, hết hạn mức gọi…
            print("   (không gọi được Gemini:", type(e).__name__, ")")
            return None

    def _dien_dat(self, cau_mau, doi_tuong):
        """Gemini diễn đạt lại; mọi con số của câu mẫu phải còn nguyên, không thì giữ câu mẫu."""
        moi = self._gemini(
            f"Bạn là trợ lý ảo của Ngân hàng FTA. Viết lại câu trả lời dưới đây gửi {doi_tuong}, tiếng Việt "
            "lịch sự, ngắn gọn, giữ nguyên mọi con số, mã và ngày; không thêm thông tin, lời khuyên hay cam kết "
            f"nào ngoài câu gốc. Chỉ trả về câu đã viết lại.\n\nCâu gốc: {cau_mau}")
        if moi is None:
            return cau_mau, "câu mẫu"
        so = re.findall(r"\d[\d.,]*\d|\d", cau_mau)
        if all(s in moi for s in so):
            return moi, "Gemini, đã kiểm số liệu"
        return cau_mau, "câu mẫu – bản Gemini sai số liệu nên không dùng"

    def _soan_bang_gemini(self, cau_mau):
        nhom, dac_diem = self._dac_diem_nhom
        moi = self._gemini(
            f"Soạn 1 tin nhắn tiếp thị (tối đa 300 ký tự) của Ngân hàng FTA gửi nhóm khách hàng '{nhom}' "
            f"(đặc điểm: {dac_diem}). Không nêu lãi suất, phí, quà tặng hay bất kỳ con số nào; không hứa "
            "hẹn; không dùng thông tin cá nhân; kết thúc bằng gợi ý dùng Mobile Banking hoặc liên hệ chi "
            "nhánh. Chỉ trả về nội dung tin nhắn.")
        if moi is None:
            return cau_mau, "câu mẫu"
        if re.search(r"\d", moi) or len(moi) > 400:
            return cau_mau, "câu mẫu – bản Gemini có con số hoặc quá dài nên không dùng"
        return moi, "Gemini, đã kiểm không có con số"

    # ------------------------------------------------------------------ Luồng xử lý 1 câu hỏi
    def hoi(self, cau, vai="khach_hang", chi_tiet=True):
        y, p = self.nhan_dien(cau)
        buoc = [f"1. Ý định: {y} (độ tin cậy {so(p, 2)})"]
        tra_loi, nguon = self._xu_ly(cau, vai, y, p, buoc)
        buoc.append(f"3. Dữ liệu: {nguon}")
        if y == "soan_tin" and vai == "marketing" and nguon.startswith("đặc điểm"):
            tra_loi, cach = self._soan_bang_gemini(tra_loi)
        elif nguon not in ("—", "không truy xuất"):
            tra_loi, cach = self._dien_dat(tra_loi, TEN_VAI[vai])
        else:
            cach = "câu mẫu"
        buoc.append(f"4. Trả lời [{cach}]: {tra_loi}")
        print(f"[{TEN_VAI[vai]}] {cau}")
        print("\n".join(buoc) if chi_tiet else tra_loi)
        print()

    def _xu_ly(self, cau, vai, y, p, buoc):
        """Bước 2: kiểm tra; trả về (câu trả lời, nguồn dữ liệu)."""
        ma_khac = self._ma(cau, r"KH\d{6}")
        if vai == "khach_hang" and ma_khac and (self.khach is None or ma_khac != self.khach["ma_kh"]):
            buoc.append("2. Kiểm tra: hỏi theo mã của khách hàng khác – từ chối")
            return "Trợ lý chỉ cung cấp thông tin của chính khách hàng đã xác thực.", "không truy xuất"
        if p < NGUONG_TIN_CAY:
            buoc.append(f"2. Kiểm tra: độ tin cậy dưới {so(NGUONG_TIN_CAY, 2)} – chưa hiểu câu hỏi")
            return "Trợ lý chưa hiểu câu hỏi. Vui lòng diễn đạt lại hoặc đề nghị gặp chuyên viên.", \
                "không truy xuất"
        if y == "ngoai_pham_vi":
            buoc.append("2. Kiểm tra: ngoài phạm vi dịch vụ – không truy xuất")
            return ("Câu hỏi nằm ngoài phạm vi hỗ trợ của trợ lý ảo Ngân hàng FTA. Trợ lý không tư vấn đầu tư "
                    "và không cung cấp thông tin ngoài dịch vụ của ngân hàng; quý khách có thể hỏi về tài khoản, "
                    "tiết kiệm, khoản vay hoặc đề nghị gặp chuyên viên."), "không truy xuất"
        if y not in QUYEN[vai]:
            buoc.append(f"2. Kiểm tra: vai {TEN_VAI[vai]} không được dùng ý định {y} – từ chối")
            return f"Nội dung này không thuộc quyền truy cập của {TEN_VAI[vai]}.", "không truy xuất"
        if y == "chao_hoi":
            buoc.append(f"2. Kiểm tra: vai {TEN_VAI[vai]} được phép")
            viec = {"khach_hang": "số dư, sổ tiết kiệm, khoản vay, hồ sơ đề nghị vay, giao dịch gần nhất, "
                                  "chuyển chuyên viên",
                    "marketing": "thống kê khách hàng theo nhóm, soạn tin nhắn tiếp thị",
                    "chuyen_vien": "tra cứu hồ sơ vay cá nhân, doanh nghiệp, tổng hợp hồ sơ theo lý do"}[vai]
            return f"Trợ lý ảo Ngân hàng FTA xin chào. Trợ lý hỗ trợ: {viec}.", "không truy xuất"
        if y == "chuyen_chuyen_vien":
            buoc.append("2. Kiểm tra: yêu cầu cần con người xử lý – chuyển chuyên viên")
            return self._chuyen_chuyen_vien(cau)
        if y in CAN_XAC_THUC:
            if self.khach is None:
                buoc.append("2. Kiểm tra: khách hàng chưa xác thực – không truy xuất")
                return ("Để bảo mật, quý khách vui lòng xác thực bằng mã khách hàng, 4 số cuối giấy tờ tùy thân "
                        "và ngày sinh trước khi tra cứu."), "không truy xuất"
            buoc.append(f"2. Kiểm tra: đã xác thực {self.khach['ma_kh']}")
            return getattr(self, "_" + y)(self.khach["ma_kh"])
        buoc.append(f"2. Kiểm tra: vai {TEN_VAI[vai]} được phép")
        return getattr(self, "_" + y)(cau)

    def phieu_chuyen(self):
        return pd.DataFrame(self._phieu, columns=["ma_phieu", "ma_kh", "noi_dung"])
