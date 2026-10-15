"""Print structure of the SROIE parquet files (schema + first rows, truncated)."""
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1] / "data" / "raw" / "sroie"


def short(v, limit=300):
    if isinstance(v, (bytes, bytearray)):
        return f"<bytes len={len(v)}>"
    if isinstance(v, dict):
        return {k: short(x, limit) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return f"<list len={len(v)}> first={[short(x, limit) for x in v[:3]]}"
    s = repr(v)
    return s if len(s) <= limit else s[:limit] + f"... <len={len(s)}>"


for name in ["train", "test"]:
    path = next((ROOT / "data").glob(f"{name}-*.parquet"))
    pf = pq.ParquetFile(path)
    print("=" * 70)
    print(path.name, "| rows:", pf.metadata.num_rows)
    print(pf.schema_arrow)
    batch = next(pf.iter_batches(batch_size=2))
    for i, row in enumerate(batch.to_pylist()):
        print(f"--- row {i} ---")
        for col, val in row.items():
            print(f"{col}: {short(val)}")

print("=" * 70)
print("README (first 60 lines):")
print("\n".join((ROOT / "README.md").read_text(encoding="utf-8").splitlines()[:60]))
print("=" * 70)
print("NOTICE:")
print((ROOT / "NOTICE").read_text(encoding="utf-8")[:1500])
print("LICENSE (first 5 lines):")
print("\n".join((ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()[:5]))