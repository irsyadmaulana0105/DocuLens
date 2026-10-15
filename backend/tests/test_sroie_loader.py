from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from app.datasets.sroie import iter_samples, list_keys, pick_dev_keys

SCHEMA = pa.schema(
    [
        ("image", pa.struct([("bytes", pa.binary()), ("path", pa.string())])),
        ("key", pa.string()),
        ("image_size", pa.struct([("width", pa.int64()), ("height", pa.int64())])),
        (
            "entities",
            pa.struct(
                [
                    ("company", pa.string()),
                    ("date", pa.string()),
                    ("address", pa.string()),
                    ("total", pa.string()),
                ]
            ),
        ),
        ("words", pa.list_(pa.string())),
        ("bboxes", pa.list_(pa.list_(pa.int64()))),
    ]
)


def make_root(tmp_path: Path, n: int = 12) -> Path:
    rows = [
        {
            "image": {"bytes": f"img{i}".encode(), "path": f"{i}.jpg"},
            "key": f"X{i:04d}",
            "image_size": {"width": 100 + i, "height": 200 + i},
            "entities": {
                "company": f"SHOP {i}",
                "date": "01/02/2018",
                "address": "JALAN 1",
                "total": f"{i}.00",
            },
            "words": ["SHOP", str(i)],
            "bboxes": [[1, 2, 3, 4], [5, 6, 7, 8]],
        }
        for i in range(n)
    ]
    (tmp_path / "data").mkdir()
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    pq.write_table(table, tmp_path / "data" / "train-0-of-1.parquet")
    return tmp_path


def test_iter_all_samples(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    samples = list(iter_samples("train", root=root, batch_size=5))
    assert len(samples) == 12
    first = samples[0]
    assert first.key == "X0000"
    assert first.image_bytes == b"img0"
    assert (first.image_width, first.image_height) == (100, 200)
    assert first.entities["company"] == "SHOP 0"
    assert first.words == ["SHOP", "0"]
    assert first.bboxes == [[1, 2, 3, 4], [5, 6, 7, 8]]


def test_filter_by_keys(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    samples = list(iter_samples("train", root=root, keys={"X0003", "X0009"}, batch_size=4))
    assert [s.key for s in samples] == ["X0003", "X0009"]


def test_pick_dev_keys_is_deterministic(tmp_path: Path) -> None:
    root = make_root(tmp_path)
    a = pick_dev_keys("train", 5, seed=1, root=root)
    b = pick_dev_keys("train", 5, seed=1, root=root)
    assert a == b
    assert len(a) == 5
    assert set(a) <= set(list_keys("train", root))
