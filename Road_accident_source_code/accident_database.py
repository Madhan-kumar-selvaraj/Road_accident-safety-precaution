import mysql.connector

# MYSQL connector
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Ubuntu@220417",
        database="Road_accident")
mycursor = mydb.cursor()


def mysql_data(state, feature_value):
    # Creating SQL query
    sql_query = "select "+", ".join(feature_value)+"  from accident where  States_UTs='"+ state +"' or States_UTs='Threshold percentage'"
    mycursor.execute(sql_query)
    myresult = mycursor.fetchall()
    return myresult

