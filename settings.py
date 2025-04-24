TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",
                "port": "3306",
                "user": "root",
                "password": "1234512345qw!!",
                "database": "FastAPI",
                "charset": "utf8mb4",
                "connect_timeout": 30  # 连接超时时间
            }
        }
    },
    "apps": {
        "models": {
            "models": ["models","aerich.models"],
            "default_connection": "default"
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai"
}