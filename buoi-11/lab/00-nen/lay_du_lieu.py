# BẢN SAO của tools/lay_du_lieu.py — SINH TỰ ĐỘNG bởi tools/sinh_nen.py — KHÔNG SỬA TAY. Sửa tools/lay_du_lieu.py rồi chạy lại tool.
"""Tải dữ liệu của một buổi theo `du-lieu.toml`, kiểm sha256, cache dùng chung giữa các buổi.

    python tools/lay_du_lieu.py buoi-NN                    # đọc buoi-NN/lab/00-nen/du-lieu.toml
    python tools/lay_du_lieu.py duong/dan/du-lieu.toml     # file bất kỳ
    python tools/lay_du_lieu.py buoi-NN --chi uci-bike-sharing
    python tools/lay_du_lieu.py buoi-NN --tom-tat          # bảng tệp / số dòng / sha256 rút gọn
    python tools/lay_du_lieu.py --sha URL                  # tác giả: tính sha256 + dung lượng một URL

Mỗi buổi có BẢN SAO của file này ở `buoi-NN/lab/00-nen/lay_du_lieu.py` (sinh bởi
`tools/sinh_nen.py`) — buổi không đọc gì ngoài thư mục của nó. Sửa ở đây rồi chạy lại
`sinh_nen.py`, đừng sửa bản sao.

Chỉ dùng thư viện chuẩn Python ≥ 3.11 để chạy được cả trước khi `uv sync` xong. Ngoại lệ:
nguồn `kaggle` cần `kagglehub` (sinh_nen tự thêm vào phụ thuộc của buổi có dữ liệu Kaggle).

Luồng của một bộ dữ liệu:
    nguồn (mirror trước, gốc sau) ──tải──> cache/sha256/ab/abcd…  ──kiểm sha256──>
    giải nén / chép ──> <lab>/du-lieu/raw/<ten>/  (chỉ đọc) + NGUON.txt ghi nguồn, giấy phép

Cache: $KHOA_FORECASTING_CACHE, mặc định ~/.cache/khoa-forecasting/. Cache lưu theo sha256
nên hai buổi dùng cùng một tệp chỉ tải một lần.

Các kiểu nguồn (`kieu`):
    http    URL tải trực tiếp (UCI, Zenodo, NOAA…). Có `url_mirror` thì thử mirror trước.
    hf      tệp trong Hugging Face Datasets, CHỐT commit 40 ký tự: repo, revision, duong_dan
    kaggle  cuộc thi/bộ dữ liệu Kaggle, học viên tự đăng nhập và chấp nhận luật; sha256 theo tệp
    eia     EIA API v2 (cần EIA_API_KEY), phân trang, lưu CSV chuẩn hoá
    openaq  OpenAQ API v3 (cần OPENAQ_API_KEY), lưu CSV chuẩn hoá

Trường `truc_tiep = true` chỉ dành cho bài dự báo trực tiếp (dữ liệu chưa tồn tại lúc soạn):
bỏ kiểm sha256 nhưng ghi lại sha256 thực tế và thời điểm tải.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import http.client
import json
import os
import shutil
import stat
import sys
import tarfile
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import UTC, datetime
from pathlib import Path

PHIEN_BAN_DINH_DANG = 1
# Wikimedia yêu cầu User-Agent có tên công cụ + cách liên hệ; UA chung chung (curl, urllib) có thể bị 403
TAC_NHAN = "khoa-forecasting-lay-du-lieu/1 (khoa hoc Forecasting in AI; lien he qua repo khoa hoc) Python-urllib"
KIEU_HOP_LE = {"http", "hf", "kaggle", "eia", "openaq"}
KHOA_API = {"eia": "EIA_API_KEY", "openaq": "OPENAQ_API_KEY"}
DANG_KY_KHOA = {
    "EIA_API_KEY": "https://www.eia.gov/opendata/register.php",
    "OPENAQ_API_KEY": "https://explore.openaq.org/register",
}
SO_LAN_THU = 4
CHO_TOI_DA = 60  # giây, cho một lần chờ khi bị 429/5xx


class LoiDuLieu(Exception):
    """Lỗi có thông báo đủ để học viên tự sửa — in ra nguyên văn, không kèm traceback."""


# ---------------------------------------------------------------------------- tiện ích


def thu_muc_cache() -> Path:
    goc = os.environ.get("KHOA_FORECASTING_CACHE")
    if goc:
        return Path(goc).expanduser()
    xdg = os.environ.get("XDG_CACHE_HOME")
    return (Path(xdg) if xdg else Path.home() / ".cache") / "khoa-forecasting"


def sha256_tep(duong_dan: Path) -> str:
    h = hashlib.sha256()
    with open(duong_dan, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def an_bi_mat(url: str) -> str:
    """Xoá giá trị api_key/token khỏi URL trước khi in."""
    phan = urllib.parse.urlsplit(url)
    if not phan.query:
        return url
    q = [(k, "***" if k.lower() in {"api_key", "apikey", "token", "key"} else v)
         for k, v in urllib.parse.parse_qsl(phan.query, keep_blank_values=True)]
    return urllib.parse.urlunsplit(phan._replace(query=urllib.parse.urlencode(q, safe="[]*")))


def dep_dung_luong(so_byte: float) -> str:
    for don_vi in ("B", "KB", "MB", "GB"):
        if so_byte < 1024 or don_vi == "GB":
            return f"{so_byte:.0f} {don_vi}" if don_vi == "B" else f"{so_byte:.1f} {don_vi}"
        so_byte /= 1024
    return ""


def bao(chu: str) -> None:
    print(chu, file=sys.stderr, flush=True)


def lay_khoa(ten_bien: str, ten_bo: str) -> str:
    gia_tri = os.environ.get(ten_bien, "").strip()
    if not gia_tri:
        raise LoiDuLieu(
            f"thiếu biến môi trường {ten_bien} (bộ '{ten_bo}' cần API key miễn phí).\n"
            f"    Đăng ký: {DANG_KY_KHOA.get(ten_bien, '(xem MOI-TRUONG.md)')}\n"
            f"    Rồi:     export {ten_bien}=...   (hoặc ghi vào tệp .env ở gốc lab, không commit)")
    return gia_tri


def doc_env_tep(thu_muc: Path) -> None:
    """Nạp KEY=VALUE từ .env ở thư mục lab (nếu có) — không ghi đè biến đã export."""
    tep = thu_muc / ".env"
    if not tep.is_file():
        return
    for dong in tep.read_text(encoding="utf-8").splitlines():
        dong = dong.strip()
        if not dong or dong.startswith("#") or "=" not in dong:
            continue
        khoa, _, gia_tri = dong.partition("=")
        khoa = khoa.removeprefix("export ").strip()
        os.environ.setdefault(khoa, gia_tri.strip().strip("'\""))


# ---------------------------------------------------------------------------- HTTP


def mo_url(url: str, tieu_de: dict[str, str] | None = None, bat_dau: int = 0):
    """urlopen có thử lại khi 429/5xx/lỗi mạng; tôn trọng Retry-After."""
    tieu_de = {"User-Agent": TAC_NHAN, **(tieu_de or {})}
    if bat_dau:
        tieu_de["Range"] = f"bytes={bat_dau}-"
    loi_cuoi: Exception | None = None
    for lan in range(SO_LAN_THU):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=tieu_de), timeout=60)
        except urllib.error.HTTPError as loi:
            if loi.code == 416 and bat_dau:  # tệp .part đã đủ
                raise
            if loi.code not in (408, 425, 429, 500, 502, 503, 504):
                raise
            loi_cuoi = loi
            cho = loi.headers.get("Retry-After", "")
            cho_giay = min(int(cho), CHO_TOI_DA) if cho.isdigit() else min(2 ** (lan + 1), CHO_TOI_DA)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as loi:
            loi_cuoi = loi
            cho_giay = min(2 ** (lan + 1), CHO_TOI_DA)
        if lan < SO_LAN_THU - 1:
            bao(f"    … lỗi tạm thời ({loi_cuoi}), thử lại sau {cho_giay} giây")
            time.sleep(cho_giay)
    assert loi_cuoi is not None
    raise loi_cuoi


def tai_ve_tep(url: str, dich: Path, tieu_de: dict[str, str] | None = None) -> None:
    """Tải URL về `dich`, tiếp tục được nếu đang dở (tệp .part + Range)."""
    tam = dich.with_name(dich.name + ".part")
    da_co = tam.stat().st_size if tam.exists() else 0
    try:
        phan_hoi = mo_url(url, tieu_de, bat_dau=da_co)
    except urllib.error.HTTPError as loi:
        if loi.code == 416 and da_co:
            tam.replace(dich)
            return
        raise
    with phan_hoi:
        if da_co and phan_hoi.status != 206:  # máy chủ không hỗ trợ Range: tải lại từ đầu
            da_co = 0
        tong = phan_hoi.headers.get("Content-Length")
        tong = int(tong) + da_co if tong and tong.isdigit() else None
        da_tai, lan_bao = da_co, time.monotonic()
        with open(tam, "ab" if da_co else "wb") as f:
            while khoi := phan_hoi.read(1 << 20):
                f.write(khoi)
                da_tai += len(khoi)
                if sys.stderr.isatty() and time.monotonic() - lan_bao > 2:
                    phan_tram = f" ({100 * da_tai / tong:.0f}%)" if tong else ""
                    bao(f"    … {dep_dung_luong(da_tai)}{phan_tram}")
                    lan_bao = time.monotonic()
    tam.replace(dich)


def tai_khoang_byte(url: str, dich: Path, bat_dau: int, do_dai: int, tieu_de: dict[str, str] | None = None) -> None:
    """Tải đúng một khoảng byte (vd một biến trong tệp GRIB2 theo offset của tệp .index)."""
    tieu_de = {"User-Agent": TAC_NHAN, **(tieu_de or {}), "Range": f"bytes={bat_dau}-{bat_dau + do_dai - 1}"}
    with urllib.request.urlopen(urllib.request.Request(url, headers=tieu_de), timeout=120) as phan_hoi:
        if phan_hoi.status != 206:
            raise LoiDuLieu(f"máy chủ không hỗ trợ tải theo khoảng byte (HTTP {phan_hoi.status}) tại {url}")
        du_lieu = phan_hoi.read()
    if len(du_lieu) != do_dai:
        raise LoiDuLieu(f"nhận {len(du_lieu)} byte, cần {do_dai}")
    dich.write_bytes(du_lieu)


def giai_thich_http(loi: urllib.error.HTTPError, url: str) -> str:
    goi_y = {
        401: "chưa xác thực hoặc API key sai",
        403: "bị từ chối — key không có quyền, hoặc chưa chấp nhận điều khoản của nguồn",
        404: "không còn tệp ở URL này — nguồn đã đổi đường dẫn; cập nhật danh mục dữ liệu",
        429: "bị giới hạn tần suất — chờ vài phút rồi chạy lại",
    }.get(loi.code, "")
    return f"HTTP {loi.code} tại {an_bi_mat(url)}" + (f" — {goi_y}" if goi_y else "")


# ---------------------------------------------------------------------------- cache


class Cache:
    """Kho tệp theo sha256: cache/sha256/ab/abcdef… ; tệp đang tải nằm ở cache/tam/."""

    def __init__(self, goc: Path):
        self.goc = goc
        (goc / "sha256").mkdir(parents=True, exist_ok=True)
        (goc / "tam").mkdir(parents=True, exist_ok=True)

    def duong_dan(self, sha: str) -> Path:
        return self.goc / "sha256" / sha[:2] / sha

    def co(self, sha: str) -> Path | None:
        p = self.duong_dan(sha)
        if not p.is_file():
            return None
        if sha256_tep(p) != sha:  # hỏng (ai đó sửa tệp đã hardlink ra lab) → bỏ, tải lại
            bao(f"    ! tệp trong cache hỏng, tải lại: {p}")
            p.unlink()
            return None
        return p

    def them(self, tep: Path, sha: str | None = None) -> tuple[Path, str]:
        """Đưa tệp vào cache (move), trả về (đường dẫn trong cache, sha256)."""
        sha = sha or sha256_tep(tep)
        dich = self.duong_dan(sha)
        dich.parent.mkdir(parents=True, exist_ok=True)
        if dich.exists():
            tep.unlink()
        else:
            os.replace(tep, dich)
            dich.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        return dich, sha

    def tep_tam(self, ten: str) -> Path:
        return self.goc / "tam" / ten


# ---------------------------------------------------------------------------- nguồn


def _tai_http_co_kiem(bo: dict, cache: Cache, urls: list[str]) -> Path:
    """Tải từ danh sách URL (thử lần lượt) vào cache; kiểm sha256 nếu bộ có chốt."""
    sha_chot = bo.get("sha256")
    if sha_chot and (p := cache.co(sha_chot)):
        return p
    loi_gap: list[str] = []
    for url in urls:
        tam = cache.tep_tam(hashlib.sha1(url.encode()).hexdigest())
        bao(f"    tải {an_bi_mat(url)}")
        tieu_de = {}
        lien_he = os.environ.get("KHOA_FORECASTING_LIEN_HE", "").strip()
        if bo.get("can_lien_he"):
            if not lien_he:
                raise LoiDuLieu("nguồn này (vd BLS) từ chối yêu cầu không có thông tin liên hệ trong User-Agent.\n"
                                "      Đặt email của bạn:  export KHOA_FORECASTING_LIEN_HE=ban@vi-du.com")
            tieu_de["User-Agent"] = f"{TAC_NHAN} lien-he:{lien_he}"
        if url.startswith("https://huggingface.co/") and os.environ.get("HF_TOKEN"):
            tieu_de["Authorization"] = f"Bearer {os.environ['HF_TOKEN']}"  # ẩn danh: 3.000 lượt/5 phút/IP
        loi_mang: Exception | None = None
        for lan in range(SO_LAN_THU):  # đứt GIỮA LÚC TRUYỀN (UCI hay bị): tiếp từ .part hoặc tải lại
            try:
                if bo.get("khoang_byte"):
                    tai_khoang_byte(url, tam, *bo["khoang_byte"], tieu_de)
                else:
                    tai_ve_tep(url, tam, tieu_de)
                loi_mang = None
                break
            except urllib.error.HTTPError as loi:
                loi_mang = loi
                break
            except (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException,
                    OSError) as loi:
                loi_mang = loi
                if lan < SO_LAN_THU - 1:
                    bao(f"    … đứt kết nối khi đang tải ({loi}), thử lại lần {lan + 2}/{SO_LAN_THU}")
                    time.sleep(min(2 ** (lan + 1), CHO_TOI_DA))
        if isinstance(loi_mang, urllib.error.HTTPError):
            loi_gap.append(giai_thich_http(loi_mang, url))
            continue
        if loi_mang is not None:
            loi_gap.append(f"lỗi mạng tại {an_bi_mat(url)} sau {SO_LAN_THU} lần thử: {loi_mang}")
            continue
        sha_that = sha256_tep(tam)
        if sha_chot and sha_that != sha_chot:
            tam.unlink()
            loi_gap.append(
                f"sha256 KHÔNG KHỚP tại {an_bi_mat(url)}\n"
                f"        chốt:    {sha_chot}\n        tải về:  {sha_that}\n"
                "        → nguồn đã đổi nội dung (sửa số liệu lùi, đóng gói lại). KHÔNG sửa sha256"
                " cho khớp:\n          báo tác giả khoá để kiểm tra và cập nhật danh mục/mirror.")
            continue
        p, _ = cache.them(tam, sha_that)
        return p
    raise LoiDuLieu("không tải được từ nguồn nào:\n      - " + "\n      - ".join(loi_gap))


def nguon_http(bo: dict, cache: Cache) -> Path:
    urls = []
    uu_tien_goc = os.environ.get("KHOA_FORECASTING_UU_TIEN") == "goc"
    if bo.get("url_mirror") and not uu_tien_goc:
        urls.append(bo["url_mirror"])
    urls.append(bo["url"])
    if bo.get("url_mirror") and uu_tien_goc:
        urls.append(bo["url_mirror"])
    return _tai_http_co_kiem(bo, cache, urls)


def url_hf(repo: str, revision: str, duong_dan: str) -> str:
    return (f"https://huggingface.co/datasets/{repo}/resolve/{revision}/"
            + urllib.parse.quote(duong_dan))


def nguon_hf(bo: dict, cache: Cache) -> Path:
    return _tai_http_co_kiem(bo, cache, [url_hf(bo["repo"], bo["revision"], bo["duong_dan"])])


def nguon_kaggle(bo: dict, cache: Cache) -> Path:
    """Trả về THƯ MỤC chứa các tệp đã kiểm sha256 (tep_sha256) trong cache."""
    ma = bo["kaggle"]  # "competition:m5-forecasting-accuracy" hoặc "dataset:owner/slug"
    loai, _, ten = ma.partition(":")
    tep_sha: dict[str, str] = bo["tep_sha256"]
    if all(cache.co(s) for s in tep_sha.values()):
        return _gom_thu_muc(cache, tep_sha, ten.replace("/", "__"))

    try:
        import kagglehub
        from kagglehub.exceptions import KaggleApiHTTPError, UnauthenticatedError
    except ImportError as loi:
        raise LoiDuLieu("nguồn Kaggle cần gói kagglehub — chạy qua `python lab.py up` của buổi "
                        "(venv của buổi đã có), hoặc `uv pip install kagglehub`.") from loi

    luat = f"https://www.kaggle.com/competitions/{ten}/rules"
    tam = cache.tep_tam("kaggle-" + ten.replace("/", "__"))
    shutil.rmtree(tam, ignore_errors=True)
    try:
        if loai == "competition":
            thu_muc = kagglehub.competition_download(ten, output_dir=str(tam))
        elif loai == "dataset":
            thu_muc = kagglehub.dataset_download(ten, output_dir=str(tam))
        else:
            raise LoiDuLieu(f"trường kaggle phải bắt đầu bằng competition: hoặc dataset:, gặp '{ma}'")
    except UnauthenticatedError as loi:
        raise LoiDuLieu(
            "chưa đăng nhập Kaggle. Một trong các cách (xem MOI-TRUONG.md):\n"
            "      kaggle auth login  |  export KAGGLE_API_TOKEN=...  |  lưu token vào ~/.kaggle/access_token\n"
            "      Tạo token: https://www.kaggle.com/settings/api") from loi
    except KaggleApiHTTPError as loi:
        ma_http = getattr(getattr(loi, "response", None), "status_code", None)
        if ma_http == 403 and loai == "competition":
            raise LoiDuLieu(f"Kaggle từ chối (403): tài khoản chưa chấp nhận luật cuộc thi.\n"
                            f"      Mở {luat} → 'I Understand and Accept', rồi chạy lại.") from loi
        if ma_http == 401:
            raise LoiDuLieu("Kaggle báo 401: token sai hoặc hết hạn — tạo token mới "
                            "tại https://www.kaggle.com/settings/api") from loi
        raise LoiDuLieu(f"Kaggle lỗi: {loi}") from loi

    thu_muc = Path(thu_muc)
    for ten_tep, sha in tep_sha.items():
        p = thu_muc / ten_tep
        if not p.is_file():
            raise LoiDuLieu(f"Kaggle không có tệp {ten_tep} — cuộc thi/bộ dữ liệu đã đổi cấu trúc")
        sha_that = sha256_tep(p)
        if sha_that != sha:
            raise LoiDuLieu(f"sha256 KHÔNG KHỚP cho {ten_tep}: chốt {sha}, tải về {sha_that}")
        cache.them(p, sha)
    shutil.rmtree(tam, ignore_errors=True)
    return _gom_thu_muc(cache, tep_sha, ten.replace("/", "__"))


def _gom_thu_muc(cache: Cache, tep_sha: dict[str, str], ten: str) -> Path:
    """Dựng thư mục ảo (hardlink/copy từ cache) cho nguồn nhiều tệp."""
    thu_muc = cache.tep_tam("gom-" + ten)
    shutil.rmtree(thu_muc, ignore_errors=True)
    for ten_tep, sha in tep_sha.items():
        _lien_ket(cache.duong_dan(sha), thu_muc / ten_tep)
    return thu_muc


def _ghi_csv_chuan(dong: list[dict], cot: list[str], dich: Path) -> None:
    """CSV chuẩn hoá để sha256 ổn định: cột cố định, dòng đã sắp, xuống dòng \\n, UTF-8."""
    with open(dich, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cot, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(dong)


def _json(url: str, tieu_de: dict[str, str]) -> dict:
    try:
        with mo_url(url, tieu_de) as phan_hoi:
            return json.load(phan_hoi)
    except urllib.error.HTTPError as loi:
        raise LoiDuLieu(giai_thich_http(loi, url)) from loi


def nguon_eia(bo: dict, cache: Cache) -> Path:
    """EIA API v2: GET /v2/<route>/data/ với tham số cố định, phân trang offset/length."""
    sha_chot = bo.get("sha256")
    if sha_chot and (p := cache.co(sha_chot)):
        return p
    khoa = lay_khoa(KHOA_API["eia"], bo["ten"])
    route = bo["route"].strip("/")
    tham_so: list[tuple[str, str]] = []
    for k, v in bo["tham_so"].items():
        for gia_tri in (v if isinstance(v, list) else [v]):
            tham_so.append((k, str(gia_tri)))
    trang = int(bo.get("trang", 5000))
    dong: list[dict] = []
    offset = 0
    while True:
        q = urllib.parse.urlencode(tham_so + [("offset", str(offset)), ("length", str(trang)),
                                              ("api_key", khoa)], safe="[]")
        du_lieu = _json(f"https://api.eia.gov/v2/{route}/data/?{q}", {})
        phan = du_lieu.get("response", {})
        lo = phan.get("data", [])
        dong.extend(lo)
        tong = int(phan.get("total", 0) or 0)
        bao(f"    EIA {route}: {len(dong)}/{tong} dòng")
        offset += len(lo)
        if not lo or offset >= tong:
            break
    return _luu_csv_api(bo, cache, dong)


def nguon_openaq(bo: dict, cache: Cache) -> Path:
    """OpenAQ API v3: GET /v3/<duong_dan> (vd sensors/123/hours), phân trang page/limit."""
    sha_chot = bo.get("sha256")
    if sha_chot and (p := cache.co(sha_chot)):
        return p
    khoa = lay_khoa(KHOA_API["openaq"], bo["ten"])
    gioi_han = int(bo.get("trang", 1000))
    dong: list[dict] = []
    trang = 1
    while True:
        q = urllib.parse.urlencode({**bo.get("tham_so", {}), "limit": gioi_han, "page": trang})
        du_lieu = _json(f"https://api.openaq.org/v3/{bo['duong_dan'].strip('/')}?{q}",
                        {"X-API-Key": khoa, "Accept": "application/json"})
        lo = du_lieu.get("results", [])
        dong.extend(_phang(x) for x in lo)
        bao(f"    OpenAQ {bo['duong_dan']}: {len(dong)} dòng (trang {trang})")
        if len(lo) < gioi_han:
            break
        trang += 1
        time.sleep(float(bo.get("nghi_giay", 1.0)))  # giữ dưới giới hạn tần suất
    return _luu_csv_api(bo, cache, dong)


def _phang(x: dict, tien_to: str = "") -> dict:
    """{"period": {"datetimeFrom": {"utc": ..}}} -> {"period.datetimeFrom.utc": ..}"""
    ra: dict = {}
    for k, v in x.items():
        khoa = f"{tien_to}{k}"
        if isinstance(v, dict):
            ra.update(_phang(v, khoa + "."))
        elif isinstance(v, list):
            ra[khoa] = json.dumps(v, ensure_ascii=False, sort_keys=True)
        else:
            ra[khoa] = v
    return ra


def _luu_csv_api(bo: dict, cache: Cache, dong: list[dict]) -> Path:
    if not dong:
        raise LoiDuLieu("API trả về 0 dòng — kiểm tra tham số (mã trạm/vùng, khoảng thời gian)")
    cot = bo.get("cot") or sorted({k for d in dong for k in d})
    khoa_sap = bo.get("sap_xep") or cot
    dong.sort(key=lambda d: tuple("" if d.get(k) is None else str(d.get(k)) for k in khoa_sap))
    tam = cache.tep_tam(f"api-{bo['ten']}.csv")
    _ghi_csv_chuan(dong, cot, tam)
    sha_that = sha256_tep(tam)
    sha_chot = bo.get("sha256")
    if sha_chot and sha_that != sha_chot:
        tam.unlink()
        raise LoiDuLieu(
            f"sha256 KHÔNG KHỚP cho dữ liệu API: chốt {sha_chot}, nhận {sha_that}.\n"
            "      Nguồn đã sửa số liệu lùi. Dùng bản mirror (url_mirror) nếu buổi có, hoặc báo tác giả.")
    p, _ = cache.them(tam, sha_that)
    return p


NGUON = {"http": nguon_http, "hf": nguon_hf, "kaggle": nguon_kaggle,
         "eia": nguon_eia, "openaq": nguon_openaq}


# ---------------------------------------------------------------------------- đặt vào lab


def _lien_ket(nguon: Path, dich: Path) -> None:
    """Hardlink từ cache (không tốn đĩa); khác ổ đĩa thì copy. Tệp để chỉ đọc."""
    dich.parent.mkdir(parents=True, exist_ok=True)
    if dich.exists() or dich.is_symlink():
        dich.chmod(stat.S_IWUSR | stat.S_IRUSR)
        dich.unlink()
    try:
        os.link(nguon, dich)
    except OSError:
        shutil.copy2(nguon, dich)
    dich.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def _an_toan(goc: Path, ten: str) -> Path:
    dich = (goc / ten).resolve()
    if not dich.is_relative_to(goc.resolve()):
        raise LoiDuLieu(f"tệp nén chứa đường dẫn thoát ra ngoài: {ten}")
    return dich


def _giai_nen(tep: Path, kieu: str, dich: Path, chi_lay: list[str] | None) -> list[str]:
    ra: list[str] = []

    def muon(ten: str) -> bool:
        return not chi_lay or ten in chi_lay

    if kieu == "zip":
        with zipfile.ZipFile(tep) as z:
            for thong_tin in z.infolist():
                if thong_tin.is_dir() or not muon(thong_tin.filename):
                    continue
                p = _an_toan(dich, thong_tin.filename)
                p.parent.mkdir(parents=True, exist_ok=True)
                with z.open(thong_tin) as vao, open(p, "wb") as ra_tep:
                    shutil.copyfileobj(vao, ra_tep)
                ra.append(thong_tin.filename)
    elif kieu in ("tar", "tar.gz", "tgz", "tar.bz2", "tar.xz"):
        with tarfile.open(tep) as t:
            for thanh_vien in t.getmembers():
                if not thanh_vien.isfile() or not muon(thanh_vien.name):
                    continue
                p = _an_toan(dich, thanh_vien.name)
                p.parent.mkdir(parents=True, exist_ok=True)
                with t.extractfile(thanh_vien) as vao, open(p, "wb") as ra_tep:
                    shutil.copyfileobj(vao, ra_tep)
                ra.append(thanh_vien.name)
    elif kieu == "gz":
        ten = tep.name if not chi_lay else chi_lay[0]
        with gzip.open(tep) as vao, open(dich / ten, "wb") as ra_tep:
            shutil.copyfileobj(vao, ra_tep)
        ra.append(ten)
    else:
        raise LoiDuLieu(f"giai_nen không hỗ trợ '{kieu}' (zip, tar, tar.gz, tgz, tar.bz2, tar.xz, gz)")
    if chi_lay and (thieu := set(chi_lay) - set(ra)):
        raise LoiDuLieu(f"tệp nén thiếu {sorted(thieu)} — nguồn đã đổi cấu trúc")
    for ten in ra:
        (dich / ten).chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    return ra


def _ghi_nguon(bo: dict, dich: Path, sha: str, cac_tep: list[str]) -> None:
    dong = [
        f"{bo.get('tieu_de', bo['ten'])}",
        f"Nguồn:      {bo.get('trang_nguon') or bo.get('url', '')}",
        f"Giấy phép:  {bo.get('giay_phep', '?')}  {bo.get('link_giay_phep', '')}".rstrip(),
    ]
    if bo.get("ghi_nguon"):
        dong.append(f"Trích dẫn:  {bo['ghi_nguon']}")
    if bo.get("khoang_thoi_gian"):
        dong.append(f"Thời gian:  {' → '.join(bo['khoang_thoi_gian'])}")
    dong += [f"sha256:     {sha}", "Tệp:        " + ", ".join(cac_tep)]
    if bo.get("truc_tiep"):
        dong.append(f"TRỰC TIẾP — tải lúc {datetime.now(UTC):%Y-%m-%dT%H:%MZ}, không cố định")
    (dich / "NGUON.txt").write_text("\n".join(dong) + "\n", encoding="utf-8")


def dau_moc(bo: dict) -> str:
    """Chuỗi đại diện cho nội dung chốt của bộ — đổi thì phải đặt lại thư mục raw/<ten>."""
    phan = {k: bo.get(k) for k in ("sha256", "tep_sha256", "giai_nen", "chi_lay", "ten_tep", "giai_nen_long",
                                   "khoang_byte")}
    return hashlib.sha256(json.dumps(phan, sort_keys=True).encode()).hexdigest()


def dat_vao_lab(bo: dict, cache: Cache, goc_raw: Path, lam_moi: bool = False) -> Path:
    dich = goc_raw / bo["ten"]
    moc = dich / ".da-kiem"
    if (not lam_moi and not bo.get("truc_tiep") and moc.is_file()
            and moc.read_text().strip() == dau_moc(bo)):
        return dich

    nguon = NGUON[bo["kieu"]](bo, cache)

    if dich.exists():
        for p in dich.rglob("*"):
            if p.is_file():
                p.chmod(stat.S_IWUSR | stat.S_IRUSR)
        shutil.rmtree(dich)
    dich.mkdir(parents=True)

    if nguon.is_dir():  # kaggle: nhiều tệp
        cac_tep = sorted(bo["tep_sha256"])
        for ten in cac_tep:
            _lien_ket(nguon / ten, dich / ten)
        sha = hashlib.sha256("".join(bo["tep_sha256"][t] for t in cac_tep).encode()).hexdigest()
    else:
        sha = nguon.name
        if bo.get("giai_nen"):
            cac_tep = _giai_nen(nguon, bo["giai_nen"], dich, bo.get("chi_lay"))
            # tệp nén lồng bên trong (vd UCI Beijing: zip trong zip) — giải nén tại chỗ rồi bỏ tệp nén
            for ten_long in bo.get("giai_nen_long", []):
                if ten_long not in cac_tep:
                    raise LoiDuLieu(f"giai_nen_long: không có {ten_long} trong tệp nén")
                long = dich / ten_long
                kieu_long = "zip" if ten_long.lower().endswith(".zip") else "tar.gz"
                cac_tep.remove(ten_long)
                cac_tep += [str(Path(ten_long).parent / t) if Path(ten_long).parent != Path(".") else t
                            for t in _giai_nen(long, kieu_long, long.parent, None)]
                long.chmod(stat.S_IWUSR | stat.S_IRUSR)
                long.unlink()
        else:
            ten = bo.get("ten_tep") or Path(urllib.parse.urlsplit(
                bo.get("url") or bo.get("duong_dan") or bo["ten"]).path).name or bo["ten"]
            _lien_ket(nguon, dich / ten)
            cac_tep = [ten]

    _ghi_nguon(bo, dich, sha, cac_tep)
    moc.write_text(dau_moc(bo) + "\n")
    return dich


# ---------------------------------------------------------------------------- kiểm danh mục


def kiem_bo(bo: dict) -> list[str]:
    """Trả về danh sách vấn đề của một mục dữ liệu (rỗng = hợp lệ). Dùng chung với sinh_nen."""
    van_de = []
    ten = bo.get("ten", "?")
    kieu = bo.get("kieu")
    if kieu not in KIEU_HOP_LE:
        return [f"{ten}: kieu '{kieu}' không hợp lệ ({', '.join(sorted(KIEU_HOP_LE))})"]
    for truong in ("giay_phep", "link_giay_phep", "trang_nguon"):
        if not bo.get(truong):
            van_de.append(f"{ten}: thiếu {truong}")
    if "mirror" not in bo:
        van_de.append(f"{ten}: thiếu mirror = true/false (được phép phân phối lại không)")
    if bo.get("url_mirror") and bo.get("mirror") is not True:
        van_de.append(f"{ten}: có url_mirror nhưng mirror không phải true — giấy phép cấm thì không mirror")

    def la_sha(s: object) -> bool:
        return isinstance(s, str) and len(s) == 64 and all(c in "0123456789abcdef" for c in s)

    if bo.get("cho_sha256"):
        # mục đã rà giấy phép nhưng tác giả chưa tải được để chốt sha256 (vd cần tài khoản Kaggle):
        # được nằm trong danh mục, sinh_nen từ chối đưa vào buổi
        if not isinstance(bo["cho_sha256"], str) or len(bo["cho_sha256"]) < 10:
            van_de.append(f"{ten}: cho_sha256 phải là chuỗi giải thích vì sao chưa chốt sha256")
    elif bo.get("truc_tiep"):
        if not bo.get("ly_do_truc_tiep"):
            van_de.append(f"{ten}: truc_tiep = true phải kèm ly_do_truc_tiep")
    elif kieu == "kaggle":
        tep = bo.get("tep_sha256")
        if not tep or not all(la_sha(s) for s in tep.values()):
            van_de.append(f"{ten}: nguồn kaggle cần tep_sha256 = {{ tệp = sha256 }} đủ 64 hex")
    elif not la_sha(bo.get("sha256")):
        van_de.append(f"{ten}: thiếu sha256 (64 hex) — chỉ bộ truc_tiep mới được bỏ")
    if not bo.get("truc_tiep") and not bo.get("khoang_thoi_gian") and not bo.get("khong_thoi_gian"):
        van_de.append(f"{ten}: thiếu khoang_thoi_gian cố định [bắt đầu, kết thúc]")

    if kieu == "http" and not bo.get("url"):
        van_de.append(f"{ten}: kieu http cần url")
    if kieu == "hf":
        rev = str(bo.get("revision", ""))
        if len(rev) != 40 or any(c not in "0123456789abcdef" for c in rev):
            van_de.append(f"{ten}: kieu hf cần revision là commit sha đủ 40 ký tự (không nhánh/tag)")
        if not bo.get("repo") or not bo.get("duong_dan"):
            van_de.append(f"{ten}: kieu hf cần repo và duong_dan")
    if kieu == "kaggle" and bo.get("mirror"):
        van_de.append(f"{ten}: dữ liệu Kaggle không mirror (luật cuộc thi cấm phân phối lại) — "
                      "nếu bộ thực sự có giấy phép mở, dùng kieu http với nguồn gốc")
    if kieu == "kaggle" and not bo.get("du_phong"):
        van_de.append(f"{ten}: bộ hạn chế phải có du_phong = tên bộ dữ liệu mở thay thế")
    if kieu == "eia" and not (bo.get("route") and bo.get("tham_so")):
        van_de.append(f"{ten}: kieu eia cần route và tham_so")
    if kieu == "openaq" and not bo.get("duong_dan"):
        van_de.append(f"{ten}: kieu openaq cần duong_dan (vd sensors/123/hours)")
    return van_de


def doc_toml(duong_dan: Path) -> list[dict]:
    with open(duong_dan, "rb") as f:
        du_lieu = tomllib.load(f)
    if du_lieu.get("phien_ban", PHIEN_BAN_DINH_DANG) > PHIEN_BAN_DINH_DANG:
        raise LoiDuLieu(f"{duong_dan} dùng định dạng mới hơn công cụ này — chạy lại sinh_nen.py")
    return du_lieu.get("bo", [])


# ---------------------------------------------------------------------------- tóm tắt


def dem_dong(p: Path) -> int | None:
    """Số dòng dữ liệu: CSV/TSV không tính dòng tiêu đề; tệp văn bản khác đếm mọi dòng."""
    ten = p.name.lower()
    if ten.endswith((".csv", ".txt", ".tsv")):
        mo = open
    elif ten.endswith((".csv.gz", ".txt.gz", ".tsv.gz")):
        mo = gzip.open
    else:
        return None
    so = 0
    with mo(p, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            so += khoi.count(b"\n")
    co_tieu_de = ten.removesuffix(".gz").endswith((".csv", ".tsv"))
    return max(so - 1, 0) if co_tieu_de else so


def tom_tat(goc_raw: Path, cac_bo: list[dict]) -> None:
    print(f"{'bộ':<28} {'tệp':<34} {'dung lượng':>10} {'dòng DL':>10}  sha256[:12]")
    for bo in cac_bo:
        dich = goc_raw / bo["ten"]
        for p in sorted(x for x in dich.rglob("*") if x.is_file() and not x.name.startswith(".")
                        and x.name != "NGUON.txt"):
            so_dong = dem_dong(p)
            print(f"{bo['ten']:<28} {str(p.relative_to(dich)):<34} "
                  f"{dep_dung_luong(p.stat().st_size):>10} "
                  f"{'' if so_dong is None else f'{so_dong:,}':>10}  {sha256_tep(p)[:12]}")


# ---------------------------------------------------------------------------- main


def tim_toml(dich: str) -> Path:
    p = Path(dich)
    if p.is_file():
        return p
    for ung_vien in (p / "lab" / "00-nen" / "du-lieu.toml", p / "00-nen" / "du-lieu.toml",
                     p / "du-lieu.toml"):
        if ung_vien.is_file():
            return ung_vien
    raise LoiDuLieu(f"không tìm thấy du-lieu.toml cho '{dich}' — đã chạy tools/sinh_nen.py chưa?")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dich", nargs="?", help="buoi-NN, thư mục lab/00-nen, hoặc đường dẫn du-lieu.toml")
    ap.add_argument("--raw", help="thư mục đặt dữ liệu (mặc định <lab>/du-lieu/raw)")
    ap.add_argument("--chi", help="chỉ các bộ này, cách nhau dấu phẩy")
    ap.add_argument("--lam-moi", action="store_true", help="đặt lại thư mục raw dù đã kiểm")
    ap.add_argument("--tom-tat", action="store_true", help="in bảng tệp/số dòng/sha256 sau khi tải")
    ap.add_argument("--kiem", action="store_true", help="chỉ kiểm du-lieu.toml hợp lệ, không tải")
    ap.add_argument("--sha", metavar="URL", help="tải URL vào cache, in sha256 + dung lượng")
    ap.add_argument("--tac-gia", action="store_true",
                    help="tác giả thêm bộ mới: cho phép thiếu sha256, tải rồi IN sha256 để ghi vào danh mục")
    tham_so = ap.parse_args(argv)

    try:
        cache = Cache(thu_muc_cache())
        if tham_so.sha:
            p = _tai_http_co_kiem({"ten": "sha"}, cache, [tham_so.sha])
            print(f"sha256 = \"{p.name}\"\ndung_luong = {p.stat().st_size}")
            return 0
        if not tham_so.dich:
            ap.error("cần buoi-NN hoặc đường dẫn du-lieu.toml")

        toml = tim_toml(tham_so.dich)
        cac_bo = doc_toml(toml)
        if tham_so.chi:
            muon = set(tham_so.chi.split(","))
            if thieu := muon - {b["ten"] for b in cac_bo}:
                raise LoiDuLieu(f"{toml} không có bộ {sorted(thieu)}")
            cac_bo = [b for b in cac_bo if b["ten"] in muon]

        van_de = [v for bo in cac_bo for v in kiem_bo(bo)
                  if not (tham_so.tac_gia and "sha256" in v)]
        if van_de:
            raise LoiDuLieu(f"{toml} không hợp lệ:\n      - " + "\n      - ".join(van_de))
        if tham_so.kiem:
            print(f"✓ {toml}: {len(cac_bo)} bộ hợp lệ")
            return 0

        lab = toml.resolve().parent.parent  # <lab>/00-nen/du-lieu.toml
        doc_env_tep(lab)
        goc_raw = Path(tham_so.raw) if tham_so.raw else lab / "du-lieu" / "raw"
    except LoiDuLieu as loi:
        bao(f"✗ {loi}")
        return 1

    that_bai = 0
    if not cac_bo:
        bao("Buổi này không có bộ dữ liệu nào cần tải.")
        return 0
    bao(f"Dữ liệu → {goc_raw}   (cache: {cache.goc})")
    for bo in cac_bo:
        bat_dau = time.monotonic()
        try:
            dich = dat_vao_lab(bo, cache, goc_raw, tham_so.lam_moi)
        except LoiDuLieu as loi:
            that_bai += 1
            bao(f"✗ {bo['ten']}: {loi}")
            if bo.get("du_phong"):
                bao(f"      Bộ dự phòng mở: {bo['du_phong']} (xem hướng dẫn trong tài liệu buổi)")
            continue
        giay = time.monotonic() - bat_dau
        if tham_so.tac_gia:
            dong = (dich / "NGUON.txt").read_text(encoding="utf-8").splitlines()
            sha = next(d.split()[-1] for d in dong if d.startswith("sha256:"))
            print(f'[bo.{bo["ten"]}]\nsha256 = "{sha}"   # ghi vào tools/du-lieu/danh-muc.toml')
        bao(f"✓ {bo['ten']:<28} sha256 {'(tác giả, chưa chốt)' if tham_so.tac_gia and not bo.get('sha256') else 'khớp'}  {bo.get('giay_phep', '')}  "
            f"({dich.relative_to(goc_raw.parent.parent) if dich.is_relative_to(goc_raw.parent.parent) else dich}, {giay:.1f}s)")
    if tham_so.tom_tat:
        tom_tat(goc_raw, [b for b in cac_bo if (goc_raw / b["ten"] / ".da-kiem").exists()])
    if that_bai:
        bao(f"\n{that_bai}/{len(cac_bo)} bộ không lấy được — xem thông báo ✗ ở trên.")
    return 1 if that_bai else 0


if __name__ == "__main__":
    sys.exit(main())
