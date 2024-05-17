<div align="center">

[简体中文](https://github.com/SunoApi/SunoApi/blob/main/README_ZH.md) | [繁體中文](https://github.com/SunoApi/SunoApi/blob/main/README_TC.md) | [Русский](https://github.com/SunoApi/SunoApi/blob/main/README_RU.md) | [English](https://github.com/SunoApi/SunoApi/blob/main/README.md) | [한국어](https://github.com/SunoApi/SunoApi/blob/main/README_KR.md) | [日本語](https://github.com/SunoApi/SunoApi/blob/main/README_JP.md) | [Français](https://github.com/SunoApi/SunoApi/blob/main/README_FR.md) 


[![GitHub release](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=black)](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=blue)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# SunoAPI inoffizieller Suno AI Client

# Herzlichen Glückwunsch zu diesem Open-Source-Projekt, das für diese Woche ausgewählt wurde
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>



### Einführung

- Dies ist ein inoffizieller SunoAPI Client basierend auf Python und Streamlit, der derzeit Funktionen wie das Erzeugen von Musik und das Abrufen von Musikinformationen unterstützt. Es verfügt über integrierte Wartungs- und Aktivierungsfunktionen für Token, so dass Sie sich keine Sorgen über das Ablaufen von Token machen müssen. Sie können mehrere Kontoinformationen einrichten, die für die Verwendung gespeichert werden.

- Manchmal kann nicht auf GitHub zugegriffen werden. Wenn der Zugriff nicht möglich ist, wechseln Sie bitte zur Gitee-Adresse: https://gitee.com/SunoApi/SunoApi

### Charakteristik

- Kontoinformationen ausfüllen und das Programm automatisch pflegen und aktiv halten
- Mehrere Kontoinformationen können gespeichert und verwendet werden
- Music Sharing Square zeigt alle öffentlich zugänglichen Songs
- Geben Sie die Musiknummer ein, um direkt Songinformationen zu erhalten
- Unterstützung beim Hochladen von Bildern und Generieren von Songs basierend auf dem Inhalt, der von den Bildern analysiert wird
- Unterstützen Sie mehrere Sprachen wie Chinesisch, Englisch, Koreanisch, Japanisch usw

### Debugging

#### Lokale Python-Debugging-Ausführung

- Quellcode klonen

```bash
git clone https://github.com/SunoApi/SunoApi.git
```


- Installation sabhängigkeiten

```bash
cd SunoApi
pip3 install -r requirements.txt
```

- .env Umgebungsvariablen-Datei erfordert die Verwendung des gpt-4-vision-preview Modells für die Bilderkennung. Die OpenAI Schnittstelle kann verwendet werden, oder andere häufig verwendete Schnittstellen können verwendet werden, um sie zu ersetzen. Registrieren Sie ein console.bitiful.com Objektspeicherkonto, um den S3_ACCESSKEY_ID，S3_SECRETKEY_ID Parameter zu erhalten, der zum Hochladen von Bildern in den von Ihnen erstellten Speicher-Bucket verwendet wird. Geben Sie den Domänennamen für den externen Zugriff Ihres Objektspeicherkontos ein, nachdem Sie den Speicher-Bucket in S3_WEB_SITE_URL erstellt haben. Auf diese Weise kann die lokale Umgebung die Bilderkennung testen.

```bash
OPENAI_BASE_URL = https://chatplusapi.cn
OPENAI_API_KEY = sk-xxxxxxxxxxxxxxxxxxxx
S3_WEB_SITE_URL = https://sunoapi.s3.bitiful.net
S3_ACCESSKEY_ID = xxxxxxxxxxxxxxxxxxxx
S3_SECRETKEY_ID = xxxxxxxxxxxxxxxxxxxx
```


- Starten Sie das Projekt, lesen Sie bitte die Streamlit Dokumentation für Details zu Streamlit

```bash
streamlit run main.py --server.maxUploadSize=2
```


### Bereitstellung

#### Docker Lokale Bereitstellung ein Klick Bereitstellung

```bash
docker run -d \
  --name sunoapi \
  --restart always \
  -p 8501:8501 \
  -v ./sunoapi.db:/app/sunoapi.db \
  -v ./images/upload:/app/images/upload \
  -e OPENAI_BASE_URL=https://api.openai.com  \
  -e OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx \
  -e S3_WEB_SITE_URL=https://sunoapi.s3.bitiful.net  \
  -e S3_ACCESSKEY_ID=xxxxxxxxxxxxxxxxxxxx  \
  -e S3_SECRETKEY_ID=xxxxxxxxxxxxxxxxxxxx  \
  sunoapi/sunoapi:latest
```

##### Vorsicht: Es ist notwendig, https://sunoapi.s3.bitiful.net Ersetzen Sie die aktuelle Adresse, auf die Sie zugreifen können, und die endgültige hochgeladene Bilddatei wird durch http://xxxxxx.s3.bitiful.net/images/upload/xxxxxx.jpg Das Format kann aufgerufen werden, andernfalls kann OpenAI nicht auf das hochgeladene Bild zugreifen und seinen Inhalt nicht erkennen. Daher wird die Funktion des Hochladens von Bildern zur Erzeugung von Musik nicht verfügbar sein.


#### Docker Lokale Kompilierung ein Klick Bereitstellung

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
CMD [ "nohup", "streamlit", "run", "main.py", "--server.maxUploadSize=2" ]
```

#### Docker Image-Bereitstellung abrufen

```bash
docker-compose pull && docker-compose up -d
```

#### docker-compose.yml

```docker
version: '3.2'

services:
  sunoapi:
    image: sunoapi/sunoapi:latest
    container_name: sunoapi
    ports:
      - "8501:8501"
    volumes:
      - ./sunoapi.db:/app/sunoapi.db
      - ./images/upload:/app/images/upload
    environment:
      - TZ=Asia/Shanghai
      - OPENAI_BASE_URL=https://api.openai.com
      - OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
      - S3_WEB_SITE_URL=https://sunoapi.s3.bitiful.net
      - S3_ACCESSKEY_ID=xxxxxxxxxxxxxxxxxxxx
      - S3_SECRETKEY_ID=xxxxxxxxxxxxxxxxxxxx
    restart: always
```

##### Vorsicht: Um die Image-Bereitstellung abzurufen, müssen Sie sunoapi.db aus dem Projekt herunterladen und in Ihr docker-compose.yml-Dateiverzeichnis übertragen. Andernfalls wird beim Docker-Start angezeigt, dass die Datei nicht eingehängt werden kann.


#### Streamlit Remote Warehouse Deployment

- Zuerst eine Kopie des SunoApi-Codes in Ihr Github-Repository forken
- Github Autorisierungs-Login auswählen: https://share.streamlit.io/
- Öffnen Sie die Bereitstellungsseite: https://share.streamlit.io/deploy
- Auswahl des Repositories: SunoApi/SunoApi Branch Input: main
- Main Datei Pfad Eingabe: main.py
- Klicken Sie auf Bereitstellen!

#### Zeabur Ein Klick Bereitstellung

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/ORTEGG)


### Zuteilung

- Rufen Sie zunächst Ihre Sitzung und Ihren Cookie von der Browserseite ab, wenn Sie eingeloggt sind.

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session.png" style="max-width: 100%;"/></a>

- Nach dem Ausfüllen der Einstellungsinformationen werden diese automatisch gespeichert und mehrere Kontoinformationen können ausgefüllt werden.

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session1.png" style="max-width: 100%;"/></a>

- Nach dem Ausfüllen speichern Sie die Informationen und geben Sie die Identität ein, um die Kontoinformationen zu ändern.

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session2.png" style="max-width: 100%;"/></a>

### Komplett

- Browserzugriff nach Start und Ausführung des Projekts http://localhost:8501/ Du kannst es jetzt benutzen.

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index1.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index2.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index3.png" style="max-width: 100%;"/></a>


### Frage

- Wenn die Seite die Meldung auffordert: Bitte speichern Sie zuerst die Informationen und aktualisieren Sie dann die Seite, um sie normal zu verwenden! Bitte fügen Sie zuerst Ihre eigenen Kontoinformationen hinzu und speichern Sie sie, löschen Sie dann andere ungültige Kontoinformationen in der sunoapi.db Datenbank, einschließlich der von mir getesteten Kontoinformationen, und dann können Sie sie normal verwenden.
- Wenn die Seite die Meldung auffordert: Suno AI Musiksonggenerierung fehlgeschlagen: Unautorisiert. Dies zeigt an, dass der Anmeldestatus für das Konto nicht autorisiert ist. Diese Situation wird normalerweise dadurch verursacht, dass sich mehrere Browser-Clients beim Konto anmelden und eine Preemption bilden. Verlassen Sie andere angemeldete Browser-Clients, halten Sie das Konto auf diesem SunoAPI AI Musiksonggenerator-Client angemeldet und melden Sie sich nicht auf anderen Browser-Clients an.
- Wenn die Seite die Meldung auffordert: Suno AI Music Song Generation Submission failed: Insufficient credits. Dies zeigt an, dass die Kontoinformationen Credits nicht genügend Punkte haben. Bitte fügen Sie zuerst Ihre eigenen Kontoinformationen hinzu, um sie zu speichern, und dann können Sie sie normal verwenden.
- Nachdem die Musikgenerierungsaufgabe erfolgreich übermittelt wurde, wird der Warteschlangenstatus des Erzeugungsaufgangs abgerufen. Wenn der Status "abgeschlossen" ist, wird er erfolgreich zurückgegeben. Zu diesem Zeitpunkt wird standardmäßig 15 Sekunden lang auf die offizielle Erzeugungsdatei gewartet. Der offizielle Schnittstellendienst gibt direkt die URL-Adresse von Mediendateien zurück, und die meiste Zeit kann die Seite diese Mediendateien normal anzeigen. Gelegentlich hat die Schnittstelle möglicherweise die Url-Adresse der Mediendatei zurückgegeben, aber die eigentliche Datei kann nicht von der Url-Adresse aus aufgerufen werden und muss eine Weile warten. Zu diesem Zeitpunkt kann die Mediendatei möglicherweise nicht auf der Seite geladen werden. Sie können mit der rechten Maustaste auf den Medienplayer klicken und die Mediendateinadresse kopieren. Öffnen Sie die Adresse separat im Browser, um darauf zuzugreifen, oder klicken Sie mit der rechten Maustaste, um sie als Download zu speichern und zu speichern.
- In Bezug auf das Sicherheitsproblem der Speicherung von Kontositzungs- und Cookie-Informationen: Solange Ihr Konto nicht aufgeladen ist, brauchen Sie sich keine Sorgen zu machen, da Sie Ihr Konto-Passwort nicht kennen. Die Sitzungs- und Cookie-Informationen, die Sie eingeben, werden ungültig, wenn Ihr Konto sich bei anderen Aktivitäten anmeldet oder sich von der offiziellen Website abmeldet. Die Sitzungs- und Cookie-Informationen, die Sie eingeben, ändern sich, wenn Sie sich das nächste Mal auf der offiziellen Website anmelden.


### Schaffung

- Professionelles Hilfsmittel für Texte：https://poe.com/SuperSunoMaster


### Kommunizieren

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/wechat.jpg?20240517" style="max-width: 100%;"/></a>


### Teilnahme an

- Meine persönliche Stärke ist immer begrenzt, und jede Form des Beitrags ist willkommen, einschließlich, aber nicht beschränkt auf das Beitragen von Code, die Optimierung von Dokumenten, das Einreichen von Problemen und PRs. Aufgrund von Zeitbeschränkungen akzeptiere ich keine Bugs an Entwickler in WeChat oder WeChat Gruppen. Wenn Sie Fragen oder Optimierungsvorschläge haben, senden Sie bitte Probleme und PRs!

<a href="https://star-history.com/#SunoApi/SunoApi" target="_blank"><img src="https://api.star-history.com/svg?repos=SunoApi/SunoApi" style="max-width: 100%;"/></a>


### Referenz

- Suno AI Offizielle Website: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### Anweisung

- SunoAPI ist ein inoffizielles Open-Source-Projekt nur für Lern- und Forschungszwecke. Benutzer geben freiwillig kostenlose Kontoinformationen ein, um Musik zu erzeugen. Jeder Account kann jeden Tag fünf Songs kostenlos generieren und wir werden sie nicht für andere Zwecke verwenden. Bitte seien Sie versichert zu verwenden! Wenn es 10000Benutzer gibt, kann das System 50000 Songs kostenlos jeden Tag generieren. Bitte versuchen Sie, die Nutzung zu sparen, da jedes Konto nur fünf Songs pro Tag kostenlos generieren kann. Wenn jeder jeden Tag fünf oder mehr Songs erstellt, reicht das immer noch nicht aus. Das ultimative Ziel ist es, bei Bedarf jederzeit freie Erzeugung zu ermöglichen.


### Buy me a Coffee

<a href="https://www.buymeacoffee.com/SunoApi" target="_blank"><img src="https://sunoapi.net/images/donate.jpg" alt="Buy me a Coffee" style="max-width: 100%;"></a>


##### Dieses Projekt ist Open-Source auf GitHub, basiert auf dem MIT-Protokoll und kostenlos, ohne jegliche Form von Zahlungsverhalten! Wenn du denkst, dass dieses Projekt hilfreich für dich ist, bitte hilf mir, auf Star zu klicken und ihn weiterzuleiten, um es zu verbreiten.