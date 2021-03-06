from praw import *
import os
import matplotlib.pyplot as plt
import configparser
import numpy as np
import matplotlib.ticker as mtick
import logging

CANDIDATES=[[["Clementine","Clem"],["Lee"]]]
URL="https://www.reddit.com/r/telltale/comments/gmy3qz/telltales_most_popular_character_the_final_match/"
OPEN_PERIOD=60*60*24*2
MIN_ACC_AGE=60*60*24*10

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
        results.append([[x[0],0] for x in choice])

    comments.sort(key=lambda x: x.created_utc,reverse=False)

    csvData=[]

    for comment in comments:
        if comment.author in voters:
            if not any([x.lower() in comment.body.lower() for x in (choice[0] + choice[1])]):
                continue
            print(f"Shame on {comment.author.name}\nComment: '{comment.body}'")
            print(f"Reason: Already voted")
            print("")
            continue
        if thread.created_utc + OPEN_PERIOD - comment.author.created_utc<MIN_ACC_AGE:
            print(f"Shame on {comment.author.name}\nComment: '{comment.body}'")
            print(f"Reason: Account not old enough")
            print("")
            continue
        if comment.created_utc> thread.created_utc +  OPEN_PERIOD:
            print(f"Shame on {comment.author.name}\nComment: '{comment.body}'")
            print(f"Reason: Vote window closed")
            print("")
            continue
        # if len(list(comment.author.comments.new(limit=2))) == 1:
        #     print(f"Shame on {comment.author.name}\nComment: '{comment.body}'")
        #     print(f"Reason: Only has one comment")
        #     print("")
        #     continue

        voteString = [str(comment.author)] + [""]*len(choices)
        voted = False
        for i,choice in enumerate(choices):
            a = any([x.lower() in comment.body.lower() for x in choice[0]])
            b = any([x.lower() in comment.body.lower() for x in choice[1]])
            if a or b:
                if a and b:
                    continue
                if a:
                    voteString[i+1]=choice[0][0]
                    results[i][0][1]+=1
                if b:
                    voteString[i+1]=choice[1][0]
                    results[i][1][1]+=1
                voted=True
                voters.add(comment.author)
        if voted:
            csvData.append(";".join(voteString+[comment.body.replace("\n"," ")]))

    with open("data.csv","wb") as out:
        out.write("\n".join(["User;"+";".join([f"Choice {i+1}" for i in range(len(choices))])+";Comment"] + sorted(csvData,key=lambda x:x.lower())).encode("utf8"))

    return results

def graphIt(db):
    names = []
    vals = []
    for x,y in db:
        names.append(x[0])
        names.append(y[0])
        vals.append(x[1])
        vals.append(y[1])

    for i in range(0,len(vals),2):
        p1 = vals[i]/(vals[i]+vals[i+1])
        p2 = vals[i+1]/(vals[i]+vals[i+1])
        vals[i] = p1
        vals[i+1] = p2

    N = len(db)
    fig, ax = plt.subplots()

    ind = np.arange(N)    # the x locations for the groups
    width = 0.35         # the width of the bars
    p1 = ax.bar(ind, vals[::2], width)

    p2 = ax.bar(ind + width, vals[1::2], width)

    ax.set_title('Vote Results')
    ax.set_xticks(ind + width / 2)
    labelList = []
    for i in range(0,len(names),2):
        labelList.append(f"{names[i]}/{names[i+1]}")
    ax.set_xticklabels(labelList)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    ax.autoscale_view()

    plt.show()

def printIt(db):
    names = []
    vals = []
    for x,y in db:
        names.append(x[0])
        names.append(y[0])
        vals.append(x[1])
        vals.append(y[1])

    out = open("results.txt","w")
    for i in range(0,len(names),2):
        percentStr = "{:.2%}".format(vals[i]/(vals[i]+vals[i+1]))
        print(f"{names[i]}: {vals[i]} ({percentStr})")
        percentStr = "{:.2%}".format(vals[i+1]/(vals[i]+vals[i+1]))
        print(f"{names[i+1]}: {vals[i+1]} ({percentStr})")
        print("")


        percentStr = "{:.2%}".format(vals[i]/(vals[i]+vals[i+1]))
        print(f"{names[i]}: {vals[i]} ({percentStr})",file=out)
        percentStr = "{:.2%}".format(vals[i+1]/(vals[i]+vals[i+1]))
        print(f"{names[i+1]}: {vals[i+1]} ({percentStr})",file=out)
        print("",file=out)
    out.close()




def main():
    choices = CANDIDATES
    res = processReddit(choices)
    printIt(res)
    graphIt(res)

if __name__ == '__main__':
    main()
