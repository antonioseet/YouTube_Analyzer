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

    # To make testing a postgres connection a bit easier, when we know connection is successful, let user decide if they want to proceed.
    cont = input("Would you like to continue? (y/n): ")

    if(cont != 'y'):
        print("Ending session, see ya!")
        return
    
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

                    # Sometimes there are lines wihtout enough table data, continue will skip these.
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

                    # TODO: Create a video object, and set all the values from the list. related vids is last param.

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

def video(id, name, category, relatedVids):
    return

parser()