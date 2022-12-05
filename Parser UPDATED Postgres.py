import os
import psycopg2

dbname = "415DBTest"
user = "postgres"
host = "localhost"
password = "PWD"

## Remember to add double forward slash \\ or use the provided "getPath()" method to input it yourself.
folderPath = "C:\\Users\\aabar\\Desktop\\Code Bench\\Python\\parser"


def parser():

    # ask the user for path to folder containing crawl txt files, alternatively, replace getPath with your own path.
    path = folderPath
    os.chdir(path)

    try:
        #establish connection
        ## db, user, host, and password need to be updated for Azure db?
        ### DO NOT CHANGE, update your changes above only! ###
        connectString = "dbname='" + dbname + "' user='"+ user +"' host='"+ host +"' password='"+ password +"'"
        conn = psycopg2.connect(connectString)
    except:
        # Quit if connection is not successful.
        print('Unable to connect to the database!')
        return

    print("Connection to DB Successful!")

    # To make testing a postgres connection a bit easier, when we know connection is successful, let user decide if they want to proceed.
    cont = input("Would you like to continue? (y/n): ")

    if(cont != 'y'):
        print("Ending session, see ya!")
        return
    
    cur = conn.cursor()

    # check if tables have already been created, drop if so
    cur.execute("DROP TABLE IF EXISTS videodata;")
    cur.execute("DROP TABLE IF EXISTS relatedvideos;")

    # create tables
    cur.execute("CREATE TABLE videodata (vidID CHAR(11) PRIMARY KEY, uploader VARCHAR(30), age INTEGER, category VARCHAR(30), length INTEGER, views INTEGER, rate FLOAT(2), ratings INTEGER, comments INTEGER);")
    cur.execute("CREATE TABLE relatedvideos (vidID CHAR(11), relatedId CHAR(11));")

    for file in os.listdir():

        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            with open(file_path, 'r') as f:
                lines = f.readlines()

                # variables to get progress output per file
                totalLines = len(lines)
                currentLineIndex = 0
                prevPercent = 0

                for line in lines:
                    #split data into list
                    lineArray = line.split()

                    # Sometimes there are lines wihtout enough data, skip these.
                    if(len(lineArray) < 8):
                        continue

                    # Use this input to stop at each line, press enter to insert next item. uncomment to run it all with progress reporting.
                    #yo = input("Line Break: " + str(lineArray))

                    # If an '&' is found in results, we must merge the category into one. {News, &, politics} -> {News&Politics} (& will always be found in the 4th spot)
                    if(lineArray[4] == '&'):
                        lineArray = fixSplit(lineArray)

                    #list for all video data  
                    vid_info = lineArray[:9] 
                    #list for related video ids
                    related_vid = lineArray[9:]

                    #insert values into VideoData SQL table
                    try:
                        #str,str,int,str,int,int,float,int,int
                        commandStr = "INSERT INTO videodata (vidId, uploader, age, category, length, views, rate, ratings, comments)"+ "VALUES ('{}', '{}', {}, '{}', {}, {}, {}, {}, {})".format(vid_info[0], vid_info[1], int(vid_info[2]), vid_info[3], int(vid_info[4]), int(vid_info[5]), float(vid_info[6]), int(vid_info[7]), int(vid_info[8]))

                        cur.execute(commandStr)
                    except Exception as e:
                        print("Insert to videodata failed!",e)

                    conn.commit()

                    #insert values into relatedvideos SQL table
                    for x in related_vid:
                        try:
                            cur.execute("INSERT INTO relatedvideos (vidId, relatedId)"
                                + " VALUES (%s, %s)", (vid_info[0], x)) #str, str
                        except Exception as e:
                            print("Insert to relatedvideos failed!", e)
                        conn.commit()

                    # Determine to print progress report once the percent has changed.
                    percent = progress(currentLineIndex, totalLines)
                    if(prevPercent != percent):
                        print("Processing: " + file + " | " + str(percent) + "%")
                        prevPercent = percent
                        
                    currentLineIndex += 1

    cur.close()
    conn.close()
    print("100% COMPLETE!!!")

def getPath():
    print("What is the path of the txt files?")
    path = input("Enter folder path (exclude quoteation marks): ")
    print(path)
    return path

# Function that fixes the spaces between categories like "News & politics", returns an array ready for postgres table
def fixSplit(lineArray):
    category = lineArray[3] + lineArray[4] + lineArray[5]
    newArray = lineArray[:3] + category.split() + lineArray[6:11]
    return newArray

def progress(current, total):
    percentDone = int((current/total) * 100)
    return percentDone

parser()