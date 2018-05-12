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

#### 起動時（前回の引っ張り回数を取得）
```
method：GET
endpoint：/api/walk/prevwalk?user_id=1
request：
{}
response：
{
    "now": 123
}
```

#### スタートボタンタップ時（お散歩開始）
```
method：POST
endpoint：/api/walk
request：
{
    "user_id": 1
}
response：
{
    "walk_id": 12
}
```

#### ストップボタンタップ時（本当に終了する前のアラート出すところ）
```
method：GET
endpoint：/api/walk/now?user_id=1
request：
{}
response：
{
    "now": 12
}
```

#### お散歩終了時（本当に終了する前のアラートの終了を押した時）
```
method：PUT
endpoint：/api/walk
request：
{
    "walk_id": 10
}
response：
{
    "results": [
        {
            "count": 1,
            "time": "2018-05-12 22:35:00"
        },
        {
            "count": 3,
            "time": "2018-05-12 22:40:00"
        },
        {
            "count": 1,
            "time": "2018-05-12 22:45:00"
        },
        {
            "count": 3,
            "time": "2018-05-13 00:10:00"
        },
        {
            "count": 10,
            "time": "2018-05-13 00:15:00"
        },
        {
            "count": 2,
            "time": "2018-05-13 00:20:00"
        },
        {
            "count": 2,
            "time": "2018-05-13 01:00:00"
        },
        {
            "count": 3,
            "time": "2018-05-13 01:05:00"
        },
        {
            "count": 2,
            "time": "2018-05-13 01:35:00"
        },
        {
            "count": 2,
            "time": "2018-05-13 01:40:00"
        },
        {
            "count": 4,
            "time": "2018-05-13 02:15:00"
        }
    ]
}
```


#### リスト一覧表示
```
method：GET
endpoint：/api/walk/list?user_id=1
request：{}
response：
{
    "results": [
        {
            "count": 13,
            "date": "2018-05-12",
            "id": 4
        }
    ]
}
```