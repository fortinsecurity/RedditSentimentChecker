from textblob import TextBlob

texts = ["This movie is a piece of shit. Just a load of woke crap",
    "I love Keanu Reeves' performance though","i have no strong feelings one way or another","it was fine but i found it a bit boring."]

def getSentiment(text):
    resultSentiment = 0
    blob = TextBlob(text)
    for sentence in TextBlob(text).sentences:
        print(sentence, sentence.sentiment.polarity)
    return resultSentiment