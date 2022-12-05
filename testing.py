from doctest import testfile


# Function that fixes the spaces between categories like "News & politics", returns an array ready for postgres table
def fixSplit(lineArray):
    category = lineArray[3] + lineArray[4] + lineArray[5]
    newArray = lineArray[:3] + category.split() + lineArray[6:]
    return newArray

line = "49hC9TpP_rY	JohnMcCaindotcom	1257	News & Politics	33	267795	2.38	1017	1700	mm9IUfPZsX8	Au0eBx05Zxc	4yU2-LTFLf0	Z0cNqtUtufo	390STYaUebM	D5QKyUvZv5A	9-HfSY6LEqY	sONerncAkQ4	2EDOgG-GdPw	K2X8SVZNUrY	Fw2KxSWs0hA	gO35AwPtn9o	_1brJ8tuN8w	2hEzGKQLmU4	f2bGDgfHZvQ	gMTSIWXZ8ts	mTSuHweJXxc	f-mdHN24iS0	kD3LTtYXl2A	HqlyqG6tNh0"

lineArray = line.split()

# If an '&' is found in results, we must merge the category into one. {News, &, politics} -> {News&Politics} (& will always be found in the 4th spot)
if(lineArray[4] == '&'):
    lineArray = fixSplit(lineArray)

#list for all video data  
vid_info = lineArray[:8] 
#list for related video ids
related_vid = lineArray[8:]

for i in range(len(vid_info)):
    print(str(i) + " | " + vid_info[i])

    #str,str,int,str,int,int,float,int
print("INSERT INTO VideoData ('{}', '{}', {}, '{}', {}, {}, {}, {})".format(vid_info[0], vid_info[1], int(vid_info[2]), vid_info[3], int(vid_info[4]),int(vid_info[5]), float(vid_info[6]), int(vid_info[7])))

