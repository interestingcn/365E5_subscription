# Office365 E5 开发者订阅续订工具
------
```python
  ____    __ _____ ______ _____            _                   _       _   _             
 |___ \  / /| ____|  ____| ____|          | |                 (_)     | | (_)            
   __) |/ /_| |__ | |__  | |__   ___ _   _| |__  ___  ___ _ __ _ _ __ | |_ _  ___  _ __  
  |__ <| '_ \___ \|  __| |___ \ / __| | | | '_ \/ __|/ __| '__| | '_ \| __| |/ _ \| '_ \ 
  ___) | (_) |__) | |____ ___) |\__ \ |_| | |_) \__ \ (__| |  | | |_) | |_| | (_) | | | |
 |____/ \___/____/|______|____/ |___/\__,_|_.__/|___/\___|_|  |_| .__/ \__|_|\___/|_| |_|
                            ______                              | |                      
                           |______|  interestingcn01@gmail.com  |_|   
```

### 当前状态 / STATUS：
[![GitHub last commit](https://img.shields.io/github/last-commit/interestingcn/365E5_subscription)](https://github.com/meloncn/OpenWrtAutoBuild) [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/interestingcn/365E5_subscription/365E5_subscription?label=%E8%87%AA%E5%8A%A8%E7%BB%AD%E8%AE%A2%E7%8A%B6%E6%80%81)](https://github.com/interestingcn/365E5_subscription/actions?query=workflow%3A%22365E5_subscription%22) ![GitHub search hit counter](https://img.shields.io/github/search/interestingcn/365E5_subscription/office365?color=green&label=%E6%90%9C%E7%B4%A2%E5%91%BD%E4%B8%AD) ![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/interestingcn/365E5_subscription/main?label=%E6%9B%B4%E6%96%B0%E9%A2%91%E7%8E%87)

---

## 什么是 365E5_subscription
365E5_subscription 是一个由Python3语言所编写的脚本程序,其主要功能用于访问Office365相关API以达到活跃开发者账户的目的,依托Python实现全平台的支持.


---
## 部署流程
### 一. 创建开发者账户并创建订阅所需子账户
### 二. 注册应用程序
1. 管理员身份进入 [Azure AD](https://aad.portal.azure.com/)
2. 注册一个应用程序，受支持的账户类型选择：任何组织目录（任一）
3. 返回概要获取 “应用程序(客户端) ID”
4. 在“证书和密码”中创建客户端密码获取“密码值”

### 三. 添加如下应用API权限(委托的权限)并代表管理员同意
    Calendars.ReadWrite、Contacts.ReadWrite、Directory.ReadWrite.All
    
    Files.ReadWrite.All、MailboxSettings.ReadWrite、Mail.ReadWrite
    
    Mail.Send、Notes.ReadWrite.All、People.Read.All
    
    Sites.ReadWrite.All、Tasks.ReadWrite、User.ReadWrite.All

### 四. 使用rclone程序获取子账户的Refresh_token内容
    PS：
    ./rclone.exe authorize "onedrive" "应用程序(客户端)ID" "密码值"
    
    拷贝返回的json文本，从中获取Refresh_token字段内容，保存至项目根目录token.txt

### 五. 部署私钥 (任一部署)
#### 1.私有服务器部署
使用文本编辑软件编辑`main.py`中的18-19行，填写对应的 “应用程序(客户端) ID” 与 “密码值” 


#### 2. Github Actions 部署
1. 创建个人密钥(Developer settings -> Personal access tokens -> Generate new token)命名为` GITHUB_TOKEN`，授予`repo`操作权限。
2. 新建仓库私钥 `APP_ID` ,内容为`appId ='应用程序ID' `
3. 新建仓库私钥 `APP_SECRET` ,内容为`appSecret = '密码值' `
4. 授予Actions对仓库的读写权限。

### 六. 部署完成
---

## 版权声明
    365E5_subscription遵循Apache2.0协议开源。
    
