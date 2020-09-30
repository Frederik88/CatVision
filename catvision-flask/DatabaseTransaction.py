import mysql.connector
from mysql.connector import Error

class DatabaseTransaction:

    def save_img_to_db(self, img_path, name, timestamp, detection):
        print("[DB TRANSACTION]: Insert Img into image_model table")
        try:
            connection = mysql.connector.connect(host='192.168.111.111',
                                                 database='catvision',
                                                 user='catvision',
                                                 password='Catvision_1234')
            cursor = connection.cursor()
            sql_insert_query = """ INSERT INTO image_model
                                (img_path, name, timestamp, detection) VALUES (%s,%s,%s,%s)"""
            
            insert_tuple = (img_path, name, timestamp, detection)
            result = cursor.execute(sql_insert_query, insert_tuple)
            connection.commit()
            print("[DB TRANSACTION]: Img successfully inserted into image_model")
            
        except mysql.connector.Error as error:
            print("[DB TRANSACTION]: Failed inserting Img data into MySQL table {}".format(error))

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("[DB TRANSACTION]: MySQL connection is closed")
    