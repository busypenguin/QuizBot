from environs import Env


env = Env()
env.read_env()

REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.int('REDIS_PORT')
REDIS_PASSWORD = env.str('REDIS_PASSWORD')

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')
VK_TOKEN = env.str('VK_TOKEN')
