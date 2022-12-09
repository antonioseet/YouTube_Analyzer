# pip install "pymongo[srv]"

from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "mongodb+srv://bag:Backpack!@teambag.ywpuiau.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    return client
  
def printResult(result):
    print(str(result['uploader']) + ' | ' + str(result['category']) + ' | ' + str(result['length']) + ' | ' + str(result['views']))

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
        results = db['VideoData']['videos'].aggregate([{'$group': {'_id': '$category', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 5}])
        return topCategoriesStrings(results)
# most popular - by views
    elif option == 1:
        results = db['VideoData']['videos'].aggregate([{'$sort' : {'views': -1}}, {'$limit': k}])
        return mostPopularStrings()
# top rated
    else:
        results = db['VideoData']['videos'].aggregate([{'$sort' : {'rate': -1, 'ratings': -1}}, {'$limit': k}])
        return topRatedStrings()
    
    return results
    
def topCategoriesStrings(messyList: list):
    results = list()
    for item in messyList:
        results.append(item['_id'])
    return results

def mostPopularStrings(messyList: list):
    results = list()
    for item in messyList:
        results.append(item['_id'])
    return results

def topRatedStrings(messyList: list):
    pass

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   

    # Get the database
    db = get_database()

    filter={'length': {'$gt': 0, '$lt': 1008}, 'category': 'Sports'}

    #result contains a Cursor object
    results = getTopKResults(5, 1)#db['VideoData']['videos'].find(filter=filter)

    for result in results:
        print(result)

    print('__________')