from pathlib import Path
import sys
import shutil


def copy_tests(from_dir):
    to_path = Path(__file__).parent / "python_environment" / "tests"
    to_path.mkdir(parents=True, exist_ok=True)
    from_path = Path(from_dir).resolve()
    if not from_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {from_path}")
    for item in from_path.rglob("*"):
        relative_path = item.relative_to(from_path)
        dest_path = to_path / relative_path
        if item.is_file():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(item, dest_path)
        elif item.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    copy_tests(sys.argv[1])
