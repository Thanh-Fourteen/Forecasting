"""du_lieu: đọc .tsf của Monash, dạng dài theo khai báo dang_dai, báo lỗi khi chưa python lab.py up."""
import pandas as pd
import pytest

from tv import du_lieu

TSF = """# Dataset mẫu
@relation mau
@attribute series_name string
@attribute state string
@attribute start_timestamp date
@frequency monthly
@horizon 3
@missing true
@equallength false
@data
T1:NSW:2020-01-31 00-00-00:1,2,?,4
T2:VIC:2021-03-01 00-00-00:5.5,6
"""


def test_doc_tsf(tmp_path):
    p = tmp_path / "mau.tsf"
    p.write_text(TSF)
    df, meta = du_lieu.doc_tsf(p)
    assert meta["frequency"] == "monthly" and meta["horizon"] == "3"
    assert list(df.columns) == ["unique_id", "ds", "y", "state"]
    t1 = df[df.unique_id == "T1"]
    # bước tháng giữ ngày bắt đầu, không nhảy về cuối/đầu tháng sai
    assert list(t1["ds"]) == [pd.Timestamp("2020-01-31"), pd.Timestamp("2020-02-29"),
                              pd.Timestamp("2020-03-31"), pd.Timestamp("2020-04-30")]
    assert t1["y"].isna().sum() == 1
    assert len(du_lieu.doc_tsf(p, gioi_han_chuoi=1)[0]["unique_id"].unique()) == 1


def test_tsf_khong_timestamp(tmp_path):
    p = tmp_path / "x.tsf"
    p.write_text("@attribute series_name string\n@frequency yearly\n@data\nA:1,2,3\n")
    df, _ = du_lieu.doc_tsf(p)
    assert list(df["ds"]) == [0, 1, 2]


def _nen_gia(tmp_path, monkeypatch, co_du_lieu=True):
    nen = tmp_path / "lab" / "00-nen"
    nen.mkdir(parents=True)
    (nen / "du-lieu.toml").write_text(
        'phien_ban = 1\n[[bo]]\nten = "xe"\nkieu = "http"\n'
        'dang_dai = { tep = "hour.csv", ds = "ngay", gio = "gio", y = "cnt", id = "xe" }\n'
        '[[bo]]\nten = "m4"\nkieu = "http"\n', encoding="utf-8")
    monkeypatch.setenv("KHOA_FORECASTING_NEN", str(nen))
    raw = tmp_path / "lab" / "du-lieu" / "raw"
    if co_du_lieu:
        (raw / "xe").mkdir(parents=True)
        (raw / "xe" / ".da-kiem").write_text("x")
        (raw / "xe" / "NGUON.txt").write_text("nguồn")
        (raw / "xe" / "hour.csv").write_text("ngay,gio,cnt\n2024-01-01,1,5\n2024-01-01,0,3\n")
        (raw / "m4").mkdir(parents=True)
        (raw / "m4" / ".da-kiem").write_text("x")
        (raw / "m4" / "m4.tsf").write_text(TSF)
    return raw


def test_doc_du_lieu_dang_dai(tmp_path, monkeypatch):
    _nen_gia(tmp_path, monkeypatch)
    assert du_lieu.danh_sach() == ["m4", "xe"]
    df = du_lieu.doc_du_lieu("xe")
    assert list(df.columns) == ["unique_id", "ds", "y"]
    assert list(df["ds"]) == [pd.Timestamp("2024-01-01 00:00"), pd.Timestamp("2024-01-01 01:00")]
    assert list(df["y"]) == [3, 5]
    m4 = du_lieu.doc_du_lieu("m4")
    assert m4["unique_id"].nunique() == 2
    assert du_lieu.duong_dan("m4").name == "m4.tsf"


def test_chua_make_up(tmp_path, monkeypatch):
    _nen_gia(tmp_path, monkeypatch, co_du_lieu=False)
    with pytest.raises(FileNotFoundError, match="lab.py up"):
        du_lieu.doc_du_lieu("xe")
    with pytest.raises(KeyError, match="không có bộ"):
        du_lieu.thong_tin("khong-co")


def test_kiem_dang_dai_bat_trung():
    df = pd.DataFrame({"unique_id": ["a", "a"], "ds": [1, 1], "y": [1.0, 2.0]})
    with pytest.raises(ValueError, match="trùng"):
        du_lieu.kiem_dang_dai(df)
