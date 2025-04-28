from fastapi import Request

async def get_token_from_cookie(request: Request)->str:
    token = request.cookies.get("access_token")
    return token