class Config(object):
    DEBUG = False
    TESTING = False
    base_url = 'https://digitallibrary.un.org'
    ns = '{http://www.loc.gov/MARC21/slim}'
    path = '/search'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
