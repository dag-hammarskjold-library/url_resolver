class Config():
    BASE_URL = 'https://digitallibrary.un.org'
    NS = '{http://www.loc.gov/MARC21/slim}'
    PATH = '/search'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
