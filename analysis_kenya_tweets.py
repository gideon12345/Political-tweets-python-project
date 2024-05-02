import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import re
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import dbconn

# Ensure NLTK resources are available
nltk.download('vader_lexicon')

# Connect to MySQL database
engine = create_engine('mysql+mysqlconnector://root:@localhost/kenyan_tweets')

# Load data from MySQL into a DataFrame
query = "SELECT * FROM tweets"
df = pd.read_sql(query, engine)

# Tokenize and clean tweets
def clean_tweet(tweet):
    cleaned_tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet)
    cleaned_tweet = re.sub(r'\W', ' ', cleaned_tweet)
    cleaned_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', cleaned_tweet)
    cleaned_tweet = re.sub(r'\s+', ' ', cleaned_tweet)
    return cleaned_tweet

# Analyze sentiment of tweets
def analyze_sentiment(tweet):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(tweet)
    return sentiment_score

# Word frequency analysis
def word_frequency_analysis(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts

# Apply cleaning, sentiment analysis, and word frequency analysis to each tweet
df['cleaned_text'] = df['text'].apply(clean_tweet)
df['sentiment_score'] = df['cleaned_text'].apply(analyze_sentiment)
df['word_counts'] = df['cleaned_text'].apply(word_frequency_analysis)

# Display results
print("Average sentiment score:")
print(df['sentiment_score'].apply(lambda x: x['compound']).mean())

print("\nMost common words:")
word_counts_total = Counter()
for counts in df['word_counts']:
    word_counts_total += counts
for word, count in word_counts_total.most_common(10):
    conn =dbconn.connect_to_database()
    cursor =conn.cursor()

    #insert data to the analysis_details table
    cursor.execute("INSERT INTO analysis_details (analysis_id, word, count) VALUES (%s, %s, %s)", (1, word,count))
    conn.commit() 
    #print the data to the screen
    print(f"{word}: {count}")
