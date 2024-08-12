<div align="center">

[简体中文](https://github.com/SunoApi/SunoApi/blob/main/README_ZH.md) | [繁體中文](https://github.com/SunoApi/SunoApi/blob/main/README_TC.md) | [Русский](https://github.com/SunoApi/SunoApi/blob/main/README_RU.md) | [English](https://github.com/SunoApi/SunoApi/blob/main/README.md) | [한국어](https://github.com/SunoApi/SunoApi/blob/main/README_KR.md) | [Français](https://github.com/SunoApi/SunoApi/blob/main/README_FR.md) | [Deutsch](https://github.com/SunoApi/SunoApi/blob/main/README_DE.md)


[![GitHub release](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=black)](https://img.shields.io/github/v/release/SunoApi/SunoApi?label=release&color=blue)  ![GitHub last commit](https://img.shields.io/github/last-commit/SunoApi/SunoApi)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/SunoApi/SunoApi)  ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/SunoApi/SunoApi)  ![SunoApi GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/SunoApi/SunoApi/total)  [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg)](https://www.apache.org/licenses/LICENSE-2.0.html)

# SunoAPI 非公式 Suno AIクライアントです

# 今週のweeklyへの本開源プロジェクトの入選を祝う
### [![ruanyf](https://avatars.githubusercontent.com/u/905434?s=20) ruanyf added the weekly label 12 hours ago](https://github.com/ruanyf/weekly/issues/4263)

</div>



### 紹介

- これはPython、Streamlitに基づく非公式Suno APIクライアントであり、現在は音楽の生成、音楽情報の取得などの機能をサポートしている。トケンの期限切れを心配することなく、複数のアカウントの情報保存を設定して使用することができます。

- GitHubにアクセスできない場合があります。アクセスできない場合はGiteeアドレスに移動してください：https://gitee.com/SunoApi/SunoApi

### 特徴

- アカウント情報を記入するプログラム自動保守と保活
- 複数のアカウントを設定できる情報保存用
- 音楽共有広場に公開されたすべての曲を展示
- 楽曲情報を直接取得するために音楽番号を入力します
- アップロード画像解析コンテンツの楽曲生成に対応しています
- 中国語、英語、韓国語、日本語など多言語対応

### デバッグします

#### Pythonローカルデバッグ実行

- 複製ソースコードです

```bash
git clone https://github.com/SunoApi/SunoApi.git
```


- インストール依存

```bash
cd SunoApi
pip3 install -r requirements.txt
```

- .env環境変数ファイル、画像認識にgpt-4oを使用する必要があるモデルは、OpenAIのインタフェースを使用することも、他の自分がよく使うインタフェースに置き換えることもできます。console.bitiful.comオブジェクトストレージアカウントを登録してS3_ACCESSKEY_IDを取得し、S3_SECRETKEY_IDパラメータは画像を作成したストレージバケットにアップロードするために使用され、S3_WEB_SITE_URLはオブジェクトストレージアカウントを記入してストレージバケットを作成した後の外部アクセスドメイン名を記入します。これにより、ローカル環境で画像認識をテストすることができます。

```bash
OPENAI_BASE_URL = https://chatplusapi.cn
OPENAI_API_KEY = sk-xxxxxxxxxxxxxxxxxxxx
#S3_WEB_SITE_URL = https://cdn1.suno.ai
#S3_WEB_SITE_URL = http://localhost:8501
#S3_WEB_SITE_URL = http://123.45.67.8:8501
#S3_WEB_SITE_URL = https://sunoapi.s3.bitiful.net
S3_WEB_SITE_URL = https://res.sunoapi.net
S3_ACCESSKEY_ID = xxxxxxxxxxxxxxxxxxxx
S3_SECRETKEY_ID = xxxxxxxxxxxxxxxxxxxx
```


- プロジェクトを開始し、StreamlitについてはStreamlitドキュメントを参照してください

```bash
streamlit run main.py --server.maxUploadSize=3
```

### 配備します

#### Docker ローカルワンクリック配備です

```bash
docker run -d \
  --name sunoapi \
  --restart always \
  -p 8501:8501 \
  -v ./sunoapi.db:/app/sunoapi.db \
  -v ./images/upload:/app/images/upload \
  -v ./audios/upload:/app/audios/upload \
  -e OPENAI_BASE_URL=https://api.openai.com  \
  -e OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx \
  -e S3_WEB_SITE_URL=https://sunoapi.s3.bitiful.net  \
  -e S3_ACCESSKEY_ID=xxxxxxxxxxxxxxxxxxxx  \
  -e S3_SECRETKEY_ID=xxxxxxxxxxxxxxxxxxxx  \
  sunoapi/sunoapi:latest
```

##### 注意です: https://sunoapi.s3.bitiful.net 交替をあなたが実際の必要の住所を訪問し、最終の写真ファイルが http://xxxxxx.s3.bitiful.net/images/upload/xxxxxx.jpg の形で掲載できる訪問には、アップロードされた画像にOpenAIがアクセスできないと画像の内容を認識できず、画像をアップロードして音楽を生成する機能が使えなくなります。


#### Docker ネイティブコンパイル配備します

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
CMD [ "nohup", "streamlit", "run", "main.py", "--server.maxUploadSize=3" ]
```

#### Docker ミラーリング部署を引っ張ります

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
      - ./audios/upload:/app/audios/upload
    environment:
      - TZ=Asia/Shanghai
      - OPENAI_BASE_URL=https://api.openai.com
      - OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
      - S3_WEB_SITE_URL=https://sunoapi.s3.bitiful.net
      - S3_ACCESSKEY_ID=xxxxxxxxxxxxxxxxxxxx
      - S3_SECRETKEY_ID=xxxxxxxxxxxxxxxxxxxx
    restart: always
```

##### 注意です：ミラーリングの展開を引き出すには、プロジェクト内のsunoapi.dbをdocker-compose.ymlファイルディレクトリにダウンロードする必要があります。そうしないと、dockerの起動によりファイルをマウントできないことが示されます。


#### Streamlit リモート・ウェアハウスの配備します

- まずFork SunoApiコードをGithub倉庫に
- Github認証ログインを選択します。https://share.streamlit.io/
- 配備ページを開きます。https://share.streamlit.io/deploy
- Repository選択：SunoApi/SunoApi
- Branch入力：main
- Main file path入力：main.py
- Deployをクリック！

#### Zeabur ローカルワンクリック配備です

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/ORTEGG)


### 設定

- ブラウザのログイン状態から自分のセッションとクッキーを取得します。

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session.png" style="max-width: 100%;"/></a>

- 設定情報に記入すると自動的に保存され、複数のアカウント情報を記入することができます。

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session1.png" style="max-width: 100%;"/></a>

- 記入後は情報を保存し、identityを入力することでアカウント情報を変更修正できます。

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/session2.png" style="max-width: 100%;"/></a>

### 完成です

- プロジェクト実行後のブラウザアクセスの開始http://localhost:8501/すぐに使用できます。

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index1.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index2.png" style="max-width: 100%;"/></a>

- <a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/index3.png" style="max-width: 100%;"/></a>


### 問題

- ページプロンプト情報：ページを更新する前に情報を設定して保存してください！まず自分のアカウント情報を追加して保存してから、sunoapi.dbデータベースの他の無効なアカウント情報を削除してください。その中には私がテストしたアカウント情報が含まれていて、それから正常に使用することができます。
- ページプロンプト情報：Suno AI音楽歌曲生成のコミットに失敗した場合：Unauthorized.はアカウント登録状態が許可されていないことを示し、この場合は一般的に複数のブラウザクライアントがアカウントにログインしてプリエンプトを形成し、他のログインしたブラウザクライアントを終了し、アカウントをこのSuno API AI音楽歌曲生成器クライアントにログインしたままにし、他のブラウザクライアントにログインしないでください。
- ページプロンプト情報：Suno AI楽曲生成のコミットに失敗した場合：Insufficient credits.アカウント情報creditsの点数が不足していることを示します。まず自分のアカウント情報を追加して保存してから、正常に使用することができます。
- ページプロンプトにエラーが発生した場合：ModuleNotFoundError：No module named'streamlit _ image _ selectこれは、streamlit _ image _ selectコンポーネントの機能を2回開発したためです。2回開発後、このコンポーネントはプログラム実行中のpagesディレクトリに格納されています。プログラム実行ディレクトリ1回目のロードstreamlit _ image _ selectコンポーネントはPython 3のsite-packagesディレクトリにロードされていますが、2回開発されたコンポーネントはpip 3 install streamlit _ image _ selectロケーションで保存されたプログラム二次開発の機能は使用できませんが、解決策は左メニューの他のページリンクをクリックしてから正常にロードして使用することです。
- 音楽生成タスクのコミットに成功した後、生成タスクキュー状態をプルし、状態が「complete」の場合は正常に戻り、この場合はデフォルトで15秒滞在して公式生成ファイルを待ちます。公式インタフェースサービスはメディアファイルのUrlアドレスに直接戻り、ほとんどの場合ページにこれらのメディアファイルが正常に表示されます。インタフェースがメディアファイルのUrlアドレスを返している場合もありますが、実際のファイルはUrlアドレスからアクセスできないのでしばらく待ちます。この時点でメディアファイルはページにロードできない可能性があります。メディアプレイヤーをクリックしてメディアファイルのアドレスを右クリックしてコピーし、ブラウザでこのアドレスを単独で開くことでアクセスできます。または、直接右クリックしてダウンロードとして保存することができます。または、生成されたレコードを音楽共有プラザのページリストに表示することもできます。
- アカウントsessionとcookieの情報保存セキュリティの設定については、あなたのアカウントがチャージされていない限り心配する必要はありません。あなたのアカウントのパスワードが分からないので、あなたが記入したsessionとcookieの情報は、あなたのアカウントが他の場所でイベントにログインしたり、公式サイトでログインを退出したりすれば、記入したsessionとcookieは無効になり、次の公式サイトsessionとcookieにログインしても変わります。


### オーサリング

- 専門歌詞支援ツール：https://poe.com/SuperSunoMaster


### こうりゅう

- Github Issues： https://github.com/SunoApi/SunoApi/issues

<a href="https://sunoapi.net" target="_blank"><img src="https://sunoapi.net/images/wechat.jpg?20240812" style="max-width: 100%;"/></a>


### 参加する

- 個人の力は常に限られており、どのような形の貢献も歓迎されています。貢献コード、文書の最適化、IssueとPRの提出などが含まれていますが、これに限られていないので、微信や微信グループで開発者にBugを提出することは受け入れられません。問題や最適化の提案があれば、IssueとPRを提出してください。

<a href="https://star-history.com/#SunoApi/SunoApi" target="_blank"><img src="https://api.star-history.com/svg?repos=SunoApi/SunoApi" style="max-width: 100%;"/></a>


### リファレンス

- Suno AI 公式サイト: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


### ステートメント

- SunoAPIは非公式のオープンソースプロジェクトで、学習と研究用にのみ使用されています。ユーザは任意に無料のアカウント情報を入力して音楽を生成する。各アカウントは毎日5曲の曲を無料で生成でき、他の目的には使用しません。安心してお使いください！10000人のユーザーがいる場合、システムは毎日50,000曲を無料で生成することができます。各アカウントでは1日5曲の曲しか無料で生成できないので、できるだけ使用量を節約してください。一人一人が毎日5曲以上の曲を作るとしたら、それはまだ足りない。最終的には、必要なときにいつでも無料で生成できるようにすることを目指しています。


### Buy me a Coffee

<a href="https://www.buymeacoffee.com/SunoApi" target="_blank"><img src="https://sunoapi.net/images/donate.jpg" alt="Buy me a Coffee" style="max-width: 100%;"></a>


##### このプロジェクトはGitHubから始まり、MITのプロトコルに基づいており、無料です。もしあなたはこの項目があなたに対して助けがあると感じるならば、私を手伝ってStarを点(点)して拡散を転送して、ここであなたに感謝します!