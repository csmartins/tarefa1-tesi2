import os
import sys
import csv 
import re
import nltk
from nltk.corpus import stopwords

path_output = "output"
path_episodes_cleaned = "cleaned_episodes"
word_frequence = {}

def create_diretory(path):
    if not (os.path.isdir(path)):
		os.mkdir(path)

def filter_words(words):
	filtered_words = [word for word in words if word not in stopwords.words('english')]
	return filtered_words

def get_tokens(sent):
	words_tokenized = filter_words(nltk.word_tokenize(sent))
	return words_tokenized

def update_dict(x, y):
	z = x.copy()
	z.update(y)
	return z

def count_words(full_content):
	sentences = nltk.sent_tokenize(full_content.decode('utf-8'))
	words_count = {}
	words_dict = {}
	for sent in sentences:
		words_tokenized = get_tokens(sent)

		for key in words_tokenized:
			if key not in words_dict.keys():
				words_dict[key] = 0

		for token in words_tokenized:
			words_dict[token]+= 1
			if token in words_count.keys():
				words_count[token]+= words_dict[token]
			else:
				words_count[token] = words_dict[token]
		words_count = update_dict(words_count, words_dict)
	return words_count

def do_main():
    full_content = ""

    seasons = os.listdir(path_episodes_cleaned)
    create_diretory(path_output)

    for season in seasons:
    	if "season" in season:
            path_season = path_episodes_cleaned+'/'+season+'/'
            files = os.listdir(path_season)
            path_season_output = path_output+'/'+season+'/'
            create_diretory(path_season_output)

            for episode in files:
				path_episode = path_season + episode
				with open(path_episode) as f:
					full_content = f.read()
					words_count = count_words(full_content)
					
					for word in words_count.keys():
						if word in word_frequence.keys():
							word_frequence[word].append((path_episode, words_count[word]))
						else:
							word_frequence[word] = [(path_episode, words_count[word])]
		
if __name__ == "__main__":
	do_main()
	print word_frequence['Cersei']
