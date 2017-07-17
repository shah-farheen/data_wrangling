#1
def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$match": {"name": {"$exists": True, "$ne": "NULL"}}},
    {"$group": {"_id": "$name", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 1}]
    return pipeline


#2
def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$match": {"country": "India", "lon":{"$gt": 75, "$lt": 80}}},
    {"$unwind": "$isPartOf"},
    {"$group": {"_id": "$isPartOf", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 1}]
    return pipeline


#3
def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$unwind": "$isPartOf"},
    {"$group": {"_id": {"isPartOf": "$isPartOf", "country": "$country"}, "ravg": {"$avg": "$population"}}},
    {"$group": {"_id": "$_id.country", "avgRegionalPopulation": {"$avg": "$ravg"}}}]
    return pipeline
