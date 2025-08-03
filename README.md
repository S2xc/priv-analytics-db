# PrivAnalyticsDB

**Zero-trust ClickHouse proxy with AES-256-GCM encryption out-of-the-box.**

## Quick start:

```bash
docker compose up -d
export PA_KEY=$(curl -s -H "Authorization: Bearer demo-key-123" http://localhost:8000/key)
curl -s -H "Authorization: Bearer demo-key-123" \
  -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT 1","fmt":"JSONEachRow"}' \
  | PYTHONPATH=proxy python client/decrypt.py --in - --out -
```
## Example:
```bash
(.venv) (base) s2xdeb@MacBook-Air-s2x priv-analytics-db % curl -s -H "Authorization: Bearer demo-key-123" \
  -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT 1","fmt":"JSONEachRow"}'
```
## Output:
```bash
{"encrypted_data":"P6H0zWUwkb9c3PrnHiRwaCVkYzK8ymOg","key_id":"40607","iv":"cbmkwKZF0zrDfAEc","algorithm":"AES-256-GCM"}% 
```

## launch:
```bash
cd proxy
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
⸻

# 🔹 Назначение

Этот метод используется для выполнения SQL-запросов к аналитической базе данных через промежуточный API-сервис (прокси). Прокси отвечает за выполнение запроса, шифрование результата и возврат безопасного зашифрованного ответа. Такой подход применяется для защиты данных при передаче, особенно если содержимое запроса может быть конфиденциальным.

## 🔹 Метод запроса

POST /query

HTTP-запрос к локальному серверу (по умолчанию http://localhost:8000/query).

## 🔹 Запрос

Пример запроса:

```bash
curl -s -H "Authorization: Bearer demo-key-123" \
  -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT 1","fmt":"JSONEachRow"}'
```

Объяснение параметров:

Элемент запроса	Назначение
Authorization: Bearer demo-key-123	Заголовок авторизации. Используется для проверки прав пользователя.
Content-Type: application/json	Указывает, что тело запроса — JSON.
-d '{"query":"...","fmt":"..."}'	JSON-объект с SQL-запросом и форматом результата.

Поля тела запроса:

Поле	Тип	Описание
query	string	SQL-запрос, который будет выполнен через ClickHouse.
fmt	string	Формат вывода результата. Например, JSONEachRow или JSON.

В данном примере SELECT 1 — простой запрос для проверки соединения и корректности обработки запроса.

## 🔹 Ответ

Пример:
```bash
{
  "encrypted_data": "P6H0zWUwkb9c3PrnHiRwaCVkYzK8ymOg",
  "key_id": "40607",
  "iv": "cbmkwKZF0zrDfAEc",
  "algorithm": "AES-256-GCM"
}
```
Описание полей:

Поле	Описание
encrypted_data	Зашифрованный результат SQL-запроса. Данные представлены в Base64.
key_id	Идентификатор ключа, использованного для шифрования.
iv	Вектор инициализации (Initialization Vector) — обязательный параметр для AES-GCM.
algorithm	Алгоритм шифрования, всегда AES-256-GCM.

Этот ответ не содержит открытых данных — результат запроса зашифрован. Для расшифровки клиенту необходимо использовать ключ с соответствующим key_id.

## 🔹 Дешифровка на клиенте

Результат можно расшифровать локально, используя утилиту:

echo '{...}' | PYTHONPATH=proxy python client/decrypt.py

Утилита должна уметь:
	•	найти ключ по key_id;
	•	использовать iv и algorithm для расшифровки;
	•	вывести оригинальные данные, полученные от ClickHouse.

## 🔹 Назначение архитектуры

Этот подход повышает безопасность при передаче аналитических данных. Даже если перехватить сетевой трафик, данные невозможно расшифровать без доступа к ключам. Такой механизм может быть частью архитектуры, где клиент и сервер физически разделены и только клиенту доступны ключи дешифровки.
