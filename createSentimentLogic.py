'''
strategy: 
reddit api returns a list of articles given a subreddit and a query
loop through the articles and get the comments
store everything in database: one record per comment, with the relevant columns being: subreddit and topic
sentiment should only consider comments to articles, not the articles themselves (for now)

clientid: yI9vKDOvJduZHfGHFwzxVw
secret: 	_cZjCXrVM7H4j0As9HqrYs9NvyyddQ

https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

smarter way to use the reddit api: https://praw.readthedocs.io/en/latest/tutorials/comments.html

'''

'''
authentication to reddit api
'''

import requests, json, time
from textblob import TextBlob
import configparser

config = configparser.ConfigParser()
config.read("logincreds.ini")
print(config["default"]["user"])

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(config["default"]["client_id"], config["default"]["secret_token"])

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': config["default"]["username"],
        'password': config["default"]["password"]}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

TOKEN = ""
with open("authtoken.txt") as authfile:
    TOKEN = authfile.read()

# send our request for an OAuth token

res2 = requests.get('https://oauth.reddit.com/r/cyberpunkgame/comments/ydv2o3', headers=headers, params={"depth":"1"})
if res2.status_code != 200:
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']
    with open("authtoken.txt","w") as authfile:
        authfile.write(TOKEN)


# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests

""" res2 = requests.get('https://oauth.reddit.com/r/Ghost_in_the_Shell/search', headers=headers, params={"q":"motoko"})
f = open("temp.json","w")
f.write(json.dumps(res2.json(), indent=4))
f.close() """

# get comments for a specific post
'''
requires field "id": "yhrcvo"
needs to be in the right subreddit; articles found in the earlier step will actually be from different subreddits; in that case: "subreddit_name_prefixed": "r/cyberpunkgame"
the actual comment data is in: "body": "That's why I meant in spirit.\nToo bad there weren't many missions with both in the game... Especially that Cyberpsycho Gits Homage"
'''
""" res2 = requests.get('https://oauth.reddit.com/r/cyberpunkgame/comments/ydv2o3', headers=headers, params={"depth":"1"})
f = open("temp_comments.json","w")
f.write(json.dumps(res2.json(), indent=4))
f.close() """

'''
NLP
receives a string, breaks it into sentences and calculates a sentiment for each sentence. then sums the results and returns.

'''

def getSentiment(text):
    resultSentiment = []
    blob = TextBlob(text)
    for sentence in TextBlob(text).sentences:
        # print(sentence, sentence.sentiment.polarity)
        resultSentiment.append(sentence.sentiment.polarity)
    if len(resultSentiment) == 0:
        return 0
    else:
        return sum(resultSentiment)/len(resultSentiment)

def queryToDatabase(subreddit, query, limit=25):

    # list of articles to request in the next step (in order to get the comments). lists of the form: [acutalSubreddit, articleId]
    articles = []
    # list of comments: [acutalSubreddit, articleId,commentBody,sentiment]
    comments = []
    try:
        rawResultArticles = requests.get('https://oauth.reddit.com/r/'+subreddit+'/search', headers=headers, params={"q":query, "limit":str(limit+1)}).json()
        # test code
        """ f = open("temp_articles.json","w")
        f.write(json.dumps(rawResultArticles, indent=4))
        f.close() """

        for article in rawResultArticles["data"]["children"]:
            actualSubreddit = article["data"]["subreddit"]
            articleId = article["data"]["id"]
            articles.append([actualSubreddit,articleId])
        print(len(articles), " articles: ", articles)
    except Exception as er: 
        print(er)

    '''
    loop through the articles in order to get the comments. 
    we only look at first-level comments; we assume only first-level comments contain information on the sentiment of the article/topic itself. (Deeper levels contain sentiment on the first-level comments instead.)
    '''
    try:
        for index,article in enumerate(articles):
            print("crawling ", index+1, " out of ", len(articles), " articles...")
            rawResultComments = requests.get('https://oauth.reddit.com/r/'+article[0]+'/comments/'+article[1], headers=headers, params={"limit":str(limit+1)}).json()
            # test code
            """ f = open("temp_comments.json","w")
            f.write(json.dumps(rawResultComments, indent=4))
            f.close() """
            for comment in rawResultComments[1]["data"]["children"]:
                try:
                    commentBody = comment["data"]["body"]
                    comments.append([article[0],article[1],commentBody,getSentiment(commentBody)]) # should i trim the string?
                except KeyError:
                    continue
            time.sleep(2)
    except Exception as er:
        print("Error: " ,er)
    finally:
        # test code
        """ f = open("temp_results.json","w")
        f.write(json.dumps(comments, indent=4))
        f.close() """

        return comments

def totalSentimentForTopicAndSubreddit(comments):
    sentimentValues = [c[3] for c in comments]
    return sum(sentimentValues)/len(sentimentValues)

comments = queryToDatabase("CryptoCurrency","ethereum",3)
print(totalSentimentForTopicAndSubreddit(comments))

