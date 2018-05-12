# API

#### 引っ張りの登録（ユーザをサーバ側で勝手に指定バージョン）
```
method：GET
endpoint：api/pull/test
request：
{}
response：
{
    "msg": "Success"
}
```

#### 引っ張りの登録
```
method：POST
endpoint：api/pull
request：
{
    "id": 1
}
response：
{
    "msg": "Success"
}
```