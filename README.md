# Проект YaMDb

![Python](https://img.shields.io/badge/Python-313131?style=flat&logo=Python&logoColor=white&labelColor=306998)
![Django](https://img.shields.io/badge/Django-313131?style=flat&logo=django&labelColor=092e20)
![DjangoREST](https://img.shields.io/badge/Django-REST-313131?style=flat&logo=django&logoColor=white&color=ff1709&labelColor=313131)
![SQLite](https://img.shields.io/badge/SQLite-313131?style=flat&logo=sqlite&logoColor=ffffff&labelColor=033b55)
![Visual Studio](https://img.shields.io/badge/VS%20Code-313131?style=flat&logo=visualstudiocode&logoColor=ffffff&labelColor=0098FF)

## Проект YaMDb собирает отзывы пользователей на произведения.  
**Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.**  
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

### Над проектом работали:

- [Бобков Константин](https://github.com/deltabobkov) - тимлид
- [Корбаков Иван](https://github.com/nir0k)
- [Фёдоров Антон](https://github.com/Anton-1991128)

### Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/deltabobkov/api_yamdb.git

cd api_final_yatube
```

2. Cоздать и активировать виртуальное окружение:

```
python -m venv venv

source env/Scripts/activate
```

3. Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip

pip install -r requirements.txt
```

4. Выполнить миграции:

```
python manage.py migrate
```

5. Запустить проект:

```
python manage.py runserver
```

## Кратское описание API

### AUTH
Регистрация пользователей и выдача токенов
#### Регистрация пользователя

Получить код подтверждения на переданный email. Права доступа: Доступно без токена. Использовать имя 'me' в качестве username запрещено. Поля email и username должны быть уникальными.
<details>
<summary>Пример POST-запроса:</summary>

```
/auth/signup/
Payload:
{
  "email": "user@example.com",
  "username": "string"
}
```
Пример ответа:
```
{
  "email": "string",
  "username": "string"
}
```
</details>

#### Получение JWT-токена
Получение JWT-токена в обмен на username и confirmation code. Права доступа: Доступно без токена.
<details>
<summary>Пример POST-запроса:</summary>

```
/auth/token/
Payload:
{
  "username": "string",
  "confirmation_code": "string"
}
```
Пример ответа:
```
{
  "token": "string"
}
```
</details>

### CATEGORIES
Категории (типы) произведений

#### Получение списка всех категорий
Получить список всех категорий Права доступа: Доступно без токена

<details>
<summary>Пример GET-запроса:</summary>

```
/categories/
```
Пример ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
</details>

#### Добавление новой категории
Создать категорию. Права доступа: Администратор. Поле slug каждой категории должно быть уникальным.

<details>
<summary>Пример POST-запроса:</summary>

```
/categories/
Payload:
{
  "name": "string",
  "slug": "string"
}
```
Пример ответа:
```
{
  "name": "string",
  "slug": "string"
}
```
</details>

### GENRES
Категории жанров

#### Получение списка всех жанров
Получить список всех жанров. Права доступа: Доступно без токена

<details>
<summary>Пример GET-запроса:</summary>

```
/genres/
```
Пример ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
</details>

#### Добавление жанра
Добавить жанр. Права доступа: Администратор. Поле slug каждого жанра должно быть уникальным.

<details>
<summary>Пример POST-запроса:</summary>

```
/genres/
Payload:
{
  "name": "string",
  "slug": "string"
}
```
Пример ответа:
```
{
  "name": "string",
  "slug": "string"
}
```
</details>

### TITLES
Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

#### Получение списка всех произведений
Получить список всех объектов. Права доступа: Доступно без токена

<details>
<summary>Пример GET-запроса:</summary>

```
/titles/
```
Пример ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
</details>

#### Добавление произведения
Добавить новое произведение. Права доступа: Администратор. Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего). При добавлении нового произведения требуется указать уже существующие категорию и жанр.

<details>
<summary>Пример POST-запроса:</summary>

```
/titles/
Payload:
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
</details>

#### Получение информации о произведении
Информация о произведении Права доступа: Доступно без токена

<details>
<summary>Пример GET-запроса:</summary>

```
/titles/{titles_id}/
```
Пример ответа:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
</details>

### REVIEWS
Отзывы

#### Получение списка всех отзывов
Получить список всех отзывов. Права доступа: Доступно без токена.

<details>
<summary>Пример GET-запроса:</summary>

```
/titles/{title_id}/reviews/
```
Пример ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
</details>

#### Добавление нового отзыва
Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение. Права доступа: Аутентифицированные пользователи.

<details>
<summary>Пример POST-запроса:</summary>

```
/titles/{title_id}/reviews/
Payload:
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
</details>

#### Полуение отзыва по id
Получить отзыв по id для указанного произведения. Права доступа: Доступно без токена.
<details>
<summary>Пример GET-запроса:</summary>

```
/titles/{title_id}/reviews/{review_id}/
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
</details>

#### Частичное обновление отзыва по id
Частично обновить отзыв по id. Права доступа: Автор отзыва, модератор или администратор.

<details>
<summary>Пример PATCH-запроса:</summary>

```
/titles/{title_id}/reviews/{review_id}/
Payload:
{
  "text": "string",
  "score": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
</details>

### COMMENTS
Комментарии к отзывам

#### Получение списка всех комментариев к отзыву
Получить список всех комментариев к отзыву по id Права доступа: Доступно без токена.


<details>
<summary>Пример GET-запроса:</summary>

```
/titles/{title_id}/reviews/{review_id}/comments/
```
Пример ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
</details>

#### Добавление комментария к отзыву
Добавить новый комментарий для отзыва. Права доступа: Аутентифицированные пользователи.

<details>
<summary>Пример POST-запроса:</summary>

```
/titles/{title_id}/reviews/{review_id}/comments/
Payload:
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
</details>

#### Получение комментария к отзыву
Получить комментарий для отзыва по id. Права доступа: Доступно без токена.

<details>
<summary>Пример GET-запроса:</summary>

```
/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
</details>

#### Частичное обновление комментария к отзыву
Частично обновить комментарий к отзыву по id. Права доступа: Автор комментария, модератор или администратор.

<details>
<summary>Пример PATCH-запроса:</summary>

```
/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Payload:
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
</details>

### USERS
Пользователи

#### Получение списка всех пользователей
Получить список всех пользователей. Права доступа: Администратор
<details>
<summary>Пример GET-запроса:</summary>

```
/users/
```
Пример ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
}
```
</details>

#### Добавление пользователя
Добавить нового пользователя. Права доступа: Администратор Поля email и username должны быть уникальными.
<details>
<summary>Пример POST-запроса:</summary>

```
/users/
Payload:
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
</details>

#### Получение пользователя по username
Получить пользователя по username. Права доступа: Администратор
<details>
<summary>Пример GET-запроса:</summary>

```
/users/{username}/
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
</details>

#### Изменение данных пользователя по username
Изменить данные пользователя по username. Права доступа: Администратор. Поля email и username должны быть уникальными.

<details>
<summary>Пример PATCH-запроса:</summary>

```
/users/{username}/
Payload:
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
</details>

#### Получение данных своей учетной записи
Получить данные своей учетной записи Права доступа: Любой авторизованный пользователь

<details>
<summary>Пример GET-запроса:</summary>

```
/users/me/
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
</details>

#### Изменение данных своей учетной записи
Изменить данные своей учетной записи Права доступа: Любой авторизованный пользователь Поля email и username должны быть уникальными.

<details>
<summary>Пример PATCH-запроса:</summary>

```
/users/{username}/
Payload:
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```
Пример ответа:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
</details>
