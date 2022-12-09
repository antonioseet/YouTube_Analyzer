# pip install "pymongo[srv]"
from pymongo import MongoClient

gmaxView = 18291006
gmaxLen = 4597587

def get_database():
    CONNECTION_STRING = "mongodb+srv://bag:Backpack!@teambag.ywpuiau.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    return client

def getCategoriesList():
    db = get_database()
    results = db['VideoData']['videos'].distinct('category')
    categoryList = list()

    for result in results:
        categoryList.append(result)

    return categoryList

def getTopKResults(k: int, option: int) -> list:
    db = get_database()
    results = list()
# top categories
    if option == 0:
        results = db['VideoData']['videos'].aggregate([{'$group': {'_id': '$category', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': int(k)}])
        return topCategoriesStrings(results)
# most popular - by views
    elif option == 1:
        results = db['VideoData']['videos'].aggregate([{'$sort' : {'views': -1}}, {'$limit': int(k)}])
        return mostPopularStrings(results)
# top rated
    else:
        results = db['VideoData']['videos'].aggregate([{'$sort' : {'rate': -1, 'ratings': -1}}, {'$limit': int(k)}])
        return topRatedStrings(results)

    return results
    
def getVideoResults(minView: int, maxView: int, minLen: int, maxLen: int, minrate: int, maxrate: int, category: str):
    db = get_database()
    results = list()

    if maxView == 0:
        maxView = gmaxView

    if maxLen == 0:
        maxLen = gmaxLen
    
    filter={
    'views': {
        '$gt': minView, 
        '$lt': maxView
    }, 
    'rate': {
        '$gt': minrate, 
        '$lt': maxrate
    }, 
    'length': {
        '$gt': minLen, 
        '$lt': maxLen
    }, 
    'category': category}

    results = db['VideoData']['videos'].find(filter=filter)
    listRes = list(results)
    print("Method results: " + str(list))

    return videoResultsStrings(listRes)

def getFrequencyResults(minView: int, maxView: int, minLen: int, maxLen: int, minrate: int, maxrate: int, category: str):
    db = get_database()
    results = list()

    if maxView == 0:
        maxView = gmaxView

    if maxLen == 0:
        maxLen = gmaxLen
    
    filter={
    'views': {
        '$gt': minView, 
        '$lt': maxView
    }, 
    'rate': {
        '$gt': minrate, 
        '$lt': maxrate
    }, 
    'length': {
        '$gt': minLen, 
        '$lt': maxLen
    }, 
    'category': category}

    results = db['VideoData']['videos'].find(filter=filter)
    count = len(list(results))
    return count
    
def topCategoriesStrings(messyList: list):
    results = list()
    for item in messyList:
        results.append(str(item['_id']) + " | use count: " + str(item['count']))
    return results

def mostPopularStrings(messyList: list):
    results = list()
    for item in messyList:
        formatted = "{:,}".format(item['views'])
        results.append(str(item['uploader']) + " uploaded " + str(item['vidid'])+ " and received "  + str(formatted) + " views.")
    return results

def topRatedStrings(messyList: list):
    results = list()
    for item in messyList:
        results.append(str(item['vidid']) + " uploaded by " + str(item['uploader'])+ ", received "  + str(item['ratings']) + " ratings and scored: " + str(item['rate']))
    return results

def videoResultsStrings(messyList: list):
    results = list()
    for item in messyList:
        results.append(str(item['vidid']) + " uploaded by " + str(item['uploader'])+ ", received "  + str(item['views']) + " views and scored: " + str(item['rate']))
    return results

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   

    # Get the database
    db = get_database()

    #results = getTopKResults(10, 2)#db['VideoData']['videos'].find(filter=filter)
    result = getVideoResults(200000, 1000000, 0, 1000, 4, 5, 'Sports')
    print(result)
    #for i in result:
    #    print(i)

    print('__________')