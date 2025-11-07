#!/usr/bin/env python3
"""
File Copy and Archive Tool with Date Range Filtering

Author: Adair John Collins
Description:
    Recursively copies files from a source directory to a target directory
    based on a configurable time window. Supports both relative (last N days)
    and absolute (start/end datetime) ranges. Uses the most reliable available
    file timestamp across platforms (birth time > creation time > mtime).
    After copying, creates a ZIP archive of the target directory.

    Features:
    - Cross-platform timestamp detection
    - Timestomp suspicion detection
    - Resume support via state file
    - SHA256 verification (optional)
    - Robust error handling and logging
    - PEP8 compliant
    - CLI with help, validation, and Jupyter compatibility
    - CLI arguments override hardcoded defaults
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Set


# ================================
# HARDCODED DEFAULT CONFIGURATION
# ================================

DEFAULT_SOURCE_DIR: str = "/tmp/shutil/srcdir"
DEFAULT_TARGET_DIR: str = "/tmp/shutil/dstdir"
DEFAULT_CUTOFF_DAYS: int = 7

# Optional hardcoded absolute range (uncomment to set)
# DEFAULT_START_DATE: Optional[str] = "2025-10-01 00:00:00"
# DEFAULT_END_DATE: Optional[str] = "2025-10-31 23:59:59"
DEFAULT_START_DATE: Optional[str] = None
DEFAULT_END_DATE: Optional[str] = None

# Resume & verify not enabled by default
DEFAULT_RESUME: bool = False
DEFAULT_VERIFY: bool = False


# ================================
# JUPYTER DETECTION
# ================================

def is_jupyter() -> bool:
    """Detect if running in Jupyter (ipykernel or notebook)."""
    return any(arg in sys.argv for arg in ["-f", "ipykernel_launcher.py", "jupyter"])


# ================================
# ARGUMENT PARSER & HELP
# ================================

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser with comprehensive help."""
    parser = argparse.ArgumentParser(
        description="Copy recent files and create a ZIP archive.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
        epilog="""
Examples:
  %(prog)s -s /var/log -t /backup/logs -d 3
  %(prog)s --source /data --target /archive --start "2025-11-01 00:00:00" --end "2025-11-05 23:59:59"
  %(prog)s -s /data -t /out --resume --verify  # Resume + verify
        """.strip(),
    )

    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("-s", "--source", type=str, help="Source directory")
    parser.add_argument("-t", "--target", type=str, help="Target directory")
    parser.add_argument("-d", "--days", type=int, help="Number of recent days")
    parser.add_argument("--start", type=str, help="Start date 'YYYY-MM-DD HH:MM:SS'")
    parser.add_argument("--end", type=str, help="End date 'YYYY-MM-DD HH:MM:SS'")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from previous run (uses .copy_state.json in target dir)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify SHA256 hashes after copy (slower, more accurate)",
    )

    return parser


# ================================
# STATE MANAGEMENT (RESUME)
# ================================

STATE_FILE_NAME = ".copy_state.json"

def load_state(target_path: Path) -> Set[str]:
    """Load set of already-copied relative paths."""
    state_file = target_path / STATE_FILE_NAME
    if not state_file.exists():
        return set()
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("copied", []))
    except (json.JSONDecodeError, OSError) as e:
        print(f"[WARNING] Failed to load state file, starting fresh: {e}")
        return set()


def save_state(target_path: Path, copied_paths: Set[str]) -> None:
    """Save current state."""
    state_file = target_path / STATE_FILE_NAME
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump({"copied": sorted(copied_paths)}, f, indent=2)
    except OSError as e:
        print(f"[WARNING] Failed to save state: {e}")


# ================================
# SHA256 VERIFICATION
# ================================

def compute_sha256(path: Path) -> str:
    """Compute SHA256 hash of file."""
    hash_obj = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except OSError as e:
        print(f"[ERROR] Failed to hash {path}: {e}")
        return ""


def verify_copy(src: Path, dst: Path) -> bool:
    """Compare SHA256 of source and destination."""
    src_hash = compute_sha256(src)
    dst_hash = compute_sha256(dst)
    if not src_hash or not dst_hash:
        return False
    if src_hash != dst_hash:
        print(f"[VERIFY FAILED] Hash mismatch: {src} -> {dst}")
        return False
    return True


# ================================
# VALIDATION FUNCTIONS
# ================================

def validate_directory(path: str, label: str, must_exist: bool = True) -> Path:
    if not path:
        raise argparse.ArgumentTypeError(f"{label} cannot be empty.")
    dir_path = Path(path).expanduser().resolve()
    if must_exist and not dir_path.exists():
        raise argparse.ArgumentTypeError(f"{label} does not exist: {dir_path}")
    if must_exist and not dir_path.is_dir():
        raise argparse.ArgumentTypeError(f"{label} is not a directory: {dir_path}")
    if must_exist and not os.access(dir_path, os.R_OK):
        raise argparse.ArgumentTypeError(f"{label} is not readable: {dir_path}")
    return dir_path


def validate_positive_int(value: str) -> int:
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("must be > 0")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError("must be a valid integer") from None


def validate_datetime(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-MM-DD HH:MM:SS")
    except ValueError:
        raise argparse.ArgumentTypeError("must be in format 'YYYY-MM-DD HH:MM:SS'") from None


# ================================
# CORE FUNCTIONS
# ================================

def get_timestamp(path: Path) -> Optional[datetime]:
    try:
        stat = path.stat()
        if hasattr(stat, "st_birthtime"):
            return datetime.fromtimestamp(stat.st_birthtime)
        if os.name == "nt":
            return datetime.fromtimestamp(stat.st_ctime)
        return datetime.fromtimestamp(stat.st_mtime)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] Failed to read timestamp for {path}: {exc}")
        return None


def is_suspicious_timestamp(file_time: datetime, path: Path) -> bool:
    now = datetime.now()
    stat = path.stat()
    if file_time > now + timedelta(minutes=5):
        return True
    times = [datetime.fromtimestamp(stat.st_mtime), datetime.fromtimestamp(stat.st_ctime)]
    if hasattr(stat, "st_birthtime"):
        times.append(datetime.fromtimestamp(stat.st_birthtime))
    if len(set(times)) == 1:
        return True
    if file_time.year < 2000 or file_time.year > now.year + 1:
        return True
    return False


# ================================
# MAIN LOGIC
# ================================

def main() -> None:
    if is_jupyter():
        print("Jupyter detected: Using hardcoded defaults. CLI args ignored.")
        args = argparse.Namespace(
            source=None, target=None, days=None, start=None, end=None,
            resume=False, verify=False
        )
    else:
        parser = create_parser()
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        try:
            args = parser.parse_args()
        except SystemExit:
            return

    # === Resolve paths ===
    source_dir = args.source or DEFAULT_SOURCE_DIR
    try:
        source_path = validate_directory(source_dir, "Source directory", must_exist=True)
    except argparse.ArgumentTypeError as e:
        print(f"[FATAL] Invalid source: {e}")
        sys.exit(1)

    target_dir = args.target or DEFAULT_TARGET_DIR
    try:
        target_path = validate_directory(target_dir, "Target directory", must_exist=False)
    except argparse.ArgumentTypeError as e:
        print(f"[FATAL] Invalid target: {e}")
        sys.exit(1)

    # === Resolve date range ===
    start_dt: Optional[datetime] = None
    end_dt: Optional[datetime] = None

    if args.start and args.end:
        try:
            start_dt = validate_datetime(args.start)
            end_dt = validate_datetime(args.end)
            if start_dt > end_dt:
                print("[FATAL] Start date must be <= end date.")
                sys.exit(1)
            print(f"Using CLI date range: {start_dt} to {end_dt}")
        except argparse.ArgumentTypeError as e:
            print(f"[FATAL] Invalid date: {e}")
            sys.exit(1)
    elif DEFAULT_START_DATE and DEFAULT_END_DATE:
        try:
            start_dt = validate_datetime(DEFAULT_START_DATE)
            end_dt = validate_datetime(DEFAULT_END_DATE)
            if start_dt > end_dt:
                print("[FATAL] Hardcoded start date must be <= end date.")
                sys.exit(1)
            print(f"Using hardcoded date range: {start_dt} to {end_dt}")
        except argparse.ArgumentTypeError as e:
            print(f"[FATAL] Invalid hardcoded date: {e}")
            sys.exit(1)
    else:
        cutoff_days = args.days or DEFAULT_CUTOFF_DAYS
        try:
            cutoff_days = validate_positive_int(str(cutoff_days))
        except argparse.ArgumentTypeError as e:
            print(f"[FATAL] Invalid --days: {e}")
            sys.exit(1)
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=cutoff_days)
        print(f"Using relative range: last {cutoff_days} day(s) to {start_dt} to {end_dt}")

    # === Setup resume & verify ===
    resume = args.resume or DEFAULT_RESUME
    verify = args.verify or DEFAULT_VERIFY

    if resume:
        print(f"Resume enabled: Loading state from {target_path / STATE_FILE_NAME}")
    if verify:
        print("SHA256 verification enabled (slower)")

    # === Create target dir ===
    try:
        os.makedirs(target_path, exist_ok=True)
    except OSError as exc:
        print(f"[FATAL] Cannot create target directory '{target_path}': {exc}")
        sys.exit(1)

    # Load resume state
    copied_paths = load_state(target_path) if resume else set()

    copied_count = len(copied_paths)
    verified_count = 0
    suspicious_count = 0

    print(f"Scanning: {source_path}")

    for file_path in source_path.rglob("*"):
        if not file_path.is_file():
            continue

        rel_path_str = str(file_path.relative_to(source_path))
        if resume and rel_path_str in copied_paths:
            continue  # Skip already copied

        file_time = get_timestamp(file_path)
        if file_time is None:
            continue

        if is_suspicious_timestamp(file_time, file_path):
            print(f"[SUSPICIOUS] Possible timestomping: {rel_path_str} ({file_time})")
            suspicious_count += 1

        if start_dt <= file_time <= end_dt:
            dst_path = target_path / file_path.relative_to(source_path)

            try:
                os.makedirs(dst_path.parent, exist_ok=True)
            except OSError as exc:
                print(f"[ERROR] Failed to create directory {dst_path.parent}: {exc}")
                continue

            try:
                shutil.copy2(file_path, dst_path)
                copied_count += 1
                print(f"Copied ({copied_count}): {rel_path_str}")

                # Optional verification
                if verify:
                    if verify_copy(file_path, dst_path):
                        verified_count += 1
                    else:
                        print(f"[VERIFY FAILED] Removing corrupt copy: {dst_path}")
                        dst_path.unlink(missing_ok=True)
                        copied_count -= 1
                        continue

                # Save state
                if resume:
                    copied_paths.add(rel_path_str)
                    save_state(target_path, copied_paths)

            except (shutil.Error, OSError) as exc:
                print(f"[ERROR] Failed to copy {file_path} to {dst_path}: {exc}")

    # Final state save
    if resume and copied_paths:
        save_state(target_path, copied_paths)

    # === Archive ===
    try:
        archive_name = shutil.make_archive(
            base_name="target_archive",
            format="zip",
            root_dir=target_path,
        )
        print(f"\nArchive created: {archive_name}")
        print(f"Total files copied: {copied_count}")
        if verify:
            print(f"Verified with SHA256: {verified_count}")
        if suspicious_count:
            print(f"Suspicious files detected: {suspicious_count}")
        if resume:
            print(f"Resume state saved to: {target_path / STATE_FILE_NAME}")
    except Exception as exc:
        print(f"[ERROR] Failed to create archive: {exc}")


# ================================
# ENTRY POINT
# ================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Operation cancelled by user.")
        sys.exit(130)
    except Exception as exc:
        print(f"[FATAL] Unexpected error: {exc}")
        sys.exit(1)
