"""Export a reproducible subset of SROIE to data/processed/ (image + ground-truth JSON).

Example (from repo root, venv active):
    python scripts/prepare_sroie.py --split train --n 50 --seed 42 --out data/processed/sroie_dev

Use the *train* split for the dev subset (tuning prompts/thresholds) and keep *test* untouched
until the final evaluation (see docs/evaluation-plan.md).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from app.datasets.sroie import DEFAULT_ROOT, iter_samples, pick_dev_keys

REPO_ROOT = Path(__file__).resolve().parents[1]


def safe_name(key: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", key)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=["train", "test"], default="train")
    parser.add_argument("--n", type=int, default=50, help="number of receipts")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "data" / "processed" / "sroie_dev")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()

    keys = pick_dev_keys(args.split, args.n, seed=args.seed, root=args.root)
    args.out.mkdir(parents=True, exist_ok=True)

    written = []
    for sample in iter_samples(args.split, root=args.root, keys=set(keys)):
        name = safe_name(sample.key)
        (args.out / f"{name}.jpg").write_bytes(sample.image_bytes)
        truth = {
            "key": sample.key,
            "split": sample.split,
            "image_size": {"width": sample.image_width, "height": sample.image_height},
            "entities": sample.entities,
            "words": sample.words,
            "bboxes": sample.bboxes,
        }
        (args.out / f"{name}.json").write_text(
            json.dumps(truth, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        written.append(name)

    manifest = {"split": args.split, "seed": args.seed, "n": len(written), "keys": sorted(written)}
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {len(written)} receipts to {args.out}")


if __name__ == "__main__":
    main()
