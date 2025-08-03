# PrivAnalyticsDB

**Zero-trust ClickHouse proxy with AES-256-GCM encryption out-of-the-box.**

## Quick start

```bash
docker compose up -d
export PA_KEY=$(curl -s -H "Authorization: Bearer demo-key-123" http://localhost:8000/key)
curl -s -H "Authorization: Bearer demo-key-123" \
  -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT 1","fmt":"JSONEachRow"}' \
  | PYTHONPATH=proxy python client/decrypt.py --in - --out -

