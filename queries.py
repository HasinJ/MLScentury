
from db import config

class Queries(config):

    def __init__(self, dictionary):
        super().__init__()
        self.__extractions = dictionary
        self.cursor = self.mydb.cursor()

    def loadRef(self, href, test=False):
        try:
            self.cursor.execute("INSERT INTO reftbl (`UID`,`href`) VALUES (%(UID)s, %(href)s)", {'UID': self.__extractions['UID'], 'href': href});
            self.mydb.commit()
            print(f"LOADED REF: {self.__extractions['address']['street']}, {self.__extractions['address']['state']} inserted.")

        except self.MySQLdb._exceptions.IntegrityError: #https://stackoverflow.com/questions/4205181/insert-into-a-mysql-table-or-update-if-exists
            print(f"Ref: {self.__extractions['address']['street']}, {self.__extractions['address']['state']} exists in refTBL.")


    def getUIDaddress(self, test=False):
        self.cursor.execute('SELECT `UID` FROM `addresstbl` WHERE street=%(street)s AND city=%(city)s AND state=%(state)s AND postal=%(postal)s', (
                self.__extractions['address']
            )
        )
        self.mydb.commit()
        result = self.cursor.fetchall()
        if test: print(f"UID: {result[0][0]}")
        #self.cursor.close()
        self.__extractions['UID']=result[0][0]

    def loadAddress(self, test=False):
        try:
            self.cursor.execute('INSERT INTO addressTBL (`street`, `city`, `state`, `postal`) VALUES (%(street)s, %(city)s, %(state)s, %(postal)s);', self.__extractions['address'])
            self.mydb.commit()
            #self.cursor.close()

            print(f"LOADED ADDRESS: {self.__extractions['address']['street']}, {self.__extractions['address']['state']} inserted.")

        except self.MySQLdb._exceptions.IntegrityError: #https://stackoverflow.com/questions/4205181/insert-into-a-mysql-table-or-update-if-exists
            print(f"Address: {self.__extractions['address']['street']}, {self.__extractions['address']['state']} exists in addressTBL.")

        self.getUIDaddress(test)
        return

    def loadDetails(self, test=False):
        #details = {'listing': '', 'acres': 0, 'price': 0, 'tax': 0, 'baths': 0, 'beds': 0, 'halfbaths': 0}
        #details = self.__extractions['details']
        #details['updated_listing'], details['updated_price'], details['updated_tax'] =
        self.__extractions['details']['UID'] = self.__extractions['UID']

        try:
            self.cursor.execute("""
            INSERT INTO detailstbl (`listing`, `acres`, `price`, `tax`, `baths`, `beds`, `halfbaths`, `UID`)
            VALUES (%(listing)s, %(acres)s, %(price)s, %(tax)s, %(baths)s, %(beds)s, %(halfbaths)s, %(UID)s)
            ON DUPLICATE KEY UPDATE `listing`=%(listing)s, `acres`=%(acres)s, `price`=%(price)s, `tax`=%(tax)s, `baths`=%(baths)s, `beds`=%(beds)s, `halfbaths`=%(halfbaths)s
            ;
            """,
                self.__extractions['details']
            )
            self.mydb.commit()
            #self.cursor.close()

            print(f"LOADED DETAILS: {self.__extractions['address']['street']}, {self.__extractions['address']['state']} inserted.")

        except self.MySQLdb._exceptions.IntegrityError: #https://stackoverflow.com/questions/4205181/insert-into-a-mysql-table-or-update-if-exists
            print(f"Details: {self.__extractions['address']['street']}, {self.__extractions['address']['state']} exists in detailstbl.")
            return


    def setExtractions(self, extractions):
        self.__extractions = extractions
