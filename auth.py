import json
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

try:
    file = open("accounts.json")
    accounts = json.load(file)
except FileNotFoundError:
    # For Testing
    accounts = json.loads(
        '{"1111-2222-3333": {"plan": "free"},'
        '"2222-1111-3333": {"plan": "pro"},'
        '"3333-1111-2222": {"plan": "enterprise"}}'
    )


class Auth(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.headers.get("authorization") not in accounts:
            return JSONResponse(status_code=403, content={"error": "Invalid request!"})
        else:
            request.account = accounts[request.headers.get("authorization")]
            return await call_next(request)
