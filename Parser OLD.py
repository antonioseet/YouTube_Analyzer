import os
import psycopg2

#path to folder containing crawl txt files
path = r" C:\Users\aabar\Downloads\New folder	 (2)\080727 "
os.chdir(path)

try:
    #establish connection
    ## db, user, host, and password need to be updated for Azure db
    conn = psycopg2.connect("dbname='tempyelp' user='postgres' host='localhost' password='pswd'")
except:
    print('Unable to connect to the database!')
cur = conn.cursor()

#check if tables have already been created, drop if so
cur.execute("DROP TABLE IF EXISTS VideoData;")
cur.execute("DROP TABLE IF EXISTS RelatedVid;")

#create tables
cur.execute("CREATE TABLE VideoData (vidID CHAR(11) PRIMARY KEY, uploader VARCHAR(30), age INTEGER, category VARCHAR(30), length INTEGER, views INTEGER, rate FLOAT(2), ratings INTEGER, comments INTEGER);")
cur.execute("CREATE TABLE RelatedVid (vidID CHAR(11) PRIMARY KEY, relatedId CHAR(11));")

for file in os.listdir():

    if file.endswith(".txt"):
        file_path = f"{path}\{file}"
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for l in lines:
                #split data into list
                data = l.split()  
                #list for all video data  
                vid_info = data[:9] 
                #list for related video ids
                related_vid = data[9:]
                #insert values into VideoData SQL table
                try:
                    cur.execute("INSERT INTO VideoData (vidId, uploader, age, category, length, views, rate, ratings, comments)"
                       + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                         (vid_info[0], vid_info[1], int(vid_info[2]), vid_info[3], int(vid_info[4]), int(vid_info[5]), float(vid_info[6]), int(vid_info[7]), int(vid_info[8])) )    #str,str,int,str,int,int,float,int,int          
                except Exception as e:
                    print("Insert to VideoData failed!",e)
                conn.commit()
                #insert values into RelatedVid SQL table
                for x in related_vid:
                    try:
                        cur.execute("INSERT INTO RelatedVid (vidId, relatedId)"
                            + " VALUES (%s, %s)", (vid_info[0], x)) #str, str
                    except Exception as e:
                        print("Insert to RelatedVid failed!", e)
                    conn.commit()
cur.close()
conn.close()


