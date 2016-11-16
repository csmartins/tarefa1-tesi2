import os
import sys
import math
import nltk
from nltk.corpus import stopwords

path_output = "output"

word_frequency = {}
documents_count = 0
all_documents = []
punctuation = [".", ",", "/", "(", ")", "'", "?", "!"]

def create_diretory(path):
    if not (os.path.isdir(path)):
		os.mkdir(path)

def filter_words(words):
	filtered_words = [word for word in words if word not in stopwords.words('english') and word not in punctuation]
	return filtered_words

def get_tokens(sent):
	words_tokenized = filter_words(nltk.word_tokenize(sent))
	return words_tokenized

def update_dict(x, y):
	z = x.copy()
	z.update(y)
	return z

'''Conta o numero de palavras de um conteudo e guarda a quantidade num dicionario onde a chave
eh a palavra e o valor eh o numero de vezes que aparece.'''
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

'''Adiciona ao dicionario geral a ocorrencia de uma palavra em um episodio. Cada elemento do dict
tem como chave a palavra e o valor uma lista. Cada elemento da lista eh composto por uma tupla onde
o primeiro elemento eh o nome do arquivo e o segundo eh o valor da ocorrencia daquela palavra no documento.'''
def count_frequency(path_episode, words_count):
	for word in words_count.keys():
		if word in word_frequency.keys():
			word_frequency[word].append((path_episode, words_count[word]))
		else:
			word_frequency[word] = [(path_episode, words_count[word])]

'''Calcula o valor de idf para cada palavra do dict de frequencia de palavras(word_frequency).
Lembrando que o valor desse dict eh uma lista de tuplas onde cada uma delas junta o nome do episodio
e a quantidade de vezes que essa palavra ocorre.'''
def calc_idf():
	inverse_document_frequency = {}
	for word in word_frequency.keys():
		#df = numero de documentos em que uma palavra aparece
		df = len(word_frequency[word])

		N = documents_count * 1.0 #convertendo pra decimal para prevenir math domain error
		#print "N =", N
		#print "df de", word, "=", df
		idf = math.log(N/df)
		
		inverse_document_frequency[word] = idf
	return inverse_document_frequency

'''Constroi a matriz de tf-idf onde a chave eh uma palavra e o valor tambem é um dict. Esse dict interno
tem como chave o nome do episodio e valor o tf*idf'''
def calc_tf_idf(idf):
	tf_idf = {}
	for word in word_frequency.keys():
		tf_idf[word] = {}
		for tf in word_frequency[word]:
			tf_idf[word][tf[0]] = tf[1]*idf[word]
	return tf_idf

'''Calcula o score de cada documento percorrendo cada palavra do dict de tf-idf somando os valores
de cada elemento do mesmo'''
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

'''Ordena os scores e retorna o 5 maiores'''
def get_best_scores(scores):
	sorted_scores = sorted(scores, key=lambda scor: scor[1], reverse=True)
	new_sorted_scores = []
	for s_s in sorted_scores:
		if s_s[1] != 0:
			new_sorted_scores.append(s_s)

	return new_sorted_scores[:5]

def do_main():
	if len(sys.argv) < 3:
		print "Insuficient number of arguments."
		print "Expected: python tf-idf.py <query> <path_to_episodes>"
		return

	full_content = ""
	query = sys.argv[1]
	path_episodes = sys.argv[2]
	seasons = os.listdir(path_episodes)
	create_diretory(path_output)
	
	for season in seasons:
		if "season" in season:
			path_season = path_episodes+'/'+season+'/'
			files = os.listdir(path_season)
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
	
	scores = score(query, tf_idf)
	
	final_score = get_best_scores(scores)

	print "Most relevant episodes, sorted by score:"
	for fc in final_score:
		print fc[0], '-', fc[1]
if __name__ == "__main__":
	do_main()
