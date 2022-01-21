class config():
    def __init__(self):
        import MySQLdb

        self.__RDSHost = 'localhost'
        self.__PORT = 3306
        self.__RDSUser = 'root'
        self.__RDSPass = ""
        self.__RDSDb = 'mls2'

        self.MySQLdb = MySQLdb

        self.mydb = self.MySQLdb.connect(host = self.__RDSHost,
            port=self.__PORT,
            user = self.__RDSUser,
            passwd = self.__RDSPass,
            db = self.__RDSDb)
