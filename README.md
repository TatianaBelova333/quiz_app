# QuizApp
Приложение для формирования и прохождения тестов. 
Тесты содержат набор вопросов с указанием правильного ответа (Да / Нет). 
По результатам тестирования можно получить общую информацию о следующих показателях (о тесте):
- Количество прохождений теста;
- Процент успешного прохождения (если кол-во правильных ответов 50% и выше);
- Самый сложный вопрос (вопрос с наименьшим процентом правильных ответов).

### Requirements & Compatibility
* Django==5.0.4
* django-filter==24.2
* djangorestframework==3.15.1

### Installation

- Клонировать репозиторий
  ```
  git clone https://github.com/TatianaBelova333/quiz_app.git
  ```
- Создать .env файл на основе .env.example.

- Перейти из корня проекта в папку scr:
  ```
  cd src
  ```
- Создать и активировать окружение (python3.11):

  ```
  python3 -m venv env
  ```
  ```
  source env/bin/activate
  ```
- Установить зависимости
  ```
  pip install -r requirements.txt
  ```
- Запустить миграции:
  ```
  python3 manage.py migrate
  ```
- Заполнить базу тестовыми данными
  ```
  python3 manage.py loaddata question 
  ```
- Создать superuser:
  ```
  python manage.py createsuperuser
  ```
- Запустить проект
  ```
  python3 manage.py runserver
  ```

# API SOME REST API EXAMPLES
### SWagger API documentation is available at 
`http://127.0.0.1:8000/swagger/`
### Получить список вопросов
  ```
   GET http://127.0.0.1:8000/api/questions/
  ```

  ```
  HTTP/1.1 200 OK
  Content-Type: application/json

 [
  {
    "id": 1,
    "text": "Django - это микрофреймворк?"
  },
  {
    "id": 2,
    "text": "GET - это идемпотентный HTTP метод?"
  },
  {
    "id": 3,
    "text": "PATCH - это идемпотентный HTTP метод?"
  },
  {
    "id": 4,
    "text": "Python имеет  динамическую строгую типизацию?"
  },
  {
    "id": 5,
    "text": "SQL является декларативным языком?"
  }
  ]
  ```

### Получить список тестов

```
GET http://127.0.0.1:8000/api/quizzes/
```
```
  HTTP/1.1 200 OK
  Content-Type: application/json

  [
  {
    "id": 1,
    "title": "Основы Python",
    "questions": [
      {
        "id": 4,
        "text": "Python имеет  динамическую строгую типизацию?"
      },
      {
        "id": 8,
        "text": "Функции map() и filter() возвращают итератор"
      }
    ]
  },
  {
    "id": 2,
    "title": "Основы SQL",
    "questions": [
      {
        "id": 5,
        "text": "SQL является декларативным языком?"
      },
      {
        "id": 13,
        "text": "SELECT является SQL-оператором для извлечения информации из базы данных"
      }
    ]
  },
  {
    "id": 3,
    "title": "Основы программирования",
    "questions": [
      {
        "id": 1,
        "text": "Django - это микрофреймворк?"
      },
      {
        "id": 5,
        "text": "SQL является декларативным языком?"
      }
    ]
  }
]
```

### Получить отчет о тесте

```
GET http://127.0.0.1:8000/api/quizzes/{id}/report/
```

```
HTTP/1.1 200 OK
  Content-Type: application/json


{
  "number_of_attempts": 15,
  "attempts_success_rate": 26,
  "most_difficult_questions": [
    {
      "question_id": 4,
      "text": "Python имеет  динамическую строгую типизацию?",
      "right_answer_pct": 20
    },
    {
      "question_id": 11,
      "text": "Функция range() возвращает итератор?",
      "right_answer_pct": 20
    }
  ]
}
```
### Пройти тест

```
POST http://127.0.0.1:8000/api/attempts/

{
  "quiz": 3,
  "answers": [
    {
      "question": 1,
      "given_answer": true
    },
    {
     "question": 5,
      "given_answer": true
    }
  ]
}
```

```
Content-Type: application/json
HTTP/1.1 201 Created

{
  "id": 87,
  "quiz": 3,
  "attempt_date": "2024-05-07T09:43:03.000974Z",
  "result": 50,
  "answers": [
    {
      "id": 216,
      "attempt": 87,
      "question": 1,
      "given_answer": true,
      "is_correct": false
    },
    {
      "id": 217,
      "attempt": 87,
      "question": 5,
      "given_answer": true,
      "is_correct": true
    }
  ]
}

```

### Получить список всех прохождений теста

```
GET http://127.0.0.1:8000/api/attempts/?quiz=3
```

```
[
  {
    "id": 87,
    "quiz": 3,
    "attempt_date": "2024-05-07T09:43:03.000974Z",
    "result": 50,
    "answers": [
      {
        "id": 216,
        "attempt": 87,
        "question": 1,
        "given_answer": true,
        "is_correct": false
      },
      {
        "id": 217,
        "attempt": 87,
        "question": 5,
        "given_answer": true,
        "is_correct": true
      }
    ]
  },
  {
    "id": 66,
    "quiz": 3,
    "attempt_date": "2024-05-06T16:19:50.593609Z",
    "result": 0,
    "answers": [
      {
        "id": 129,
        "attempt": 66,
        "question": 5,
        "given_answer": false,
        "is_correct": false
      },
      {
        "id": 130,
        "attempt": 66,
        "question": 1,
        "given_answer": true,
        "is_correct": false
      }
    ]
  }
]
```

# Authors
[Tatiana Belova](https://github.com/TatianaBelova333)