# import pandas as pd
# import string
# from collections import Counter
# import matplotlib.pyplot as plt
#

import pandas as pd
import string
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px

# Load tweets from CSV file
def load_tweets_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df['Text'].tolist()  # Focus on the 'Text' column

# Reading text from CSV
tweets = load_tweets_from_csv('C:\\Users\\upend\\Downloads\\tempCSV.csv')
text = " ".join(tweets)

# Converting to lowercase
lower_case = text.lower()

# Removing punctuations
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

# Splitting text into words
tokenized_words = cleaned_text.split()

# Define stop words (add your stop words here)
stop_words = set(['the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'is', 'are'])

# Removing stop words from the tokenized words list
final_words = [word for word in tokenized_words if word not in stop_words]

# Get emotions text with word frequency
emotion_word_freq = Counter()
with open('emotions.txt', 'r') as file:
    for line in file:
        clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
        try:
            word, emotion = clear_line.split(':')
            if word in final_words:
                emotion_word_freq[emotion] += 1
        except ValueError:
            continue  # Skip lines that don't have a valid format

# Prepare data for Sankey diagram
total_responses = sum(emotion_word_freq.values())
emotions = list(emotion_word_freq.keys())

# Create a color scale
color_scale = px.colors.qualitative.Pastel

# Create Sankey diagram data
source = [0] * len(emotions)
target = list(range(1, len(emotions) + 1))
value = list(emotion_word_freq.values())
label = ['Total Responses'] + emotions

# Create links and nodes
link = {
    'source': source,
    'target': target,
    'value': value,
    'color': [color_scale[i % len(color_scale)] for i in range(len(emotions))]
}
node = {
    'label': label,
    'pad': 15,
    'thickness': 20,
    'color': ['#888888'] + [color_scale[i % len(color_scale)] for i in range(len(emotions))]
}

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=node,
    link=link
)])

# Update layout
fig.update_layout(
    title_text="Tweet Sentiment Analysis",
    font_size=10,
    height=600,
    width=1000
)

# Show the plot
fig.show()

# Save the Sankey diagram
fig.write_image("tweet_sentiment_sankey_color.png")

# # Load tweets from CSV file
# def load_tweets_from_csv(file_path):
#     df = pd.read_csv(file_path)
#     return df['Text'].tolist()  # Focus on the 'Text' column
#
# # Reading text from CSV
# tweets = load_tweets_from_csv('C:\\Users\\upend\\Downloads\\tempCSV.csv')
# text = " ".join(tweets)
#
# # Converting to lowercase
# lower_case = text.lower()
#
# # Removing punctuations
# cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
#
# # Splitting text into words
# tokenized_words = cleaned_text.split()
#
# # Define stop words
# stop_words = set([...])  # Add your stop words here
#
# # Removing stop words and handling frequencies
# final_words = [word for word in tokenized_words if word not in stop_words]
#
# # Get emotions text with word frequency
# emotion_list = []
# emotion_word_freq = Counter()
# with open('emotions.txt', 'r') as file:
#     for line in file:
#         clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
#         word, emotion = clear_line.split(':')
#         if word in final_words:
#             emotion_list.append(emotion)
#             emotion_word_freq[emotion] += 1
#
# # Pie Chart Visualization
# labels = list(emotion_word_freq.keys())
# sizes = list(emotion_word_freq.values())
# colors = plt.cm.viridis(range(len(labels)))  # Using the same colormap for consistency
#
# plt.figure(figsize=(10, 7))
# plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
# plt.title('Emotions Distribution in Tweets')
# plt.savefig('emotion_pie_chart.png')
# plt.show()
