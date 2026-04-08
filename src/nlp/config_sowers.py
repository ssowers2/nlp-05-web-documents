from pathlib import Path

# ============================================================
# API CONFIGURATION
# ============================================================

PAGE_URL: str = "https://www.kissnetwork.us/"

HTTP_REQUEST_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (educational-use; web-mining-course)"
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

RAW_HTML_PATH: Path = RAW_PATH / "sowers_raw.html"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "sowers_processed.csv"
