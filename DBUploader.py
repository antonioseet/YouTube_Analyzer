import os
import psycopg2

dbname = "415DBTest"
user = "postgres"
host = "localhost"
password = "TwilightOne1!"

connectString = "dbname='" + dbname + "' user='"+ user +"' host='"+ host +"' password='"+ password +"'"

def parser():

    # ask the user for path to folder containing crawl txt files, alternatively, replace getPath with your own path.
    path = getPath()
    os.chdir(path)

    try:
        #establish connection
        ## db, user, host, and password need to be updated for Azure db
        conn = psycopg2.connect(connectString)
    except:
        # Quit if connection is not successful.
        print('Unable to connect to the database!')
        return

    print("Connection Successful!")

    # To make testing a postgres connection a bit easier, when we know connection is successful, let user decide if they want to proceed.
    cont = input("Would you like to continue? (y/n): ")

    if(cont != 'y'):
        print("Ending session, see ya!")
        return
    
    cur = conn.cursor()

    testInput = "ly0dBk7ZZZ	smosh	157	Comedy	364	455551	4.77	10505	1246"
    vid_info = testInput.split()


    #check if tables have already been created, drop if so
    cur.execute("DROP TABLE IF EXISTS VideoData;")
    cur.execute("DROP TABLE IF EXISTS RelatedVid;")

    #create tables
    cur.execute("CREATE TABLE VideoData (vidID CHAR(11) PRIMARY KEY, uploader VARCHAR(30), age INTEGER, category VARCHAR(30), length INTEGER, views INTEGER, rate FLOAT(2), ratings INTEGER, comments INTEGER);")
    cur.execute("CREATE TABLE RelatedVid (vidID CHAR(11) PRIMARY KEY, relatedId CHAR(11));")

     #str,str,int,str,int,int,float,int,int   
    cur.execute("INSERT INTO VideoData (vidId, uploader, age, category, length, views, rate, ratings, comments)"
        + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (vid_info[0], vid_info[1], int(vid_info[2]), vid_info[3], int(vid_info[4]), int(vid_info[5]), float(vid_info[6]), int(vid_info[7]), int(vid_info[8])))

    conn.commit()


def getPath():
    print("What is the path of the csv files?")
    path = input("Enter folder path: ")
    return path


parser()