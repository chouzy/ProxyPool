# ProxyPool

> 项目参照：[Python3WebSpider: ProxyPool](https://github.com/Python3WebSpider/ProxyPool)

爬虫代理池，实现以下功能：

- 获取代理网站免费代理；

- 使用 redis 存储代理数据；

- 提供测试类测试代理的可用性；

- 提供代理 API 接口；

## 项目结构

```
ProxyPool
 ├── config                       # 配置模块
 │   └── setting.py
 ├── proxypool                    # 代理池
 │   ├── comm                       # 通用模块
 │   │   ├── proxy.py
 │   │   └── utils.py
 │   ├── main.py                  # 调度器
 │   ├── service                  # 服务
 │   │   ├── server.py
 │   │   └── tester.py
 │   ├── spiders                  # 爬虫
 │   │   └── public
 │   │       └── kuaidaili.py
 │   └── storages                 # 存储
 │       └── redis_db.py
 ├── README.md
 ├── requirements.txt
 └── run.py                       # run
```

## 运行

### 安装依赖

```shell
pip install -r requirement.txt
```

### 设置项目配置

```
ProxyPool -> config -> setting.py
```

### 运行代理池

1. 全部运行

```shell
python run.py
```

2. 按需运行

```shell
python run.py --processor getter
python run.py --processor tester
python run.py --processor server
```


