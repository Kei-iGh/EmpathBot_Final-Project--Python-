import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment, word_tokenize
nltk.download('vader_lexicon')
nltk.download('punkt')
import pandas as pd
from datetime import date
import time
today = date.today()
login = "chatbotowner"

#tokonizer will be used later for splitting a large text into sentences
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


#reading the created xlsx file as a dataframe
df_of_chat_data = pd.read_excel(f"{today}_{login}_chat.xlsx")


#getting all the values in the "message" column 
df_of_chat_data["message"] = df_of_chat_data["message"].astype(str)
list_of_df = df_of_chat_data['message'].tolist()


#deleting all the nan values
list_of_df2 = [i for i in list_of_df if str(i) != 'nan']

#print(list_of_df2)


#extracting the values from the list and putting them into a sting 
text_form = '." '.join([str(i) for i in list_of_df2])

#print(text_form)


#splitting the text into paragraphs (sentences) for an easier understanding
sentences = tokenizer.tokenize(text_form)

text_final = '. '.join([str(sentence) for sentence in sentences])

#print(text_final)


#using sentiment analyzer to get the polarity scores for the text
sentiment = SentimentIntensityAnalyzer()

scores = sentiment.polarity_scores(text_final)

#counting unique users who have chatted during a single stream 
percent_of_unique_users = round(len(pd.unique(df_of_chat_data['username'])) * 100 / len(df_of_chat_data['username']), 2)

def score(ascore):
	negative = round(ascore["neg"] * 100, 2)
	positive = round(ascore["pos"] * 100, 2)
	neutural = round(ascore["neu"] * 100, 2)

	return (f"Today your chat was {negative}% negative, {positive}% positive and {neutural}% neutural. The percentage of unique chatters is {percent_of_unique_users}%")


finalscores = score(scores)

print(finalscores)
