from textblob import TextBlob
from newspaper import Article  # No need to change this import; newspaper3k uses the same module name
import nltk

# Manually download the required tokenizer if not already done
nltk.download('punkt')

# Insert the article URL
url = 'https://en.wikipedia.org/wiki/Happiness'

# Create an Article object
article = Article(url)

# Download and parse the article
article.download()
article.parse()

# Get the article text (full text, instead of summary)
text = article.text

# Use TextBlob or NLTK directly for sentiment analysis
blob = TextBlob(text)

# Perform sentiment analysis
sentiment = blob.sentiment.polarity
print("\nSentiment Polarity:", sentiment)
