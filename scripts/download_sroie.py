"""Download SROIE mirror from Hugging Face into data/raw/sroie."""
from pathlib import Path

from huggingface_hub import snapshot_download

REPO_ID = "jsdnrs/ICDAR2019-SROIE"
TARGET = Path(__file__).resolve().parents[1] / "data" / "raw" / "sroie"


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    path = snapshot_download(repo_id=REPO_ID, repo_type="dataset", local_dir=TARGET)
    print(f"Downloaded to: {path}")
    for f in sorted(Path(path).rglob("*")):
        if f.is_file() and ".cache" not in f.parts:
            print(f"{f.relative_to(path)}  ({f.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()