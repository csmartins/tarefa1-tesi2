import nltk
import re
import os
import sys
from nltk.tree import Tree

def generate_named_entity(s):
    sentences = nltk.sent_tokenize(s.decode('utf-8'))
    sentences = re.split('\\?+!+|!+\\?+|\\.+|!+|\\?+', s)

    named_entities = []
    for sentence in sentences:
	words_tokenized = nltk.word_tokenize(sentence)

	pos = nltk.pos_tag(words_tokenized)
	ner = nltk.ne_chunk(pos, binary=True)
	    
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
				named_entities_repetition.append(entity)
	named_entities = list(set(named_entities_repetition))
	return named_entities

def do_main():
    if len(sys.argv) < 2:
        print "Insuficient number of arguments."
        print "Expected: python tarefa1.py <path_to_files>"
	print "Path Example: /episodes/season_1/"
        return

    full_content = ""
    path_season = sys.argv[1]
    files = os.listdir(path_season)
    for episode in files:
        with open(path_season + episode) as f:
            full_content = f.read().splitlines()
            full_content = remove_empty(full_content)

            write_full_content(full_content, path_season+"../output/"+episode)

	    write_list_of_line_contents(full_content, path_season+"../output/"+episode)
	
            write_named_entities(list_named_entities(full_content), path_season+"../output/"+episode)
            

if __name__ == "__main__":
    do_main()
