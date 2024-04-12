[繁體中文](README_TC.md) | [English](README.md) | [한국어](README_KR.md)

# Suno API 非官方 Suno AI 客户端

这是一个基于 Python、Streamlit 的非官方 Suno API 客户端，目前支持生成音乐，获取音乐信息等功能。  
自带维护 token 与保活功能，无需担心 token 过期问题，可以设置多个账号的信息保存以便使用。

### 特点

- token 自动维护与保活
- 可以设置多个账号的信息保存使用
- 代码简单，易于维护，方便二次开发

### 使用

#### 运行

安装依赖

```bash
pip3 install -r requirements.txt
```

启动项目，关于Streamlit请自行参考Streamlit文档

```bash
streamlit run main.py
```

#### Docker

```bash
docker compose build && docker compose up
```


#### 配置

先从浏览器页面登录状态下中获取自己的session和cookie。

![session](./images/session.png)

填写设置信息里面后面会自动保活，可以填写多个账号信息。

![session1](./images/session1.png)

填写后保存信息，更改输入identity可以即可修改账号信息。

![session2](./images/session2.png)

#### 完成

启动运行项目后浏览器访问 http://localhost:8501/ 即可使用了。

![docs](./images/index.png)


#### 问题

如果页面一直提示：请先设置信息保存，然后再刷新页面才能正常使用！请先添加自己的账号信息保存，然后把sunoapi.db数据库里面其他无效的账号信息删除，其中包括我测试的账号信息，然后再就可以正常使用了。


#### 交流

<img src="./images/wechat.jpg" width="382px" height="511px" />


## 参考

- Suno.com 官网: [https://suno.com](https://suno.com)
- Suno-API: [https://github.com/SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)


## 声明

SunoApi 是一个非官方的开源项目，仅供学习和研究使用。