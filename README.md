# api_yamdb
api_yamdb

## Модель User
Создана на основе AbstractBaseUser.
Пароль больше не является обязательным полем
Так же добавлены кастомные формы для создания и изменения пользователя через адмнику

Поля:
- username
- email
- first_name
- last_name
- is_admin
- bio
- role - Может быть:
    - admin
    - user
    - moderator
- confirm_code

# Добавлена возможность проверки прав для пользователей
(users.permissions.py)

Есть проверки:
- IsAdmin
- IsModerator
- IsUser

Предлагаю использовать их для разграничения прав. Сейчас проверятеся просто наличие нужной роли, можно изменить роли и добавить в них проверку на конкретные дейсвтия или сделать проверку на конкретные обьекты

Привер использования:
```python
# Импорт разрешений
from users.permissions import IsAdmin, IsModerator, IsUser
...

# Права только для администратора
class UserViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = [IsAdmin]
    ...

# Права для Администратора или пользователя
class UserViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = [IsAdmin|IsUser]
    ...

```