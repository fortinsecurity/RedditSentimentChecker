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

import requests, json

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('yI9vKDOvJduZHfGHFwzxVw', '_cZjCXrVM7H4j0As9HqrYs9NvyyddQ')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'anonintheshell',
        'password': '!QAY2wsx'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

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

def queryToDatabase(subreddit, query):
    # list of articles to request in the next step (in order to get the comments). lists of the form: [acutalSubreddit, articleId]
    articles = []
    # list of comments: [acutalSubreddit, articleId,commentBody]
    comments = []
    try:
        rawResultArticles = requests.get('https://oauth.reddit.com/r/'+subreddit+'/search', headers=headers, params={"q":query}).json()
        # test code
        f = open("temp_articles.json","w")
        f.write(json.dumps(rawResultArticles, indent=4))
        f.close()

        for article in rawResultArticles["data"]["children"]:
            actualSubreddit = article["data"]["subreddit"]
            articleId = article["data"]["id"]
            articles.append([actualSubreddit,articleId])
    except Exception as er: 
        print(er)

    '''
    loop through the articles in order to get the comments. 
    we only look at first-level comments; we assume only first-level comments contain information on the sentiment of the article/topic itself. (Deeper levels contain sentiment on the first-level comments instead.)
    '''
    try:
        for article in articles:
            rawResultComments = requests.get('https://oauth.reddit.com/r/'+article[0]+'/comments/'+article[1], headers=headers).json()
            # test code
            f = open("temp_comments.json","w")
            f.write(json.dumps(rawResultComments, indent=4))
            f.close()
            for comment in rawResultComments[1]["data"]["children"]:
                commentBody = comment["data"]["body"]
                comments.append([article[0],article[1],commentBody])
    except Exception as er:
        print("Error: " ,er)
    finally:
        # test code
        f = open("temp_results.json","w")
        f.write(json.dumps(comments, indent=4))
        f.close()

        return comments

print(queryToDatabase("Ghost_in_the_Shell","motoko"))