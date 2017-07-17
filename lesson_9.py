#10
def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$match": {"user.time_zone": "Brasilia", "user.statuses_count": {"$gte": 100}}},
    {"$project": {"followers": "$user.followers_count", "screen_name": "$user.screen_name", "tweets": "$user.statuses_count"}},
    {"$sort": {"followers" : -1}}, {"$limit": 1}]
    return pipeline

#12
def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$match": {"country": "India"}},
    {"$unwind": "$isPartOf"},
    {"$group": {"_id": "$isPartOf", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 1}]
    return pipeline

#14
def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$group": {"_id": "$user.screen_name",
    "count": {"$sum": 1}, "tweet_texts": {"$push": "$text"}}},
    {"$sort": {"count": -1}},
    {"$limit": 5}]
    return pipeline


#16
def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$match": {"country": "India"}},
    {"$unwind": "$isPartOf"},
    {"$group": {"_id": "$isPartOf", "ravg": {"$avg": "$population"}}},
    {"$group": {"_id": "Inida", "avg": {"$avg": "$ravg"}}}]
    return pipeline
