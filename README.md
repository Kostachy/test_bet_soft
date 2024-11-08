### Инструкция

1. git clone `https://github.com/Kostachy/test_bet_soft`
2. cd test_bet_soft
3. .env уже сконфигурирован
4. Запустить докер через `make up`
5. Прогнать миграции через `make migrate`
6. Для просмотра логов `docker compose logs ``имя_контейнера`` -f`
7. Для остановки и удаления контейнеров `make down`

Сервисы должны быть доступны по ссылкам:

`http://0.0.0.0:8100/docs` либо `http://127.0.0.1:8100/docs` - LineProviderApi

`http://0.0.0.0:8080/docs` либо `http://127.0.0.1:8080/docs` - BetMakerApi

`http://127.0.0.1:15672/` - админ панель RabbitMQ (login: admin, password: admin)
`http://127.0.0.1:8000/` - pg_admin (login: user@domain.com, password: SuperSecret)

### Обзор выбранных технологий и инструментов.

Стeк: Python 3.10, SQLAlchemy, alembic, asyncpg, RabbitMQ, aio-pika, FastStream, PostgreSQL

### Архитектурное описание решения

Реализована Чистая архитектура с элементами тактических паттернов из DDD.
Получение списка событий, на который можно совершать ставки реализован синхронным способ по http.
Получение обновления на события реализованна асинхронно через брокер RabbitMQ. Сервис line-provider
посылает события в момент обновления статусов событий(выступает в роли продьюсера). Сервис bet-maker подписывается
и прослушивает очередь, обрабатывает обновленные события по мере поступления(выступает в роли консьюмера).
В сервисе line-provider отправка событий реализована через компоненты MessageBroker и EventSender.
В сервисе bet-maker обработкой сообщений занимается фреймворк (FastStream).

### Описание основных классов и функций, их назначения и взаимодействия.

Domain layer:

- Сущность Bet представляет собой корневую сущности(анемичную плоскую модель).
- Объекты-значения BetSum задают правила и ограничения для экземпляров Bet.

Application layer:

- в пакете commonn содержаться интерфейсы для слоя юзкейсов
- в пакете usecases содержаться компоненты реализующие прикладную бизнес логику, на вход принимают интерфейсы,
  что позволяет не привязываться к деталям реализации.

Infrastructure layer:

- Содержит слоя доступа к данным, реализует интерфейсы, так же сразу маппит из моделей алхимии
  в Сущности из Domain layer.

Presentation layer:

- Представляет собой слой представления. Этот слой может быть чем угодно (API, тг бот, т.д.)
