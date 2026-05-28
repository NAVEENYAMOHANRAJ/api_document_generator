import sys
import os
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parent
SITE_PACKAGES = BACKEND_DIR / "venv" / "Lib" / "site-packages"

sys.path.insert(0, str(BACKEND_DIR))
if SITE_PACKAGES.exists():
    sys.path.insert(0, str(SITE_PACKAGES))


import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8001")),
    )
