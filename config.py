class Config(object):
    DEBUG = False
    TESTING = False
    SERVER_NAME_DB = '127.0.0.1'
    PORT_DB = 9042
    FX_API_KEY = "RfWfTDTNnsRdLuWHEWT3"
    CURRENCIES = ['EUR', 'GBP', 'USD', 'CAD', 'CHF', 'AUD', 'JPY']

class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
