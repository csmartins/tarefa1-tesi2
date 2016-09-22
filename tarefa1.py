import nltk
import re
import os
import sys
from nltk.tree import Tree
import csv

def generate_named_entity(s):
    sentences = nltk.sent_tokenize(s.decode('utf-8'))

    named_entities = []
    for sentence in sentences:
	words_tokenized = nltk.word_tokenize(sentence)

	pos = nltk.pos_tag(words_tokenized)
	grammar = ''' 	NE:	{<NNP|NNPS>+}
				{<NNP|NNPS><POS><NNP|NNPS>}
				{<NNP|NNPS>+<IN><NNP|NNPS>+}
		  '''
 
	#ner = nltk.ne_chunk(pos, binary=True)
	regex_parser = nltk.RegexpParser(grammar)
	ner = regex_parser.parse(pos)
	    
	for t in ner:
		if isinstance(t, nltk.tree.Tree):
			if t.node == 'NE':
				text = ' '.join([c[0] for c in t])
				named_entities.append(text)
    return named_entities

def remove_empty(content):
    content = filter(None, content)
    return content

def write_list_of_line_contents(content,path):
    f = open(path+"_named-entities.txt", 'a')
    f.write("------------ Lista contendo cada linha do Arquivo")
    f.write("\n")
    f.write("\n")
    f.write("\n")

    f.write(str(content))
    f.write("\n")
    f.write("\n")
    f.write("\n")

def write_full_content(content, path):
    f = open(path+"_named-entities.txt", 'a')

    f.write("------------ String contendo todo o texto")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    
    for elem in content:
        f.write(elem+" ")

    f.write("\n")
    f.write("\n")
    f.write("\n")
    

def write_named_entities(content, path):
    f = open(path+"_named-entities.txt", 'a')

    f.write("------------ Lista das Entidades Nomeadas")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write(str(content))

def list_named_entities(content):
	named_entities_repetition = []
        for line in content:
		line_named_entities = generate_named_entity(line)
		if line_named_entities != []:
			for entity in line_named_entities:
				named_entities_repetition.append(entity.strip())
	named_entities = list(set(named_entities_repetition))
	return named_entities

def write_named_entities_in_csv(entities, path_episodes):
    entities = map(lambda x: x.encode('utf8'), entities)
    entities = list(set(entities))
    print len(entities)
    with open(path_episodes+'/output/entities.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)

	for entity in entities:
            spamwriter.writerow([entity])

def clean_text(text_by_line):

	cleaned_text = []
	for line in text_by_line:
		#Condicoes para retirar parte debaixo do texto
		if "Recap" in line and len(line) < 20: break
		if "Appearances" in line and len(line) < 20: break
		#condicao para nao adicionar parte de cima do texto
		if len(line) > 150: cleaned_text.append(line)

	cleaned_text = remove_empty(cleaned_text)
	return cleaned_text

def do_main():
    if len(sys.argv) < 2:
        print "Insuficient number of arguments."
        print "Expected: python tarefa1.py <path_to_episodes>"
	print "Path Example: episodes (if it's in the same directory of this file.)"
        return

    full_content = ""
    path_episodes = sys.argv[1]

    named_entities = []
    entities = []
    seasons = os.listdir(path_episodes)
    for season in seasons:
	if "season" in season:
	    print season
	    path_season = path_episodes+'/'+season+'/'
    	    files = os.listdir(path_season)
            for episode in files:
		print episode
        	with open(path_season + episode) as f:
		     full_content = f.read().splitlines()
		     full_content = clean_text(full_content)

            	     write_full_content(full_content, path_season+"../output/"+season+"/"+episode)

	             write_list_of_line_contents(full_content, path_season+"../output/"+season+"/"+episode)
		     
	             entities = list_named_entities(full_content)
                     write_named_entities(entities, path_season+"../output/"+season+"/"+episode)
            	     named_entities += entities
    write_named_entities_in_csv(named_entities, path_episodes)
    

if __name__ == "__main__":
    do_main()
