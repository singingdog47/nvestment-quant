"""Explicit, review-scoped user consent for provisional analysis.

Consent never verifies missing disclosures and never authorizes order execution.
"""
from hashlib import sha256
import json

def review_fingerprint(preflight):
    payload = {"as_of_utc": preflight["as_of_utc"],
               "positions": [(p["symbol"], p["state"], p["decision_gate"])
                             for p in preflight["positions"]]}
    return sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

def apply_user_consent(preflight, consent=None):
    """consent: {'approved': True, 'review_fingerprint': fingerprint}.

    Absent, stale, or negative consent requires an interactive question.
    """
    pending = preflight.get("approval_required", False)
    fingerprint = review_fingerprint(preflight)
    if not pending:
        return {"state": "VERIFIED_REVIEW", "provisional_analysis_allowed": True,
                "trade_execution_allowed": False, "fingerprint": fingerprint}
    accepted = (isinstance(consent, dict) and consent.get("approved") is True
                and consent.get("review_fingerprint") == fingerprint)
    return {"state": "PROVISIONAL_USER_APPROVED" if accepted else "ASK_USER",
            "provisional_analysis_allowed": bool(accepted),
            "trade_execution_allowed": False,
            "fingerprint": fingerprint,
            "unverified_symbols": [p["symbol"] for p in preflight["positions"]
                                   if p["decision_gate"].startswith("BLOCK")],
            "question_ja": None if accepted else
            "決算・適時開示の未確認銘柄があります。未確認であることを前提に、今回の暫定分析・売買判断を続けてよいですか？",
            "warning_ja": "未確認情報は確認済みとして扱いません。注文は自動実行しません。"}
