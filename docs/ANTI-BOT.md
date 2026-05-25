# Anti-Bot, Proxy, and Fingerprinting Disclaimer

This document defines the constraints and strategies for job board scraping, ensuring compliance and platform stability.

## Constraints

- **Respect robots.txt:** The platform must respect `robots.txt` constraints for all scraped domains.
- **No CAPTCHA Solving:** The platform must not implement or use any CAPTCHA solving or bypassing mechanisms.
- **No Authenticated Scraping:** The platform must not perform authenticated scraping of LinkedIn (or other platforms where it violates Terms of Service).

## Browser Fingerprinting Strategy

To ensure reliable discovery without triggering aggressive blocks, the scraper agents employ the following strategies:
- User-Agent Rotation
- Viewport Randomisation
- Context Isolation
- Proxy Abstraction
- Residential Proxy Support (implemented in MVP 2)

## Proxy Abstraction Layer

A proxy abstraction layer will be introduced in MVP 2 to route Playwright traffic through rotating residential proxies. This prevents IP-based rate limiting when running scheduled global scraping tasks.

## Compliance Disclaimer & Terms of Service

This software is for personal intelligence and orchestration use. Users run scraping agents locally or within their own dedicated cloud environments. The developer of this platform is not responsible for any Terms of Service violations incurred by the user running the scraping workloads.
