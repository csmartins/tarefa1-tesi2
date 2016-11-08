import os
import sys
import csv 
import re
from nltk import tokenize
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import brown

'''Variaveis globais'''
path_episodes_output = "output"
path_entities_csv = "output/entities"
csv_name = "/related_entities.csv"

'''Responsavel por escrever em um csv todas as relacoes entre entidades encontradas. 
Cada linha do csv representara na primeira coluna uma entidade, na segunda a relacao, e na 
terceira a segunda entidade.'''
def write_related_entities_in_csv(related_entities):
    with open(path_episodes_output+csv_name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)
        for entity in related_entities:
            spamwriter.writerow(entity)


'''Responsavel por criar diretorios, caso nao existam.
Ou apenas abri-los, caso existam.'''
def create_diretory(path):
    if not (os.path.isdir(path)):
        os.mkdir(path)

'''Le o arquivo csv das entidades nomeadas e monta o dicionario para consulta.'''
def generate_dict_entities():
    mydict = {}
    with open(path_entities_csv+'.csv', mode='r') as infile:
        reader = csv.reader(infile, delimiter="\t")
        for i,line in enumerate(reader):
            entitiesList = line[0].split(',')
            mydict[entitiesList[0]] = []
            if len(entitiesList) > 1: mydict[entitiesList[0]] = entitiesList[1:]
    return mydict
    
'''Cria a tripla da relacao entre as entidades.
Apenas se ha um verbo entre duas entidades. '''
def create_triple_entity_relation(text_split, unigram_tagger):
    lemmatizer = WordNetLemmatizer()
    triples_line = []
    for i in range(1, len(text_split)):
        parts = text_split[i].split("<entidade:")
        words_middle = parts[0].split()

        if len(words_middle) == 1 and words_middle[0].isalnum() and "<entidade:" in text_split[i]:
            word_lemm =lemmatizer.lemmatize(words_middle[0], 'v')
            pos = unigram_tagger.tag([word_lemm])
            if pos[0][1] == 'VB':
                first = text_split[i-1].split(">")[1]
                second = text_split[i].split(">")[1]
                triples_line.append((first, word_lemm,second))
    return triples_line

'''Separa o texto por linhas, em cada linha separa os pedacos em que existem entidades.
Para cada pedaco, se existir mais de uma entidade, gera a tripla correspondente.'''
def generate_triples(content, unigram_tagger):
    triples = []
    line_content = tokenize.sent_tokenize(content)
    for line in line_content:
        #separa por entidade na linha
        split_line = line.split("</entidade>")
        if len(split_line) > 2 :
            #verifica relacao entre elas
            triples_line = create_triple_entity_relation(split_line, unigram_tagger)
            if len(triples_line) > 0 : triples += triples_line
    return triples

def do_main():
    triples = []
    brown_tagged_sents = brown.tagged_sents()
    unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
    #le todos os arquivos    
    seasons = os.listdir(path_episodes_output)
    for season in seasons:
    	if "season" in season:
            path_season = path_episodes_output+'/'+season+'/'
            files = os.listdir(path_season)
            for episode in files:
                with open(path_season + episode) as f:
                    #separa por linha
                    content = f.read()
                    triples += generate_triples(content, unigram_tagger)
    
    write_related_entities_in_csv(triples)
if __name__ == "__main__":
    do_main()
