from database.DBConnect import DBConnect
from model.esempio_classe import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_nazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gr.Country 
                    from go_retailers gr """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_vertici(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr 
                    where gr.Country = %s 
                     """

        cursor.execute(query, (nazione,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi(nazione, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT gds1.Retailer_code AS Retailer1, gds2.Retailer_code AS Retailer2, COUNT(distinct gds1.Product_number) AS CommonProducts
                    from (select gds.*
                    from go_retailers gr, go_daily_sales gds
                    where gr.Country = %s and year(gds.`Date`) = %s and gr.Retailer_code = gds.Retailer_code) as gds1, (select gds.*
                    from go_retailers gr, go_daily_sales gds
                    where gr.Country = %s and year(gds.`Date`) = %s and gr.Retailer_code = gds.Retailer_code) as gds2
                    where gds1.Product_number = gds2.Product_number and gds1.Retailer_code < gds2.Retailer_code
                    group by gds1.Retailer_code, gds2.Retailer_code
                    order by gds1.Retailer_code"""

        cursor.execute(query, (nazione, anno, nazione, anno, ))

        for row in cursor:
            result.append([row["Retailer1"], row["Retailer2"], row["CommonProducts"]])

        cursor.close()
        conn.close()
        return result
