from __future__ import annotations

from paypay_swing import inject_into_reports, run


if __name__ == "__main__":
    payload = run(".")
    inject_into_reports(".")
    print(f"PayPay swing monitor complete: {payload.get('research_status', {}).get('status', 'unknown')}")
