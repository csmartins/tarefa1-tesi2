import os
import sys
import math
import nltk
from nltk.corpus import stopwords

path_output = "output"
path_episodes_cleaned = "cleaned_episodes"
word_frequency = {}
documents_count = 0
all_documents = []

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

def count_frequency(path_episode, words_count):
	for word in words_count.keys():
		if word in word_frequency.keys():
			word_frequency[word].append((path_episode, words_count[word]))
		else:
			word_frequency[word] = [(path_episode, words_count[word])]

def calc_idf():
	inverse_document_frequency = {}
	for word in word_frequency.keys():
		df = len(word_frequency[word])

		N = documents_count * 1.0 #convertendo pra decimal para prevenir math domain error
		#print "N =", N
		#print "df de", word, "=", df
		idf = math.log(N/df)
		
		inverse_document_frequency[word] = idf
	return inverse_document_frequency

def calc_tf_idf(idf):
	tf_idf = {}
	for word in word_frequency.keys():
		tf_idf[word] = {}
		for tf in word_frequency[word]:
			tf_idf[word][tf[0]] = tf[1]*idf[word]
	return tf_idf

def score(query, tf_idf):
	scores = []
	words = nltk.word_tokenize(query)

	for document in all_documents:
		score = 0
		for word in words:
			if word in word_frequency.keys():
				score+= tf_idf[word].get(document,0)
		scores.append((document, score))
	return scores

def get_best_scores(scores):
	sorted_scores = sorted(scores, key=lambda scor: scor[1])
	new_sorted_scores = []
	for s_s in sorted_scores:
		if s_s[1] != 0:
			new_sorted_scores.append(s_s)

	return new_sorted_scores

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
			global documents_count
			documents_count += len(files)
			for episode in files:
				path_episode = path_season + episode
				all_documents.append(path_episode)
				with open(path_episode) as f:
					full_content = f.read()
					words_count = count_words(full_content)
					
					count_frequency(path_episode, words_count)
	
	idf = calc_idf()
	tf_idf = calc_tf_idf(idf)
	
	query = "Eddard Stark Death"
	scores = score(query, tf_idf)
	
	final_score = get_best_scores(scores)

	print final_score	
if __name__ == "__main__":
	do_main()
