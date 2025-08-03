import httpx
from fastapi import HTTPException

CH_URL = "http://demo:demo@localhost:8123"

async def run_clickhouse_query(query: str, fmt: str = "JSONEachRow") -> str:
    params = {"query": query}
    if fmt:
        params["default_format"] = fmt
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(CH_URL, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.text