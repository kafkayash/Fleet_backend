# backend/app/config.py
from pathlib import Path
import os

# --- PATH HELPERS (bulletproof for Render + local) ---

APP_DIR = Path(__file__).resolve().parent          # backend/app
BACKEND_DIR = APP_DIR.parent                      # backend
REPO_DIR = BACKEND_DIR.parent                     # repo root

def _first_existing_dir(candidates: list[Path]) -> Path:
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]  # fallback (so debug endpoints show "expected path")

def _find_file(filename: str, candidates: list[Path]) -> Path:
    for base in candidates:
        p = base / filename
        if p.exists():
            return p
    return candidates[0] / filename

# Candidate locations depending on Render "Root Directory"
_ARTIFACT_DIR_CANDIDATES = [
    BACKEND_DIR / "artifacts",               # if code runs from backend/
    REPO_DIR / "backend" / "artifacts",      # if code runs from repo root
    Path.cwd() / "artifacts",                # if cwd == backend
    Path.cwd() / "backend" / "artifacts",    # if cwd == repo root
]

_DATA_DIR_CANDIDATES = [
    BACKEND_DIR / "app" / "data",            # your current structure: backend/app/data
    BACKEND_DIR / "data",                    # if you later move it to backend/data
    REPO_DIR / "backend" / "app" / "data",
    Path.cwd() / "app" / "data",
    Path.cwd() / "backend" / "app" / "data",
]

# Allow overriding directories via env (optional)
ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR")) if os.getenv("ARTIFACTS_DIR") else _first_existing_dir(_ARTIFACT_DIR_CANDIDATES)
DATA_DIR      = Path(os.getenv("DATA_DIR")) if os.getenv("DATA_DIR") else _first_existing_dir(_DATA_DIR_CANDIDATES)

# --- ARTIFACT FILE PATHS ---
# Allow overriding each file via env too (optional). If env is not set, we auto-find.

FEAT_DF_CSV = Path(os.getenv("FEAT_DF_CSV")) if os.getenv("FEAT_DF_CSV") else _find_file("feat_df_all_vehicles.csv", _ARTIFACT_DIR_CANDIDATES)

FEATURES_CFG_JSON = Path(os.getenv("FEATURES_CFG_JSON")) if os.getenv("FEATURES_CFG_JSON") else _find_file("features_f1.json", _ARTIFACT_DIR_CANDIDATES)
SEQ2SEQ_MODEL     = Path(os.getenv("SEQ2SEQ_MODEL"))     if os.getenv("SEQ2SEQ_MODEL")     else _find_file("seq2seq1_f1.keras", _ARTIFACT_DIR_CANDIDATES)
GPR_RESIDUAL_PKL  = Path(os.getenv("GPR_RESIDUAL_PKL"))  if os.getenv("GPR_RESIDUAL_PKL")  else _find_file("gpr_residual.pkl", _ARTIFACT_DIR_CANDIDATES)
CA_SCALER_PKL     = Path(os.getenv("CA_SCALER_PKL"))     if os.getenv("CA_SCALER_PKL")     else _find_file("ca_scaler.pkl", _ARTIFACT_DIR_CANDIDATES)
F_SCALER_PKL      = Path(os.getenv("F_SCALER_PKL"))      if os.getenv("F_SCALER_PKL")      else _find_file("f_scaler.pkl", _ARTIFACT_DIR_CANDIDATES)
X2_SCALER_PKL     = Path(os.getenv("X2_SCALER_PKL"))     if os.getenv("X2_SCALER_PKL")     else _find_file("x2_scaler.pkl", _ARTIFACT_DIR_CANDIDATES)

# SMTP / email config
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM") or SMTP_USER

# Password reset token config
SECRET_KEY = os.getenv("SECRET_KEY", "dev_change_me_secret_key")
RESET_TOKEN_EXP_MIN = int(os.getenv("RESET_TOKEN_EXP_MIN", "30"))

# Frontend base URL (for building password reset links)
# Your React frontend is on 3000 (per your setup), so default to 3000.
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
