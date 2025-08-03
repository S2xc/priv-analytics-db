#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Запуск e2e-теста PrivAnalyticsDB…"

# 0. Проверить, что сервер жив
curl -s http://localhost:8000/docs >/dev/null || {
  echo "❌ Сервер не доступен на :8000"
  exit 1
}

# 1. Выполнить запрос
resp=$(curl -s -H "Authorization: Bearer demo-key-123" \
  -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT 42 as answer","fmt":"JSONEachRow"}')

# 2. Расшифровать
result=$(echo "$resp" | PYTHONPATH=proxy python client/decrypt.py --in - --out - | jq -r '.answer')

# 3. Проверить результат
if [[ "$result" == "42" ]]; then
  echo "✅ e2e пройден"
else
  echo "❌ e2e провалено: получили '$result'"
  exit 1
fi
