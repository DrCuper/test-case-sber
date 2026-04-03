import os
import sys
from flower.__main__ import main

if __name__ == "__main__":
    port = os.getenv("PORT", "5555")
    broker = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")

    sys.argv = [
        "flower",
        f"--broker={broker}",
    ]

    sys.exit(main())