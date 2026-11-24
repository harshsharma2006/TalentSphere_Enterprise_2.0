"""
TalentSphere Enterprise 2.0 - Production Healthcheck Probe
Validates application runtime readiness and database connectivity.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from database.session import get_db_session
    from database.models.user import User

    with get_db_session() as db:
        user_count = db.query(User).count()
        print(f"✅ Healthcheck PASS: Database operational. {user_count} registered users found.")
        sys.exit(0)
except Exception as e:
    print(f"❌ Healthcheck FAIL: {str(e)}", file=sys.stderr)
    sys.exit(1)
