<div align="center">

[简体中文](https://github.com/SunoApi/SunoApi/blob/main/README_ZH.md) | [繁體中文](https://github.com/SunoApi/SunoApi/blob/main/README_TC.md) | [Русский](https://github.com/SunoApi/SunoApi/blob/main/README_RU.md) | [English](https://github.com/SunoApi/SunoApi/blob/main/README.md) | [한국어](https://github.com/SunoApi/SunoApi/blob/main/README_KR.md) | [日本語](https://github.com/SunoApi/SunoApi/blob/main/README_JP.md) | [Deutsch](https://github.com/SunoApi/SunoApi/blob/main/README_DE.md)


[![GitHub release](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=black)](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=blue)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# Suno API non officiel Suno AI client

# Félicitations à ce projet open source sélectionné pour l’weekly de la semaine
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>



### Présentation

- Ceci est un client non officiel de l’api Suno basé sur Python, Streamlit. Actuellement, il prend en charge la génération de musique, obtenir des informations musicales et plus. Vient avec le jeton de maintenance avec la fonction de rétention, pas besoin de s’inquiéter du problème de jeton expiré, vous pouvez définir plusieurs comptes pour sauver les informations afin de les utiliser.

- Parfois visite GitHub, inaccessibles veuillez visite Gitee adresse: https://gitee.com/SunoApi/SunoApi

### caractéristiques

- remplir le Programme d'information sur le numéro de compte maintenance et conservation automatiques
- il est possible de configurer plusieurs numéros de compte pour conserver les informations à utiliser
- la place de partage de musique affiche toutes les chansons publiques
- Entrez le numéro de musique pour obtenir directement les informations sur la chanson

### Débogage

#### Exécution du débogage local Python

- Installation des dépendances

```bash
pip3 install -r requirements.txt
```

- Lancer un projet, à propos de streamlit Veuillez vous référer à la documentation streamlit

```bash
streamlit run main.py
```


### Déploiement

#### Déploiement docker local en un clic

```bash
docker run -d \
  --name sunoapi \
  --restart always \
  -p 8501:8501 \
  sunoapi/sunoapi:latest
```


#### Déploiement de la compilation locale docker

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

#### Docker pull déploiement de l’image

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

#### Déploiement d’entrepôt distant Streamlit

- Fork un code sunoapi dans votre entrepôt github
- sélectionnez github authorize login: https://share.streamlit.io/
- Ouvrez la page de déploiement: https://share.streamlit.io/deploy
- repository sélectionnez: sunoapi / sunoapi
- Branch entrée: main
- entrée du chemin du fichier principal: main.py
- cliquez sur deploy!

#### Déploiement de Zeabur en un clic

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/5BLAEZ)


### La configuration

- Obtenez d’abord votre propre session et les cookies à partir de l’état de connexion de la page du navigateur.

- <img src="https://sunoapi.net/images/session.png" width="1012px"/>

- Remplissez les informations de réglage à l’intérieur derrière sera automatiquement préservé, vous pouvez remplir plusieurs informations de compte.

- <img src="https://sunoapi.net/images/session1.png" width="1012px"/>

- Remplissez et sauvegardez les informations, entrez l’identité pour changer et modifier les informations du compte.

- <img src="https://sunoapi.net/images/session2.png" width="1012px"/>

### L’achèvement du

- Après le lancement du projet d’exécution du navigateur visite http://localhost:8501/ peut être utilisé.

- <img src="https://sunoapi.net/images/index.png" width="1012px"/>

- <img src="https://sunoapi.net/images/index1.png" width="1012px"/>

- <img src="https://sunoapi.net/images/index2.png" width="1012px"/>

- <img src="https://sunoapi.net/images/index3.png" width="1012px"/>


### La question

- si la page vous invite à un message: s’il vous plaît définir le message de sauvegarde d’abord, puis rafraîchir la page pour une utilisation normale! S’il vous plaît ajouter vos propres informations de compte pour les sauvegarder d’abord, puis supprimer les autres informations de compte invalides dans la base de données sunoapi.db, y compris les informations de compte que j’ai testé, puis il peut être utilisé normalement.
- si la page affiche le message: Suno AI music song generation soumission a échoué: crédits insuffisants. Cela signifie que les points de crédits d’informations de compte sont insuffisants. S’il vous plaît ajouter vos propres informations de compte pour les enregistrer d’abord, puis il peut être utilisé normalement.
- tirez et générez l’état de la file d’attente des tâches après que la tâche de génération de musique a été soumise avec succès. Il est retourné avec succès lorsque l’état est "complet ". À ce moment, par défaut, il reste 15 secondes en attendant le fichier de génération officiel. Le service d’interface officiel renvoie directement l’adresse Url des fichiers multimédia. La plupart du temps, la page affiche normalement ces fichiers multimédia. Parfois, l’interface a retourné l’adresse Url du fichier multimédia, mais le fichier réel n’est pas encore accessible à partir de l’adresse Url à attendre un peu. À ce moment, le fichier multimédia sur la page peut ne pas être chargé, vous pouvez cliquer sur le bouton droit de la souris dans le lecteur multimédia pour copier l’adresse du fichier multimédia, ouvrir cette adresse avec un navigateur séparément pour accéder ou directement le bouton droit et enregistrer comme téléchargement pour enregistrer.
- en ce qui concerne la mise en place de la session de compte et les informations de cookie pour sauver la question de sécurité, tant que votre compte ne recharge pas besoin de s’inquiéter, parce que vous ne savez pas votre mot de passe de compte, vous remplissez la session et les informations de cookie tant que votre compte dans d’autres activités de connexion ailleurs, ou sur le site officiel de se déconnecter, Ensuite, la session et les cookies remplis ne sont pas valides, et la prochaine fois que vous vous connectez sur le site officiel, la session et les cookies changeront.


### La création

- Aide lyrique professionnelle:https://poe.com/SuperSunoMaster


### Les échanges

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<img src="https://sunoapi.net/images/wechat.jpg" width="382px" height="511px"/>


### La participation

- Le pouvoir personnel est toujours limité et les contributions de toute nature sont les bienvenues, y compris, mais sans s'y limiter, le Code de contribution, l'optimisation de la documentation, la soumission d'issue et de pr, les bogues ne sont pas acceptés sur WeChat ou wechat pour les développeurs en raison du temps limité, les questions ou les suggestions d'optimisation sont les bienvenues.

[![Star History Chart](https://api.star-history.com/svg?repos=SunoApi/SunoApi)](https://star-history.com/#SunoApi/SunoApi)


### De référence

- Suno AI Site officiel: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### La déclaration

- SunoApi est un projet open source non officiel destiné uniquement à l’apprentissage et à la recherche. Les utilisateurs entrent volontairement des informations de compte gratuites pour générer de la musique. Chaque compte peut générer gratuitement cinq chansons par jour. Nous ne les utiliserons pas à d’autres fins. S’il vous plaît utiliser avec confiance! Avec 10000 utilisateurs, le système peut générer 50000 chansons par jour gratuitement. S’il vous plaît essayer d’économiser sur l’utilisation, car chaque compte ne peut générer que cinq chansons gratuitement par jour. Si chacun compose plus de cinq chansons par jour, cela ne suffit pas. Le but ultime est de pouvoir générer gratuitement à tout moment et en cas de besoin.


### Buy me a Coffee

<a href="https://www.buymeacoffee.com/SunoApi" target="_blank"><img src="https://sunoapi.net/images/donate.jpg" alt="Buy me a Coffee" width="398px" height="398px"></a>