from praw import *
import os
import matplotlib.pyplot as plt
import configparser

CANDIDATES=[["Fiona","Carley"],["Rhys","Louis"]]
URL="https://www.reddit.com/r/telltale/comments/ggqwob/telltales_most_popular_character_fiona_vs_carley/"
OPEN_PERIOD=60*60*24*2
MIN_ACC_AGE=60*60*24*3

def init():
    if os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return Reddit(user_agent=config["LOGIN"]["user_agent"],client_id=config["LOGIN"]["id"],client_secret=config["LOGIN"]["secret"])
    else:
        raise FileNotFoundError("'config.ini' not found in root directory.")

def processReddit(choices):
    reddit = init()

    thread = reddit.submission(url=URL)
    comments = thread.comments
    comments.replace_more()
    comments = comments.list()
    comments.sort
    voters = set()
    # [[[choice[0],val],...]
    results = []
    for choice in choices:
        results.append([[x,0] for x in choice])

    comments.sort(key=lambda x: x.created_utc,reverse=True)

    for comment in comments:

        if  comment.author in voters or\
            comment.created_utc - comment.author.created_utc<MIN_ACC_AGE or\
            comment.created_utc> thread.created_utc +  OPEN_PERIOD:
            continue

        for i,choice in enumerate(choices):
            a = choice[0].lower() in comment.body.lower()
            b = choice[1].lower() in comment.body.lower()
            if a or b:
                if a and b:
                    continue
                if a:
                    results[i][0][1]+=1
                if b:
                    results[i][1][1]+=1
                voters.add(comment.author)

    return results

def graphIt(db):
    names = []
    vals = []
    for x,y in db:
        names.append(x[0])
        names.append(y[0])
        vals.append(x[1])
        vals.append(y[1])

    plt.bar(names,vals)
    plt.show()

def printIt(db):
    names = []
    vals = []
    for x,y in db:
        names.append(x[0])
        names.append(y[0])
        vals.append(x[1])
        vals.append(y[1])

    for i,name in enumerate(names):
        print(f"{name}: {vals[i]}")




def main():
    choices = CANDIDATES
    res = processReddit(choices)
    printIt(res)
    graphIt(res)

if __name__ == '__main__':
    main()
