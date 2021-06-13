from fastapi import Cookie
from routers.secure import auth
from typing import Optional


async def cookie_extractor(access_token: Optional[str] = Cookie(None)):
    if not access_token:
        return None
    if access_token:
        try:
            check_session = auth.verify_session_cookie(access_token)
            auth.revoke_refresh_tokens(check_session['sub'])
            return access_token
        except auth.RevokedSessionCookieError:
            return None
        except auth.InvalidSessionCookieError:
            return None
    return None
