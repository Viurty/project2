Веб-сервис запускается в файле app.py.

ОТРАБОТКА ОШИБОК:

Во время проверки было замечено несклько ошибок. Во-первых, пользователь может отправить форму с >5 дней, так как это бесплатная версия API, то 5 дней это максимум. По этому вылезает ошибка и рекомендация поменять кол-во дней. Во-вторых, доступ к некоторым городам есть только если введены английские названия, поэтому вылезает ошибка, рекомендующая попробовать другое название. Так же существует шанс, что закончлись токены у API, эта ошибка тоже обрабатывается(считывается когда статус запроса равен 503).