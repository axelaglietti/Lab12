from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        results = []
        query = """
                select distinct(gr.Country) as C
                from go_retailers gr 
                """
        cursor.execute(query)
        for row in cursor:
            results.append(row["C"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getRetailers(nazione):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        results = []
        query = """
                select gr.*
                from go_retailers gr 
                where gr.Country = %s
                """
        cursor.execute(query, (nazione,))
        for row in cursor:
            results.append(Retailer(row["Retailer_code"], row["Retailer_name"], row["Type"], row["Country"], 0))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getConnessione(anno, v0, v1):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = 0
        query = """
                select gds.Retailer_code, gds2.Retailer_code, COUNT(DISTINCT(gds.Product_number)) as N
                FROM go_daily_sales gds, go_daily_sales gds2
                where gds.Product_number = gds2.Product_number 
                and year(gds.`Date`) = year(gds2.`Date`) and year(gds2.`Date`) = %s AND gds.Retailer_code = %s 
                AND gds2.Retailer_code = %s
                """
        cursor.execute(query, (anno, v0.Retailer_code, v1.Retailer_code))
        for row in cursor:
            result = row["N"]
        cursor.close()
        conn.close()
        return result
