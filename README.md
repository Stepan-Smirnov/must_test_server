<!-- Верхняя часть с оформлением -->
<div align="center">

# 📊 **test_mast_server**

</div>

---

## 🔧 Установка

### 1. Клонирование репозитория

```bash
   git clone https://github.com/Stepan-Smirnov/must_test_server.git
```

### 2. Подготовка окружения
* Установить библиотеки
```bash
   uv sync
```
* Заполнить .env
```
DATABASE_URL= # основная БД: sqlite | postgresql
TEST_DATABASE_URL = # БД для тестов: sqlite | postgresql
```
### 3. Команды проекта
* Запуск проекта
```bash
   uv run fastapi dev
```

* Запуск тестов
```bash
   uv run pytest
```

### 4. Дистрибутив приложения

* Дистрибутив находится по следующему пути

```
must_test_server\dist\must_test_server\must_test_server.exe
```
