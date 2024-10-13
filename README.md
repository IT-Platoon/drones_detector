# PC Part Detector

### Требования

Необходимо, чтобы были установлены следующие компоненты:

- `Docker` и `docker-compose`

### Модели

Класс-обертка находится по пути: ```server/app/services/model/model.py```
Модель для предсказания ```server/app/services/model/weights/best.pt```

### Запуск

Запуск приложения:
```commandline
make docker-up
```

### Статический анализ

- Запуск линтеров:
```commandline
make lint
```

- Запуск форматирования кода:
```commandline
make format
```

### Дополнительные команды

- Создание новой ревизии:
```commandline
make revision
```

- Открытие базы данных внутри Docker-контейнера:
```commandline
make open-db
```

- Открытие контейнера внутри Docker-контейнера:
```commandline
make open-server
```

- Вывести список всех команд и их описание:
```commandline
make help
```
