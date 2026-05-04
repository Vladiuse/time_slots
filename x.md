Вот моё предложение по структуре. Разберу логику разбиения и дам рекомендацию.

Логические домены
Из ТЗ выделяются такие сущности:

Пользователи (User с ролями для админов)
Клиенты (юр.лицо + его аккаунты с ролями)
Контейнеры (+ синхронизация из FoxPro)
Слоты времени
Заявки на выгрузку
Уведомления клиентам
Рекомендуемая структура

app/
├── manage.py
├── mypy.ini
├── config/                  # настройки Django (settings, urls, wsgi)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                   # кастомный User + роли админов
├── clients/                 # клиент (юр.лицо) + его аккаунты
├── containers/              # контейнеры + импорт из FoxPro
├── bookings/                # слоты + заявки (вместе)
└── notifications/           # отправка уведомлений
Что в каждом приложении
users
Кастомный User (наследник AbstractUser).
Роли админов: administrator, employee (через поле role или группы).
Не смешивать с клиентскими аккаунтами — это другой контекст.
clients
Client — юр.лицо.
ClientAccount — пользователь, привязанный к клиенту, с ролью master / employee.
Здесь же permissions: «видеть только свои контейнеры/заявки».
containers
Модель Container (номер, дата прибытия, ссылка на Client, статус).
Парсер текстового файла (services/parser.py).
Логика синхронизации: diff между файлом и БД (services/sync.py).
Management-команда + Celery-таска для запуска синхронизации.
bookings
Slot — модель слота (или генерация на лету).
Booking — заявка клиента (+ BookingContainer для связи с контейнерами, если M2M с доп. полями).
Бизнес-правила: лимит на слот, проверка «время в будущем», блокировка приёма.
SystemSetting или отдельная модель BookingFreeze — для закрытия приёма заявок.
notifications
Абстракция отправки (email / in-app / в будущем SMS).
Шаблоны уведомлений.
Celery-таски для асинхронной отправки.
Ключевые решения, которые стоит обсудить
bookings или раздельно slots + bookings?
Я объединил — слот сам по себе простая сущность (время + лимит), отдельное приложение на него избыточно. Но если позже появится сложная логика управления слотами (разные расписания, праздничные дни и т.п.) — можно вынести.

clients vs расширение users?
Можно было бы клиентские аккаунты тоже держать в users, но я бы разделил: админы и клиенты — это две разные подсистемы со своими правилами доступа. Чище читается код, чище permissions.

Префикс apps/ для приложений?
Не нужен. Полезен только когда приложений 10+. У тебя их 5 — плоская структура удобнее.

Имена приложений — английские во мн. числе. Это Django-конвенция (django.contrib.auth, users, polls и т.д.).

Альтернативные имена для bookings
bookings ← моя рекомендация (booking = резервирование времени, устоявшийся термин)
unloads (выгрузки) — ближе к доменному языку
pickups (забор) — тоже доменный термин
requests — не использовать, конфликтует с библиотекой requests
Какой вариант ближе? И решим вопрос со slots — отдельно или внутри bookings.

клиент будет связан с юзером, так? 
а аккаунт сотрудника станции - какаято связь с users  нужна?
Да, оба — через User. Логика такая: всё, что логинится в систему, должно быть User (это требование Django auth). Но сама модель User не должна знать, клиент это или сотрудник станции — иначе она быстро превратится в свалку nullable-полей.

Стандартный паттерн — User + профиль на каждый тип аккаунта.

Схема

User (django auth, минимальные поля: username, email, password)
  ├─ OneToOne → StationStaff (роль: administrator | employee)
  └─ OneToOne → ClientAccount → ForeignKey → Client
                (роль: master | employee)
У юзера должен быть ровно один профиль: либо StationStaff, либо ClientAccount. Это инвариант, его проверяешь в коде/админке.

Код

# users/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass  # пока ничего не добавляем


# clients/models.py
from django.db import models
from users.models import User

class Client(models.Model):
    name: str = models.CharField(max_length=255, unique=True)
    is_blocked: bool = models.BooleanField(default=False)


class ClientAccount(models.Model):
    class Role(models.TextChoices):
        MASTER = "master", "Мастер-аккаунт"
        EMPLOYEE = "employee", "Сотрудник"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_account")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="accounts")
    role: str = models.CharField(max_length=16, choices=Role.choices)


# users/models.py (продолжение — StationStaff здесь же)
class StationStaff(models.Model):
    class Role(models.TextChoices):
        ADMINISTRATOR = "administrator", "Администратор"
        EMPLOYEE = "employee", "Сотрудник"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="station_staff")
    role: str = models.CharField(max_length=16, choices=Role.choices)
Как определять, кто это

def is_client(user: User) -> bool:
    return hasattr(user, "client_account")

def is_station_staff(user: User) -> bool:
    return hasattr(user, "station_staff")
В permissions / middleware / DRF-permission-class пользуешься этими хелперами.

Почему именно так
Одна модель User — Django auth, login, password reset, admin — всё работает «из коробки».
Профиль отдельно — у клиента есть client (привязка к юр.лицу), у админа — нет. Хранить эти поля в одной таблице с nullable — путь к багам.
Роли — TextChoices, не Groups — у тебя ролей мало и они связаны с типом аккаунта (роль master бессмысленна для админа). Groups уместны, когда роли произвольно комбинируются.
ClientAccount живёт в приложении clients — он по смыслу принадлежит клиенту, а не пользователям.
Где разместить StationStaff
Два варианта:

в users/ — если считать его «расширением юзера для станции».
в новом staff/ — если будет много логики (расписания смен, журнал действий админов и т.п.).
Пока хватит users/. Перенести позже легко.