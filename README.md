# QamqorParser API

##  Решение задачи без обхода reCAPTCHA
Я решил данную задачу **простым способом**, без программного обхода капчи.

###  Шаг 1: Перейти на сайт
Открой страницу:
```
https://qamqor.gov.kz/criminals
```

###  Шаг 2: Получить `re_captcha` токен вручную
1. Нажми `F12`, чтобы открыть DevTools  
2. Перейди на вкладку **"Сеть" / Network**  
3. Выполни поиск по любой фамилии (например: `Сакенов`)  
4. Найди запрос, начинающийся с:
```
/api/public/person_case/criminal?page=0&...&re_captcha=...
```
5. Скопируй значение параметра `re_captcha` из запроса

###  Шаг 3: Вставь токен в код
Открой файл `main.py` и вставь токен:
```python
CAPTCHA_STUB = "your token"  # вставь свой актуальный токен
```

##  Важно
- Токен действителен 1–2 минуты
- Он одноразовый и привязан к браузерной сессии
- Если токен устарел — API вернёт ошибку:
```json
{
  "code": "controller::recaptcha",
  "status": "error",
  "data": {}
}
```

##  Установка и запуск

###  Требования
- Python 3.8+
- pip

###  Установка зависимостей
```bash
pip install fastapi uvicorn httpx
```

### ▶ Запуск сервера
```bash
uvicorn main:app --reload
```

После запуска открой в браузере:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

##  Пример запроса
```http
GET /search/by-lastname?last_name=Сакенов&page=0
```

Пример ответа:
```json
{
  "data": {
    "items": [...],
    "totalElements": 3,
    "totalPages": 1
  },
  "code": "OK",
  "status": "success",
  "time": "..."
}
```

##  Правовая информация
Проект создан исключительно в учебных целях.
Использование данных должно соответствовать законодательству и условиям использования сайта qamqor.gov.kz.
