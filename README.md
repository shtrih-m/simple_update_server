### Пример простого сервера обновлений:
Поддерживает:
1. Статическую раздачу файлов из директории
2. POST запрос  check_firmware
3. Запрос версии сервера и окружения
в теле запроса check_firmware необходимо передать JSON вида:

```json
{"build_date": "28.12.2017"}
```
**build_date** - дата сборки, получить можно из запроса состояния ФР
в ответ приходит JSON вида:

```json
{
    "update_available": true,
    "critical": true,
    "version": 20180116,
    "description": "version before 20180116 may die anytime",
    "url": "http://127.0.0.1:8888/firmware/20180116/upd_app.bin",
    "url_old_frs": "http://127.0.0.1:8888/firmware/20180116/upd_app_for_old_frs.bin",
}
```
**update_available** - наличие обновления
**critical** - критическое обновление?
**version** - версия прошивки обновления
**description** - описание обновления
**url** - ссылка на прошивку
**url_old_frs** - ссылка на прошивку без ключей
#### Установка сервера:
1. Необходимо наличие python версии 3.4+ https://www.python.org/downloads/
2. Библиотека Tornado Web Server https://pypi.python.org/pypi/tornado
3. Редактируем файл config.py в котором указать:  
**PORT**  — TCP порт на котором будет работать сервер  
**CURRENT_FIRMWARE** — словарь со следующими ключами:  
	version — версия прошивки на сервере обновления в формате yyyymmdd  
	description — текстовое описание обновления  
**CRITICAL_VERSION** — версия последнего критического обновления в формате yyyymmdd  
**FIRMWARE_PATH** — абсолютный или относительный путь к директории из которой сервер будет статически раздавать файлы.  
Внутри пути **FIRMWARE_PATH** необходимо организовать поддиректории с именами в формате yyyymmdd, в которых и будут находиться сами файлы прошивок.  
 Пример:

    ```bash
    │firmware/
    ├── 20171220 
    │   ├── upd_app.bin 
    │   └── upd_app_for_old_frs.bin 
    ├── 20180117 
    │   ├── upd_app.bin 
    │   └── upd_app_for_old_frs.bin 
    └── 20180125 
       ├── upd_app.bin 
       └── upd_app_for_old_frs.bin
    ```
#### Запуск
```bash
python server.py
```