from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import httpx, base64
from crypto import encrypt

app = FastAPI(title="PrivAnalyticsDB Proxy")
CH_URL = "http://demo:demo@localhost:8123"
security = HTTPBearer(auto_error=False)
API_KEYS = {"demo-key-123"}

class QueryRequest(BaseModel):
    query: str
    fmt: str = "JSONEachRow"

def require_key(creds: HTTPAuthorizationCredentials = Security(security)):
    if creds is None or creds.credentials not in API_KEYS:
        raise HTTPException(401, "Invalid or missing API key")
    return creds.credentials

@app.post("/query")
async def run_query(req: QueryRequest, _=Depends(require_key)):
    async with httpx.AsyncClient(timeout=30) as client:
        raw = await client.post(
            CH_URL,
            params={"query": req.query, "default_format": req.fmt}
        )
    key_id, iv, ct = encrypt(raw.text.encode())
    return {
        "encrypted_data": base64.b64encode(ct).decode(),
        "key_id": key_id,
        "iv": base64.b64encode(iv).decode(),
        "algorithm": "AES-256-GCM"
    }

@app.get("/key")
async def get_key(_=Depends(require_key)):
    from crypto import keyring
    key_id, _ = keyring.current()
    return {"key_id": key_id}