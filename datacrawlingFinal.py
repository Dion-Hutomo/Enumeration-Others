import tweepy
import re
import pandas
from textblob import TextBlob
# Pada program ini saya menggunakan bearer token untuk mengakses tweet
client = tweepy.Client('AAAAAAAAAAAAAAAAAAAAAELUVwEAAAAAlXh080nAcl0%2FVU7KulULytWhHHQ%3DLObPeKaM1IBEOgobpIO5Tarzp4FXA59swZYraD2Rw6O1x0qTAk')
# ditampung dengan variable tweets, akan digunakan function search_recent_tweets 
# untuk mencari tweet yang berhubungan dengan covid19 sampai batas 2 hari yang lalu 
# dan pada attempt untuk data crawling ini dicoba pada tanggal 19 sehingga end_timenya 
# tanggal 17 dengan total tweet yang ingin dihasilkan dibatasi jumlah 20
tweets = client.search_recent_tweets(query='#COVID19',end_time='2021-11-17T23:59:59.59+07:00',max_results=20)
tempPos = 0 # variable untuk menampung pernyataan positif
tempNeg = 0 # variable untuk menampung pernyataan negatif
data = []
print("")
print("list of tweets regarding Covid 19: ")
for tweet in tweets.data:
    text = tweet.text
    # pada line berikut, tweet yang dihasilkan akan dibersihkan dengan regular expression.
    cleanedTweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)"," ", text).split())
    print(cleanedTweets)

    # pada statement berikut Tweets yang sudah dibersihkan regex,
    # akan diukur polarity-nya sehingga dapat dilihat
    # apakah tweet bersifat positif atau negatif. 
    analysis = TextBlob(cleanedTweets)
    if(analysis.sentiment.polarity >= 0):
        polarity = 'positive'
        tempPos += 1 #jika statement positif maka akan ditambahkan 1 pada variabel
    elif(analysis.sentiment.polarity < 0):
        polarity = 'negative'
        tempNeg += 1 #sama jika statement dihitung negatif
    
    #isi dictionary
    dic = {}
    dic['Sentiment'] = polarity
    dic['Tweet'] = cleanedTweets
    dic['Polarity'] = analysis.sentiment.polarity
    data.append(dic)

#setelah dimasukkan ke list of dictionary, rapihkan dengan pandas menggunakan function Dataframe
datafile = pandas.DataFrame(data)
#datafile.to_csv('SentimentTwitter.csv')
print("")
print("Nilai Sentiment: ")
print(datafile)
print("")
print("Jumlah Statement Positif: ")
print(tempPos)
print("Jumlah Statement Negatif: ")
print(tempNeg)

# REFERENCE MATERIAL: Pertemuan Lec 6 November '21 + Tweepy documentation:https://docs.tweepy.org/en/latest/client.html