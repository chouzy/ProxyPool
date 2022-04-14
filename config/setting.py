import platform
from os.path import dirname, abspath, join

from environs import Env

env = Env()
env.read_env()  # 读取文件

# 判断操作系统
IS_WINDOWS = platform.system().lower() == 'windows'

# 设置项目文件路径
BASE_DIR = dirname(dirname(abspath(__file__)))
# 设置日志存储路径
LOG_DIR = join(BASE_DIR, env.str('LOG_DIR', 'logs'))

# 设置项目环境
DEV_MODE, TEST_MODE, PROD_MODE = 'develop', 'test', 'product'
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False)

# 配置 Redis
REDIS_HOST = env.str('REDIS_HOST', '127.0.0.1')  # redis host
REDIS_PORT = env.int('REDIS_PORT', 6379)  # redis port
# redis password, if no password, set it to None
REDIS_PASSWORD = env.str('REDIS_PASSWORD', 'root')
REDIS_DB = env.int('REDIS_DB', 0)  # redis db, if no choice, set it to 0
REDIS_KEY = env.str('REDIS_KEY', 'proxy')  # redis hash table key name

# 配置 score 分数
SCORE_MAX = 100
SCORE_MIN = 0
SCORE_INIT = 10

# 设置代理池数量
NUMBER_MAX = 5000
NUMBER_MIN = 0

# 代理测试 URL
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)
TEST_BATCH = env.int('TEST_BATCH', 20)  # 测试批次

# 每次测试代理的时间间隔
CYCLE_TESTER = env.int('CYCLE_TESTER', 20)
# 每次获取代理的时间间隔
CYCLE_GETTER = env.int('CYCLE_GETTER', 100)
GET_TIMEOUT = env.int('GET_TIMEOUT', 10)

# 配置 API 接口信息
API_HOST = env.str('API_HOST', '127.0.0.1')
API_PORT = env.int('API_PORT', 5000)

# 是否启动模块
START_TESTER = env.bool('START_TESTER', False)  # 测试代理
START_GETTER = env.bool('START_GETTER', False)  # 获取代理
START_SERVER = env.bool('START_SERVER', True)  # 创建 API

# 配置日志
ENABLE_LOG_FILE = env.bool('ENABLE_LOG_FILE', True)
ENABLE_LOG_RUNTIME_FILE = env.bool('ENABLE_LOG_RUNTIME_FILE', True)
ENABLE_LOG_ERROR_FILE = env.bool('ENABLE_LOG_ERROR_FILE', True)

LOG_LEVEL_MAP = {
    DEV_MODE: "DEBUG",
    TEST_MODE: "INFO",
    PROD_MODE: "ERROR"
}

# LOG_LEVEL = LOG_LEVEL_MAP.get(APP_ENV)

# if ENABLE_LOG_FILE:
#     if ENABLE_LOG_RUNTIME_FILE:
#         logger.add(env.str('LOG_RUNTIME_FILE', join(LOG_DIR, 'runtime.log')),
#                    level=LOG_LEVEL, rotation='1 week', retention='20 days')
#     if ENABLE_LOG_ERROR_FILE:
#         logger.add(env.str('LOG_ERROR_FILE', join(LOG_DIR, 'error.log')),
#                    level='ERROR', rotation='1 week')
