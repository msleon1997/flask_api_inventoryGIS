class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'inventory'
    #MYSQL_PORT = '3306'
    


config = {
    'production': DevelopmentConfig
}
