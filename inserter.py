import psycopg2
import pandas as pd
import psycopg2.extras
from datetime import datetime
import numpy as np
import time


conn_details = psycopg2.connect(
	host="localhost",
	database="statsCanada",
	user="postgres",
	password="JVKMarg",
	port= "5432"
)



cursor = conn_details.cursor()



def convert_to_date(date_):
	date_ = datetime.strptime(date_, '%d-%m-%Y')
	return date_



def createminitradeTable():
	sql_query = '''CREATE TABLE tradeCanada
		(
			REF_date date NOT NULL,
			GEO VARCHAR(64),
			trade VARCHAR(32),
			NAPCS VARCHAR (128),
			principal_trading_partner VARCHAR(64),
			value NUMERIC(16)
			)'''
	cursor.execute(sql_query)
	conn_details.commit()
	cursor.close()
	conn_details.close()



def insertatradefromCSV():
	df = pd.read_csv(r"12100175_6_columns.csv")
	lenDF = len(df)
	df = df.replace({np.nan: None})
	
	for index, row in df.iterrows():
		
		dateMY = row['REF_DATE']
		GEO = row['GEO']
		trade = row['Trade']
		NAPCS = row['North American Product Classification System (NAPCS)']
		partner = row['Principal trading partners']
		value = row['VALUE']

		docSingle = (dateMY, GEO, trade, NAPCS, partner, value)

		sql_query = '''INSERT INTO tradeCanada VALUES(%s, %s, %s, %s, %s, %s)'''


		cursor.execute(sql_query, docSingle)

		if index%10000 == 0:
			print(index, ' / ', lenDF)
			conn_details.commit()
	conn_details.commit()
	cursor.close()
	conn_details.close()



if __name__ == "__main__":
	# createminitradeTable()
	# time.sleep(10)
	insertatradefromCSV()