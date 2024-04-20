from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao:

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_umidita_media(_mese):
        """
        Funzione che permette di ottenere l'umidità media per ciascuna località, nel mese specificato sfruttando la
        funzione di supporto get_all_situazioni()
        """
        # situazioni = MeteoDao.get_all_situazioni()
        # umidita_media = {}
        # for situazione in situazioni:
        #     if situazione.data.month == _mese:
        #         if situazione.localita not in umidita_media:
        #             umidita_media[situazione.localita] = [situazione.umidita]
        #         else:
        #             umidita_media[situazione.localita].append(situazione.umidita)
        # for localita in umidita_media:
        #     umidita_media[localita] = round(sum(umidita_media[localita]) / len(umidita_media[localita]), 4)
        # return umidita_media

        """
        Siccome il database è composto di una sola tabella, meglio trovare l'umidità media per ciascuna località direttamente
        nella query SQL
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, AVG(s.Umidita) AS um_media
                                FROM situazione s 
                                WHERE MONTH(s.Data) = %s
                                GROUP BY s.Localita"""
            cursor.execute(query, (_mese,))
            for row in cursor:
                result.append((row["Localita"],
                              row["um_media"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_situazioni_meta_mese(_mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                                FROM situazione s 
                                WHERE MONTH(s.Data) = %s AND DAY(s.Data) <= 15
                                ORDER BY s.Data ASC"""
            cursor.execute(query, (_mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result
