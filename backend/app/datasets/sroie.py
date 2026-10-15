"""Loader for the SROIE parquet mirror (jsdnrs/ICDAR2019-SROIE).

Columns (from the dataset card): image {bytes, path}, key, image_size {width, height},
entities {company, date, address, total}, words, bboxes.
Parquet files are read in small batches so the ~500 MB dataset never sits in memory at once.
"""

from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

DEFAULT_ROOT = Path(__file__).resolve().parents[3] / "data" / "raw" / "sroie"
ENTITY_FIELDS = ("company", "date", "address", "total")


@dataclass(frozen=True)
class SroieSample:
    key: str
    split: str
    image_bytes: bytes
    image_width: int | None
    image_height: int | None
    entities: dict[str, str | None]
    words: list[str]
    bboxes: list[list[int]]


def parquet_path(split: str, root: Path = DEFAULT_ROOT) -> Path:
    matches = sorted((root / "data").glob(f"{split}-*.parquet"))
    if not matches:
        raise FileNotFoundError(f"No parquet file for split '{split}' under {root / 'data'}")
    return matches[0]


def list_keys(split: str, root: Path = DEFAULT_ROOT) -> list[str]:
    table = pq.read_table(parquet_path(split, root), columns=["key"])
    return table.column("key").to_pylist()


def pick_dev_keys(split: str, n: int, seed: int = 42, root: Path = DEFAULT_ROOT) -> list[str]:
    """Deterministic random subset of keys (sorted first so the seed is reproducible)."""
    keys = sorted(list_keys(split, root))
    rng = random.Random(seed)
    return sorted(rng.sample(keys, min(n, len(keys))))


def _row_to_sample(row: dict, split: str) -> SroieSample:
    image = row.get("image") or {}
    size = row.get("image_size") or {}
    entities = row.get("entities") or {}
    return SroieSample(
        key=row["key"],
        split=split,
        image_bytes=image.get("bytes") or b"",
        image_width=size.get("width"),
        image_height=size.get("height"),
        entities={name: entities.get(name) for name in ENTITY_FIELDS},
        words=list(row.get("words") or []),
        bboxes=[list(b) for b in (row.get("bboxes") or [])],
    )


def iter_samples(
    split: str,
    root: Path = DEFAULT_ROOT,
    keys: set[str] | None = None,
    batch_size: int = 8,
) -> Iterator[SroieSample]:
    """Yield samples of a split, optionally restricted to a set of keys."""
    pf = pq.ParquetFile(parquet_path(split, root))
    key_array = pa.array(sorted(keys)) if keys is not None else None
    for batch in pf.iter_batches(batch_size=batch_size):
        if key_array is not None:
            batch = batch.filter(pc.is_in(batch.column("key"), value_set=key_array))
            if batch.num_rows == 0:
                continue
        for row in batch.to_pylist():
            yield _row_to_sample(row, split)
