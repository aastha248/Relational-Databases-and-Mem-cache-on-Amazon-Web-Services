import os
import mysql.connector
import csv
import time
import random
import memcache
import hashlib
from flask import Flask, request, make_response

app = Flask(__name__)

db = mysql.connector.connect(host='db1.cn9dedqrxcon.us-west-2.rds.amazonaws.com',database='test_db',user='aastha_user',password='rohini12')

cursor=db.cursor(buffered=True)

mc = memcache.Client(['memcache.ynav65.cfg.usw2.cache.amazonaws.com:11211'])

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
	beforeTime = time.time()
    sql = "CREATE TABLE data(`Complaint ID` text, GivenName text, Surname text, StreetAddress text, City text, State text, EmailAddress text, Age int, Centimeters int)"
    cursor.execute(sql)
    db.commit()

    sql =  """LOAD DATA LOCAL INFILE '/home/ubuntu/flaskapp/data.csv' INTO TABLE data FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES """
    cursor.execute(sql)
    After_Time = time.time()
    Time_difference = After_Time - beforeTime
    db.commit()
    return "File Loaded in" + str(Time_difference)

@app.route('/display_rds', methods=['GET', 'POST'])
def rds():
	sql = "select * from data"
	cursor.execute(sql)
	count_res=cursor.fetchall()
	count = len(count_res)
	beforeTime = time.time()
	for x in range(1, 5000):
		rand_number = random.randrange(0,count)
		sqlselect = "SELECT * FROM data LIMIT {}".format(rand_number)
		cursor.execute(sqlselect)
		count_res = cursor.fetchall()
	afterTime = time.time()
	db.commit()
	timeDifference = afterTime - beforeTime
	return str(float(timeDifference))

@app.route('/display_limited_rds', methods=['GET', 'POST'])
def limited_rds():
        sql = 'select `Complaint ID` from data;'
        cursor.execute(sql)
        count_res=cursor.fetchall()
	list1 = []
        for row in count_res:
		list1.append(row[0])
	beforeTime = time.time()
        for x in range(1, 5000):
                rand_number = random.choice(list1)
                sqlselect = "SELECT * FROM data where `Complaint ID` = {}".format(rand_number)
                cursor.execute(sqlselect)
                count_res = cursor.fetchall()
        afterTime = time.time()
        db.commit()
        timeDifference = afterTime - beforeTime
        return str(float(timeDifference))


@app.route('/display_memcache', methods=['GET', 'POST'])
def memcache():
	sql='SELECT * FROM data'
	cursor.execute(sql)
	count_res=cursor.fetchall()
	count = len(count_res)
	beforeTime = time.time()
	for x in range(1, 5000):
                rand_number = random.randrange(0,count)
                sqlselect = "SELECT * FROM data LIMIT {}".format(rand_number)
		plaintext = hashlib.md5(sqlselect.encode())
		plaintext = plaintext.hexdigest()
		value = mc.get(plaintext)
		if (value is None):
			status=cursor.execute(sqlselect)
			mc.set(plaintext,status)
			db.commit()
	afterTime = time.time()
	timeDifference = afterTime - beforeTime
	return str(float(timeDifference))

@app.route('/display_limited_memcache', methods=['GET', 'POST'])
def limited_memcache():
        sql = 'select `Complaint ID` from data;'
        cursor.execute(sql)
        count_res=cursor.fetchall()
        list1 = []
        for row in count_res:
                list1.append(row[0])
	beforeTime = time.time()
        for i in range (1, 5000):
                rand_number = random.choice(list1)
                sqlselect = "SELECT * FROM data where `Complaint ID` = {}".format(rand_number)
                plaintext = hashlib.md5(sqlselect.encode())
                plaintext = plaintext.hexdigest()
                value = mc.get(plaintext)
                if (value is None):
                        status=cursor.execute(sqlselect)
                        mc.set(plaintext,status)
                        db.commit()
        afterTime = time.time()
        timeDifference = afterTime - beforeTime
        return str(float(timeDifference))

@app.route('/')
def first_page():
	return app.send_static_file('index.html')

if __name__ == '__main__':
  app.run()
