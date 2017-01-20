import math
def average(x):
    if len(x) > 0:
        return float(sum(x)) / len(x)
    else:
        return False
def pearson(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    if x == y:
        return 1
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0

    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y

        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff
    if math.sqrt(xdiff2 * ydiff2)==0:
        return 0
    else:
        return diffprod / math.sqrt(xdiff2 * ydiff2)
#For testing accuracy of memory based filtering
        ratingDictionary= {}
        movieSets=[]
        for x in range(0,len(train_data)):
            movieSets.append((str(train_data[x]['user_id']),str(train_data[x]['movie_id'])))
            if train_data[x]['user_id'] in ratingDictionary:
                ratingDictionary[train_data[x]['user_id']].append({train_data[x]['movie_id']:y_train[x]})
            else:
                ratingDictionary[train_data[x]['user_id']] = [{train_data[x]['movie_id']:y_train[x]}]
        countIndex=0;
        predictions=[]
        for user in test_users:
            userratings=[]
            similarusers= {}
            for userrating in ratingDictionary[user]:
                for key in userrating:
                    userratings.append(userrating[key])
            for userTwo in ratingDictionary:
                if str(user) != userTwo and (userTwo,str(test_items[countIndex])) in movieSets:
                    movieListOne= []
                    movieListTwo=[]
                    for rating in ratingDictionary[user]:
                        for movieId in rating:
                            for ratingTwo in ratingDictionary[userTwo]:
                                for movieTwo in ratingTwo:
                                    if movieId == movieTwo:
                                        movieListOne.append(rating[movieId])
                                        movieListTwo.append(ratingTwo[movieTwo])
                                        continue
                    if (len(movieListOne)>3):
                        similarity=pearson(movieListOne,movieListTwo)
                        if similarity>0.6:
                            similarusers[userTwo]=similarity
                            similarusers[userTwo+'list']=movieListTwo
            teller = 0
            nevner = 0
            for simuser in similarusers:
                if isinstance(similarusers[simuser],int):

                    nevner = nevner + similarusers[simuser]
                    for movie in ratingDictionary[simuser]:
                        if test_items[countIndex] in movie:

                            teller=teller+similarusers[simuser]*(movie[test_items[countIndex]]-average(similarusers[simuser+'list']))
                            continue
            if nevner==0:
                predictions.append(average(userratings))
            else:
                predictions.append(average(userratings)+teller/nevner)
            countIndex=countIndex+1;
