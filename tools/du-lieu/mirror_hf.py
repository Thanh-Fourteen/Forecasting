"""Mirror các bộ được phép phân phối lại (mirror = true) lên Hugging Face Datasets của khoá.

    python tools/du-lieu/mirror_hf.py --repo <org>/khoa-forecasting-du-lieu --chuan-bi   (không cần mạng/token)
    python tools/du-lieu/mirror_hf.py --repo <org>/khoa-forecasting-du-lieu --day-len     (cần HF_TOKEN có quyền ghi)

--chuan-bi  dựng thư mục tools/du-lieu/mirror/<repo>/ gồm: mỗi bộ một thư mục chứa đúng tệp gốc đã kiểm
            sha256 (lấy từ cache — chạy tai_danh_muc.py trước), README.md (thẻ dữ liệu: giấy phép, ghi nguồn,
            trích điều khoản, "không sửa đổi"), và in bảng url_mirror dự kiến.
--day-len   upload_folder lên repo dataset, in commit sha 40 ký tự và các dòng url_mirror để chép vào
            danh-muc.toml. Việc CÔNG BỐ ra ngoài — chỉ chạy khi chủ khoá đồng ý.

Quy tắc (CLAUDE.md, tools/du-lieu/NGHIEN-CUU.md):
  * chỉ bộ mirror = true, KHÔNG bộ cho_sha256, KHÔNG kieu kaggle
  * tệp giữ NGUYÊN BYTE (sha256 như nguồn gốc) — CC BY-ND (ETT) chỉ cho bản sao nguyên vẹn
  * CC BY-SA (ForecastBench): thẻ dữ liệu ghi rõ giấy phép ShareAlike
  * mỗi bộ ghi nguồn, link giấy phép, và câu "tệp không bị sửa đổi" (yêu cầu ghi nguồn của CC BY)
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from lay_du_lieu import Cache, thu_muc_cache  # noqa: E402

GIAY_PHEP_HF = {"CC BY 4.0": "cc-by-4.0", "CC BY-SA 4.0": "cc-by-sa-4.0", "CC BY-ND 4.0": "cc-by-nd-4.0",
                "CC0 1.0": "cc0-1.0"}


def chon_bo(dm: dict) -> list[dict]:
    ra = []
    for ten, b in sorted(dm["bo"].items()):
        if b.get("mirror") and not b.get("cho_sha256") and b["kieu"] in ("http", "hf", "eia", "openaq") \
                and b.get("sha256"):
            ra.append({"ten": ten, **b})
    return ra


def ten_tep(bo: dict) -> str:
    if bo.get("ten_tep"):
        return bo["ten_tep"]
    return Path(bo["url"].split("?")[0]).name if bo.get("url") else f"{bo['ten']}.csv"


def the_du_lieu(repo: str, cac_bo: list[dict]) -> str:
    giay_phep = sorted({GIAY_PHEP_HF.get(b["giay_phep"], "other") for b in cac_bo})
    dong = ["---", f"license: {giay_phep[0] if len(giay_phep) == 1 else 'other'}",
            "license_name: nhieu-giay-phep-theo-tung-thu-muc" if len(giay_phep) > 1 else "",
            "pretty_name: Khoá Forecasting in AI — mirror dữ liệu", "tags: [time-series, forecasting]", "---", "",
            f"# {repo}", "",
            "Bản sao **nguyên byte** (không sửa đổi) của các bộ dữ liệu có giấy phép cho phân phối lại, dùng cho",
            "khoá Forecasting in AI. Mỗi thư mục một bộ; giấy phép của TỪNG bộ ghi dưới đây và là giấy phép áp dụng.",
            "sha256 của mỗi tệp trùng với tệp tải từ nguồn gốc.", ""]
    for b in cac_bo:
        dong += [f"## `{b['ten']}/{ten_tep(b)}` — {b['tieu_de']}", "",
                 f"- Nguồn gốc: {b['trang_nguon']}",
                 f"- Giấy phép: {b['giay_phep']} ({b['link_giay_phep']})",
                 f"- Điều khoản (trích): \"{b.get('trich_giay_phep', '')}\"",
                 f"- Trích dẫn: {b.get('ghi_nguon', '')}",
                 f"- sha256: `{b['sha256']}`",
                 "- Thay đổi: không — tệp giữ nguyên như nguồn gốc", ""]
    return "\n".join(d for d in dong if d is not None) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", required=True)
    nhom = ap.add_mutually_exclusive_group(required=True)
    nhom.add_argument("--chuan-bi", action="store_true")
    nhom.add_argument("--day-len", action="store_true")
    t = ap.parse_args(argv)

    with open(HERE / "danh-muc.toml", "rb") as f:
        dm = tomllib.load(f)
    cac_bo = chon_bo(dm)
    thu_muc = HERE / "mirror" / t.repo.replace("/", "__")
    if t.chuan_bi:
        cache = Cache(thu_muc_cache())
        if thu_muc.exists():
            shutil.rmtree(thu_muc)
        thieu = []
        for b in cac_bo:
            nguon = cache.co(b["sha256"])
            if nguon is None:
                thieu.append(b["ten"])
                continue
            dich = thu_muc / b["ten"] / ten_tep(b)
            dich.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(nguon, dich)
            assert hashlib.sha256(dich.read_bytes()).hexdigest() == b["sha256"]
        (thu_muc / "README.md").write_text(the_du_lieu(t.repo, [b for b in cac_bo if b["ten"] not in thieu]),
                                          encoding="utf-8")
        print(f"✓ {len(cac_bo) - len(thieu)} bộ trong {thu_muc}")
        if thieu:
            print(f"! chưa có trong cache (chạy tai_danh_muc.py): {', '.join(thieu)}")
        return 1 if thieu else 0

    token = os.environ.get("HF_TOKEN")
    if not token:
        sys.exit("✗ cần HF_TOKEN có quyền ghi (https://huggingface.co/settings/tokens)")
    if not (thu_muc / "README.md").is_file():
        sys.exit("✗ chạy --chuan-bi trước")
    from huggingface_hub import HfApi

    api = HfApi(token=token)
    api.create_repo(t.repo, repo_type="dataset", exist_ok=True)
    kq = api.upload_folder(repo_id=t.repo, repo_type="dataset", folder_path=str(thu_muc),
                           commit_message="Mirror nguyên byte các bộ dữ liệu giấy phép mở của khoá")
    sha = kq.oid
    print(f"✓ commit {sha}\nChép vào tools/du-lieu/danh-muc.toml:")
    for b in cac_bo:
        if (thu_muc / b["ten"]).is_dir():
            print(f'[bo.{b["ten"]}]\nurl_mirror = "https://huggingface.co/datasets/{t.repo}/resolve/{sha}/'
                  f'{b["ten"]}/{ten_tep(b)}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
