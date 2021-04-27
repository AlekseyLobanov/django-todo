
# ToDo список на Python

## Структура проекта
- **backend**. Бекенд приложения на Django + Postgres.
Для запуска необходим docker-compose.
- **frontend**. Фронт приложения на Python + tkinter.
- **docs**. Документация по проекту и ресурсы для неё

Тесты проектов лежат в подпапках `tests`.

## Как мы ведём разрботку

### Перед началом
1. Необходим docker + docker-compose для запуска бекенда.
2. Надо установить [pre-commit](https://pre-commit.com/) для валидации коммитов на локальной машине

### Стратегия ветвления
- master -> стабильная ветка
- develop -> текущая dev ветка
- release/X, где X=1,2,3,... -> ветка для стабилизации develop
- [feat/fix/hotfix/config]_KEY.description -> ветка для задачи, относящаяся к типу фичи, фикса, хотфикса или изменений не связанных с кодом

Путь кода: ветка задачи -> develop -> release/X -> master.
Коммиты в master только через PR из релизной ветки

### Стиль
Используем стандартные соглашения Python + ограничения в pre-commit.
Комментарии и сообщеия коммитов русские, по возможности.

Зависимости отдельные на каждый из подпроектов. Используём жёсткую фиксацию зависимостей.

## Как запустить проект
### Frontend
```bash
python3 todo_tk.py
```

### backend
```bash
docker-compose up
```
**NB:** для первого запуска надо запустить базовые миграции,
в будущем их можно запускать аналогично
`docker-compose exec web python manage.py migrate`.
Потом необходимо добавить суперпользователя
для получения доступа к админ панели
`docker-compose exec web python manage.py createsuperuser`.

Админ панель доступна тут: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Новые миграции добавляются и актуализируются командой
```bash
docker-compose exec web python manage.py makemigrations backend
```

Для запуска тестов использовать
```bash
docker-compose exec web python manage.py test
```
