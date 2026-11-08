## Содержание

1. [Как это работает](#как-это-работает)
2. [Установка](#установка)
3. [Настройка](#настройка)
4. [Endpoints](#endpoints)
   - [Пользователи](#пользователи)
     - [Получить список пользователей](#получить-список-пользователей)
     - [Регистрация](#регистрация)
     - [Вход](#вход)
     - [Изменение имени и фамилии](#изменение-имени-и-фамилии)
     - [Изменение дополнительной информации](#изменение-дополнительной-информации)
     - [Изменение пароля](#изменение-пароля)
     - [Изменение аватарки](#изменение-аватарки)
   - [Объявления](#объявления)
5. [Примеры интеграции](#примеры-интеграции)

## Как это работает

```text
Сайт ──────────────────┐
                       ├── HTTP ──> LostNFound API ──> База данных
Мобильное приложение ──┘
```

- Клиенты отправляют HTTP-запросы к API.
- Для регистрации, входа и изменения текстовых данных используется JSON.
- Для загрузки аватарки используется `multipart/form-data`.
- Клиентам не нужно подключаться к базе данных напрямую.

## Установка

Клонируй репозиторий:

```bash
git clone https://github.com/17partDissections/LostNFound-api
cd LostNFound-api
```

Создай venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установи зависимости:

```bash
pip install -r dependencies.txt
```

## Настройка

### База данных

Проверь параметры подключения перед запуском. Не используй учётную запись `root` и пустой пароль.

Таблица `users` должна содержать следующие поля:

| Поле | Назначение | Тип |
|---|---|---|
| `id` | ID пользователя | `INT` |
| `name` | Имя | `TEXT` |
| `surname` | Фамилия | `TEXT` |
| `phone_num` | Номер телефона для входа | `TEXT` |
| `passwd` | Пароль | `TEXT` |
| `additional_contact` | Дополнительная контактная информация | `TEXT` |
| `avatar` | Путь к аватарке | `TEXT` |

Типы столбцов, первичный ключ и ограничения должны соответствовать схеме проекта. Приложение не создаёт таблицу автоматически.

### Дефолтная аватарка

В `users.py` задан путь `uploads/avatars/default.png`. При регистрации этот путь записывается в `avatar`. Сам файл должен существовать относительно рабочей директории приложения.<br>
upd: директория uploads/avatars вместе с нашей версией аватарки добавлена в репозиторий.

### Запуск

`main.py` создаёт FastAPI в объекте `api` и подключает роутеры пользователей и объявлений. Если установлен Uvicorn, запускать вот так:

```bash
uvicorn main:api --reload
```

Интерактивная документация обычно доступна по `/docs`, альтернативная — по `/redoc`.

## Endpoints

В примерах `https://api.1566lostnfound.ru` — базовый адрес API. Замени его адресом своего сервера..

### Пользователи

#### Получить список пользователей

`GET /users`

Возвращает список пользователей с полями `id`, `name`, `surname`, `phone_num`, `additional_contact` и `avatar`. Поле `passwd` в ответ не включается.

```bash
curl https://api.1566lostnfound.ru/users
```

Пример ответа:

```json
[
  {
    "id": 16,
    "name": "Алексей",
    "surname": "Карнавальный",
    "phone_num": "88005553535",
    "additional_contact": "тг @karnavalny",
    "avatar": "uploads/avatars/16.png"
  }
]
```

#### Регистрация

`POST /users`

Тело запроса — JSON:

| Поле | Тип |
|---|---|
| `name` | string |
| `surname` | string |
| `phone_num` | string |
| `passwd` | string |

`additional_contact` не принимается при регистрации: сервер устанавливает пустую строку. Для `avatar` используется путь к дефолтной аватарке.

```bash
curl -X POST https://api.1566lostnfound.ru/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Андрей","surname":"Смирнов","phone_num":"79260006767","passwd":"2lazy4dissht"}'
```

Пример ответа:

```json
{
  "status": "add: success",
  "message": "17 (Андрей) added to db"
}
```

#### Вход

`POST /login`

Тело запроса — JSON:

| Поле | Тип |
|---|---|
| `phone_num` | string |
| `passwd` | string |

```bash
curl -X POST https://api.1566lostnfound.ru/login \
  -H "Content-Type: application/json" \
  -d '{"phone_num":"76669991489","passwd":"Qwerty"}'
```

Успешный ответ:

```json
{
  "status": "login: success"
}
```

Если пользователь не найден:

```json
{
  "status": "login: error",
  "message": "bitch theres no user w that phone_num"
}
```

Если пароль неверный:

```json
{
  "status": "login: error",
  "message": "YO MAMA SOOO FAT"
}
```

Вы что, правда думали, что я прикалывался и изменю эти результатные сообщения? Пфф нет.

#### Изменение имени и фамилии

`PUT /users/{user_id}`

Тело запроса — JSON:

```json
{
  "name": "Котик",
  "surname": "Штефанов"
}
```

```bash
curl -X PUT https://api.1566lostnfound.ru/users/17 \
  -H "Content-Type: application/json" \
  -d '{"name":"Котик","surname":"Штефанов"}'
```

Ответ:

```json
{
  "status": "edit_name: success",
  "message": "User 21 changed their name to Котик"
}
```

#### Изменение дополнительной информации

`PUT /users/{user_id}/additional-info`

Тело запроса — JSON:

```json
{
  "additional_contact": "тг @q17pd"
}
```

```bash
curl -X PUT https://api.1566lostnfound.ru/users/17/additional-info \
  -H "Content-Type: application/json" \
  -d '{"additional_contact":"тг @q17pd"}'
```

Ответ:

```json
{
  "status": "edit_additional_info: success",
  "message": "User 17 changed their additional info"
}
```

(Чтобы очистить поле, передай `{"additional_contact": ""}`)

#### Изменение пароля

`PUT /users/{user_id}/password`

Тело запроса — JSON:

| Поле | Тип |
|---|---|
| `current_passwd` | string |
| `new_passwd` | string |

```bash
curl -X PUT https://api.1566lostnfound.ru/users/17/password \
  -H "Content-Type: application/json" \
  -d '{"current_passwd":"старый пароль","new_passwd":"новый пароль"}'
```

Успешный ответ:

```json
{
  "status": "edit_password: success",
  "message": "User 17 changed their password"
}
```

Если пользователь не найден:

```json
{
  "status": "edit_password: error",
  "message": "User 17 not found"
}
```

Если текущий пароль неверный:

```json
{
  "status": "edit_password: error",
  "message": "Current password is incorrect"
}
```

#### Изменение аватарки

`PUT /users/{user_id}/avatar`

Принимает файл `image` через `multipart/form-data`, а не JSON. Файл сохраняется в `uploads/avatars/`, а путь записывается в `users.avatar`.

```bash
curl -X PUT https://api.1566lostnfound.ru/users/17/avatar \
  -F "image=@./avatar.png"
```

Успешный ответ:

```json
{
  "status": "edit_avatar: success",
  "message": "User 21 changed their avatar"
}
```

Если пользователь не найден:

```json
{
  "status": "edit_avatar: error",
  "message": "User 21 not found"
}
```

Расширение берётся из имени файла: например, `avatar.png` сохраняется как `uploads/avatars/17.png`. Код не проверяет фактический формат и размер файла. Это должно осуществляться на стороне клиента.

### Объявления

ыыыыыыыыыыыыыы хз еще не делал

## Примеры интеграции

В примерах ниже замени `https://api.1566lostnfound.ru` на адрес своего
API. Для запросов используется `userId` - ID пользователя.

**Важно про аватарки:** API возвращает в поле `avatar` путь к
изображению, например `uploads/avatars/12.png`. Каталог `uploads`
раздаётся через HTTP, поэтому изображение доступно по адресу
`https://api.1566lostnfound.ru/uploads/avatars/12.png`. Для отображения
аватарки используй этот URL.

### JavaScript (сайт)

#### Получение имени и аватарки

`GET /users` возвращает массив пользователей. В примере находим нужного
пользователя по `id` и читаем `name`, `surname` и `avatar`.

``` javascript
const API_BASE = "https://api.1566lostnfound.ru";
const userId = 12;

async function loadUserProfile() {
  const response = await fetch(`${API_BASE}/users`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);

  const users = await response.json();
  const user = users.find(item => item.id === userId);
  if (!user) throw new Error("Пользователь не найден");

  document.querySelector("#user-name").textContent =
    `${user.name} ${user.surname}`;

  const avatarPath = user.avatar;
  if (avatarPath) {
    const avatarUrl = avatarPath.startsWith("/")
      ? `${API_BASE}${avatarPath}`
      : `${API_BASE}/${avatarPath}`;

    document.querySelector("#user-avatar").src = avatarUrl;
  }
}

loadUserProfile().catch(console.error);
```

Пример HTML для имени и изображения:

``` html
<span id="user-name"></span>
<img id="user-avatar">
```

#### Изменение имени и фамилии

``` javascript
async function updateUserName(userId, name, surname) {
  const response = await fetch(`${API_BASE}/users/${userId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, surname })
  });

  const result = await response.json();
  if (!response.ok) throw new Error(JSON.stringify(result));
  return result;
}

updateUserName(17, "Алексей", "Чекмарев")
  .then(console.log)
  .catch(console.error);
```

#### Загрузка новой аватарки

``` javascript
document.querySelector("#upload-avatar").addEventListener("click", async () => {
  const file = document.querySelector("#avatar-file").files[0];
  if (!file) {
    alert("Сначала выбери изображение");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  const response = await fetch(`${API_BASE}/users/12/avatar`, {
    method: "PUT",
    body: formData
  });

  const result = await response.json();
  if (!response.ok) throw new Error(JSON.stringify(result));
  console.log(result);
});
```

Не указывай `Content-Type` вручную при отправке `FormData`: браузер сам
добавит необходимый `boundary`.

### Java (преимущественно для Android Studio)

Примеры используют `HttpURLConnection` и `org.json`, доступные в Android
SDK. Выполняй сетевые запросы не в главном UI-потоке (например, через
`ExecutorService` или корутины через Kotlin-обёртку). В
`AndroidManifest.xml` добавь разрешение:

``` xml
<uses-permission android:name="android.permission.INTERNET" />
```

Добавь константы в свой класс:

``` java
private static final String API_BASE = "https://api.1566lostnfound.ru";
private static final int USER_ID = 12;
```

#### Получение имени и аватарки

``` java
private JSONObject loadUserProfile(int userId) throws Exception {
    URL url = new URL(API_BASE + "/users");
    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
    connection.setRequestMethod("GET");
    connection.setConnectTimeout(10000);
    connection.setReadTimeout(10000);

    try {
        int code = connection.getResponseCode();
        InputStream stream = code < 400
                ? connection.getInputStream()
                : connection.getErrorStream();

        ByteArrayOutputStream output = new ByteArrayOutputStream();
        byte[] buffer = new byte[4096];
        int count;
        while ((count = stream.read(buffer)) != -1) {
            output.write(buffer, 0, count);
        }
        stream.close();

        if (code >= 400) throw new IOException("HTTP " + code);

        JSONArray users = new JSONArray(output.toString("UTF-8"));
        for (int i = 0; i < users.length(); i++) {
            JSONObject user = users.getJSONObject(i);
            if (user.getInt("id") == userId) {
                return user;
            }
        }
        throw new IOException("Пользователь не найден");
    } finally {
        connection.disconnect();
    }
}
```

Пример вызова (выполняй в фоновом потоке):

``` java
JSONObject user = loadUserProfile(USER_ID);

String name = user.optString("name", "") + " "
        + user.optString("surname", "");

String avatarPath = user.optString("avatar", "");
String avatarUrl = avatarPath.startsWith("/")
        ? API_BASE + avatarPath
        : API_BASE + "/" + avatarPath;

// Передай name в TextView через runOnUiThread().
// Загрузи avatarUrl в ImageView, например, с помощью Glide или Coil.
```

Не обращайся к `TextView` напрямую из фонового потока: обновляй
интерфейс через `runOnUiThread()`. Для отображения изображения используй
библиотеку вроде Glide или Coil либо загружай файл самостоятельно.

#### Изменение имени и фамилии

``` java
private JSONObject updateUserName(int userId, String name, String surname) throws Exception {
    URL url = new URL(API_BASE + "/users/" + userId);
    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
    connection.setRequestMethod("PUT");
    connection.setConnectTimeout(10000);
    connection.setReadTimeout(10000);
    connection.setDoOutput(true);
    connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");

    JSONObject body = new JSONObject();
    body.put("name", name);
    body.put("surname", surname);

    try {
        try (OutputStream os = connection.getOutputStream()) {
            os.write(body.toString().getBytes(StandardCharsets.UTF_8));
        }

        int code = connection.getResponseCode();
        InputStream stream = code < 400
                ? connection.getInputStream()
                : connection.getErrorStream();

        ByteArrayOutputStream output = new ByteArrayOutputStream();
        byte[] buffer = new byte[4096];
        int count;
        while ((count = stream.read(buffer)) != -1) {
            output.write(buffer, 0, count);
        }
        stream.close();

        if (code >= 400) {
            throw new IOException("HTTP " + code + ": " + output.toString("UTF-8"));
        }
        return new JSONObject(output.toString("UTF-8"));
    } finally {
        connection.disconnect();
    }
}
```

#### Загрузка аватарки

Метод ниже принимает `File` с уже доступным локальным изображением. Если
изображение выбрано через Android Photo Picker, скопируй содержимое
выбранного `Uri` во временный файл через `ContentResolver` и передай
этот файл методу. Запрос отправляет multipart-поле с именем `image`, как
ожидает API.

``` java
private JSONObject uploadAvatar(int userId, File imageFile) throws Exception {
    String boundary = "----LostNFoundBoundary" + System.currentTimeMillis();
    URL url = new URL(API_BASE + "/users/" + userId + "/avatar");
    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
    connection.setRequestMethod("PUT");
    connection.setConnectTimeout(15000);
    connection.setReadTimeout(15000);
    connection.setDoOutput(true);
    connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);

    try {
        try (OutputStream os = connection.getOutputStream();
             FileInputStream fileInput = new FileInputStream(imageFile)) {
            String header = "--" + boundary + "\r\n"
                    + "Content-Disposition: form-data; name=\"image\"; filename=\""
                    + imageFile.getName() + "\"\r\n"
                    + "Content-Type: application/octet-stream\r\n\r\n";
            os.write(header.getBytes(StandardCharsets.UTF_8));

            byte[] buffer = new byte[8192];
            int count;
            while ((count = fileInput.read(buffer)) != -1) {
                os.write(buffer, 0, count);
            }
            os.write(("\r\n--" + boundary + "--\r\n").getBytes(StandardCharsets.UTF_8));
        }

        int code = connection.getResponseCode();
        InputStream stream = code < 400
                ? connection.getInputStream()
                : connection.getErrorStream();

        ByteArrayOutputStream output = new ByteArrayOutputStream();
        byte[] buffer = new byte[4096];
        int count;
        while ((count = stream.read(buffer)) != -1) {
            output.write(buffer, 0, count);
        }
        stream.close();

        if (code >= 400) {
            throw new IOException("HTTP " + code + ": " + output.toString("UTF-8"));
        }
        return new JSONObject(output.toString("UTF-8"));
    } finally {
        connection.disconnect();
    }
}
```

В Java-примерах нужны импорты `org.json.JSONArray`,
`org.json.JSONObject`, `java.io.*`, `java.net.HttpURLConnection`,
`java.net.URL` и `java.nio.charset.StandardCharsets`. Вызывай
`loadUserProfile`, `updateUserName` и `uploadAvatar` в фоновом потоке.

