<div align="center">

[简体中文](README_ZH.md) | [繁體中文](README_TC.md) | [English](README.md) | [한국어](README_KR.md) | [日本語](README_JP.md)


[![GitHub release](https://img.shields.io/static/v1?label=release&message=v1.0.0&color=blue)](https://www.github.com/novicezk/midjourney-proxy)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# Клиент Suno API неофициально

# Поздравляю с избранием проекта open source в уикли на этой неделе
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>


### Введение

- Это неофициальный клиент Suno API на основе Python и Streamlit, который в настоящее время поддерживает такие функции, как генерация музыки и получение информации о музыке. С функцией поддержки токенов и сохранения памяти, не беспокоясь об истечении срока действия токенов, можно настроить сохранение информации с нескольких учетных записей для использования.

- Иногда GitHub недоступен, если нет доступа, перейдите на Gitee адрес: https://gitee.com/SunoApi/SunoApi

### Особенности

- Автоматическое обслуживание и сохранение информации о номере счета
- Можно настроить несколько учетных записей для сохранения информации.
- Музыкальная ярмарка показывает все публичные песни.
- Введите музыкальный номер, чтобы получить информацию о песне напрямую.

### отладк

#### PythonЛокальная отладка

- Зависимость от установки

```bash
pip3 install -r requirements.txt
```

- Запустите проект, пожалуйста, обратитесь к документации Streamlit для Streamlit

```bash
streamlit run main.py
```

### Развертывание

#### Docker Локальное развертывание

```bash
docker run -d \
  --name sunoapi \
  --restart always \
  -p 8501:8501 \
  sunoapi/sunoapi:latest
```

#### Docker Локальное развертывание компиляции

```bash
docker compose build && docker compose up
```

#### Dockerfile

```docker
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8501
CMD [ "nohup", "streamlit", "run", "main.py" ]
```

#### Docker Развертывание зеркал

```bash
docker-compose pull && docker-compose up -d
```

#### docker-compose.yml

```docker
version: '3.1'

services:
  sunoapi:
    image: sunoapi/sunoapi:latest
    container_name: sunoapi
    ports:
      - "8501:8501"
    volumes:
      - ./sunoapi.db:/app/sunoapi.db
    restart: always
```

#### Streamlit Дистанционное развертывание склада

- сначала форк введёт код суноапи в ваш склад в гитубе
- выбер Github уполномоч залогин: https://share.streamlit.io/
- откр развертыван страниц: https://share.streamlit.io/deploy
- Repository выбирает: SunoApi/SunoApi
- ввод: мэйн
- Main file path введен: main py
- нажми деплой!

#### Zeabur Локальное развертывание

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/5BLAEZ)


### конфигурац

- Получите свои сеансы и файлы cookie из состояния входа на странице браузера.

![session](https://sunoapi.net/images/session.png)

- Заполните сообщение для установки, которое автоматически будет сохранено и может быть заполнено несколькими файлами.

![session1](https://sunoapi.net/images/session1.png)

- После заполнения сохраняется информация, введенная в identity, которая может изменить информацию о изменении аккаунта.

![session2](https://sunoapi.net/images/session2.png)

### Завершено

- Посещение браузера после запуска проекта http://localhost:8501/ Можно использовать.

![index](https://sunoapi.net/images/index.png)

![index1](https://sunoapi.net/images/index1.png)

![index2](https://sunoapi.net/images/index2.png)

![index3](https://sunoapi.net/images/index3.png)


### Вопросы

- Если сообщение подсказки страницы: пожалуйста, сначала установите сохранность информации, а затем обновите страницу, чтобы она могла нормально использоваться!  Пожалуйста, сначала добавьте информацию о своем аккаунте в базу данных sunoapi db, затем удалите другие недействительные данные о аккаунтах, включая информацию о аккаунтах, которые я тестирую, прежде чем их можно будет использовать.
- Если сообщение подсказки страницы: Suno AI Music Generation не удалось отправить: Insufficient credits указывает на то, что информация учетной записи не имеет достаточного количества баллов для credits, сначала добавьте сохраненную информацию учетной записи, прежде чем она будет доступна для нормального использования.
- после того, как музыкальная миссия была успешно выполнена, удаление статуса генерируемой задачи было успешно возвращено, когда состояние было "complete", которое оставалось по умолчанию в течение 15 секунд в ожидании официального документа.  Официальная interface service вернулась непосредственно к адресу Url media файла, который в большинстве случаев был нормально отображен на странице.  Иногда интерфейс возвращал адрес Url media-файла, но настоящий файл не может быть доступен с Url-адреса, чтобы немного подождать.  В этот момент медиафайл может не быть загружен на страницу, и он может скопировать адрес медиа-файла с помощью правого ключа медиа-плеера мыши, который использует браузер, чтобы открыть этот адрес, или же он может быть доступен с помощью браузера или непосредственно с правого клавиша для хранения.
- о сохранении информации о размещении аккаунтов session и cookie не стоит беспокоиться до тех пор, пока ваш аккаунт не будет переполнен, потому что не зная пароль вашего аккаунта, информацию о session и cookie, которую вы заполнили, до тех пор, пока ваш аккаунт регистрируется где-то еще или выходит из официального сайта, Тогда заполненные session и cookie будут недействительными, и в следующий раз будут внесены изменения в официальную сеть session и cookie.


### Творчество

- Инструменты поддержки профессиональных текстов:https://poe.com/SuperSunoMaster


### Обмен информацией

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<img src="https://sunoapi.net/images/wechat.jpg" width="382px" height="511px" />


### Участие

- Индивидуальные силы всегда ограничены, и любые вклады приветствуются, включая, но не ограничиваются кодами вкладов, оптимизированными документами, представленными Issue и PR, поскольку время ограниченное для того, чтобы не принимать микроверы или микроблоки для создания багов, вопросы или рекомендации оптимизации должны быть представлены Issue и PR!

[![Star History Chart](https://api.star-history.com/svg?repos=SunoApi/SunoApi&type=Timeline)](https://star-history.com/#SunoApi/SunoApi&Timeline)


### Ссылки

- Suno AI 官网: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### Заявления

SunoApi - это неофициальный проект с открытым исходным кодом, предназначенный только для обучения и исследований. Пользователи добровольно вводят бесплатную информацию о своей учетной записи для создания музыки. Каждый аккаунт может бесплатно генерировать пять песен в день, и мы не используем их для других целей. Будьте уверены в использовании! При 10 000 пользователей система может генерировать 50 000 песен в день бесплатно. Старайтесь максимально экономить, так как каждый аккаунт может генерировать только пять песен в день бесплатно. Если каждый человек создает более пяти песен в день, этого все равно недостаточно. Конечная цель состоит в том, чтобы обеспечить бесплатную генерацию в любое время, когда это необходимо.
