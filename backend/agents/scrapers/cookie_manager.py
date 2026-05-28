import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
from ...logging_config import get_logger

logger = get_logger(__name__)

class CookieManager:
    """
    Manages session cookies for Playwright scraping contexts to handle session-based
    pagination and circumvent strict unauthenticated limits (e.g., LinkedIn li_at).
    """

    def __init__(self, storage_path: str | Path | None = None):
        if storage_path is None:
            project_root = Path(__file__).parent.parent.parent.parent
            storage_path = project_root / "data" / "cookies.json"
            
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.cookies: List[Dict] = []
        self._load_cookies()

    def _load_cookies(self) -> None:
        """Load cookies from storage or environment variables."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.cookies = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load cookies from {self.storage_path}: {e}")
                self.cookies = []
                
        # Also check env vars for injection (e.g., LinkedIn li_at)
        li_at = os.environ.get("LINKEDIN_LI_AT")
        if li_at:
            self.add_cookie({
                "name": "li_at",
                "value": li_at,
                "domain": ".linkedin.com",
                "path": "/",
                "secure": True,
                "expires": time.time() + 86400 * 30 # 30 days
            })

    def save_cookies(self, cookies: List[Dict]) -> None:
        """Save updated cookies from a Playwright session."""
        self.cookies = cookies
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.cookies, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")

    def add_cookie(self, cookie: Dict) -> None:
        """Add or update a specific cookie."""
        self.cookies = [
            c for c in self.cookies 
            if not (c.get("name") == cookie.get("name") and c.get("domain") == cookie.get("domain"))
        ]
        self.cookies.append(cookie)
        self.save_cookies(self.cookies)

    def get_cookies_for_domain(self, domain: str) -> List[Dict]:
        """Get valid cookies for a specific domain."""
        current_time = time.time()
        valid_cookies = []
        for c in self.cookies:
            if domain in c.get("domain", ""):
                expires = c.get("expires", -1)
                # Check expiry if set (Playwright sets expires as unix timestamp)
                if expires == -1 or expires > current_time:
                    valid_cookies.append(c)
        return valid_cookies

    def clear_cookies(self, domain: Optional[str] = None) -> None:
        """Clear all cookies, or cookies for a specific domain."""
        if domain:
            self.cookies = [c for c in self.cookies if domain not in c.get("domain", "")]
        else:
            self.cookies = []
        self.save_cookies(self.cookies)
        
    def is_session_expired(self, domain: str, critical_cookie_name: str) -> bool:
        """Check if a specific session cookie is missing or expired."""
        domain_cookies = self.get_cookies_for_domain(domain)
        for c in domain_cookies:
            if c.get("name") == critical_cookie_name:
                return False
        return True
