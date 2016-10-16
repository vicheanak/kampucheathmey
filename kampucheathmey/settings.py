
BOT_NAME = 'kampucheathmey'

SPIDER_MODULES = ['kampucheathmey.spiders']
NEWSPIDER_MODULE = 'kampucheathmey.spiders'

ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
    'kampucheathmey.pipelines.MySQLPipeline': 2
}

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = 'helloworld'
DB_DB = 'khmergoo_sequelize'
