import mysql.connector

# mysql_cnx = mysql.connector.connect(user='dissingjan', password='pass1234#',
#                               host='curvex-delivery5-mysql.mysql.database.azure.com',
#                               database='curvex')

# cu = "cu"

def mysql_cnx_query(query):
    mysql_cnx = mysql.connector.connect(user='dissingjan', password='pass1234#',
                              host='curvex-delivery5-mysql.mysql.database.azure.com',
                              database='curvex')
    mycursor = mysql_cnx.cursor(dictionary=True)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    mysql_cnx.commit()
    mysql_cnx.close()
    return myresult