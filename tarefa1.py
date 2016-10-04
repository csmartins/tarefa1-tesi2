import nltk
import re
import os
import sys
from nltk.tree import Tree
import csv

#nltk.help.upenn_tagset() PARA A POSTERIDADE

path_output = "output"

names_dict = {}
names_dict["Jon Snow"] = ["Jon", "Jon Snow", "Lord Commander Jon Snow", "Lord Snow"]
names_dict["Benjen Stark"] = ["Benjen Stark", "Benjen", "Uncle Benjen"]
names_dict["Eddard Stark"] = ["Ned Stark", "Ned", "Lord Eddard", "Eddard Stark", "Eddard", "Lord Eddard Stark"]
names_dict["Daenerys Targaryen"] = ["Daenerys Stormborn", "Daenarys", "Daenerys Targaryen", "Queen Daenerys Targaryen", "Princess Daenerys Targaryen", "Queen Daenerys", "Daenarys", "Dragon Queen", "Mhysa"]
names_dict["Theon Greyjoy"] = ["Theon"]
names_dict["Bran Stark"] = ["Bran", "Brandon Stark"]
names_dict["Rickon Stark"] = ["Rickon"]
names_dict["Gregor Clegane"] = ["Ser Gregor Clegane"]
names_dict["Jorah Mormont"] = ["Ser Jorah Mormont"]

nick_names = []

def clear_entity(entity):
    return entity.strip().strip('""').strip("(").strip(")").strip(".").strip("-").strip("[").strip("]").strip("{").strip("}").strip("'").strip()

def get_nicknames(s, nicks):
    quotes = [q.decode('utf-8') for q in s.split('"')[1::2]]
    if quotes != [] and nicks != []:
        for nick in nicks:
            if nick in quotes:
                nick_names.append(nick)

def generate_named_entity(s):
    sentences = nltk.sent_tokenize(s.decode('utf-8'))
    nicks = []
    named_entities = []
    for sentence in sentences:
    	words_tokenized = nltk.word_tokenize(sentence)

    	pos = nltk.pos_tag(words_tokenized)
    	grammar = ''' 	NICK: {<DT><NNP|NNPS>}
                        NE:	{<NNP|NNPS>+}
    				        {<NNP|NNPS><POS><NNP|NNPS>}
    				        {<NNP|NNPS>+<IN><NNP|NNPS>+}
    		    '''
    	#ner = nltk.ne_chunk(pos, binary=True)
    	regex_parser = nltk.RegexpParser(grammar)
    	ner = regex_parser.parse(pos)

    	for t in ner:
            if isinstance(t, nltk.tree.Tree):
                if t.label() == 'NICK':
                    text = ' '.join(c[0] for c in t)
                    nicks.append(text)

                if t.label() == 'NE':
                    text = ' '.join([c[0] for c in t])
                    named_entities.append(clear_entity(text))

    get_nicknames(s, nicks)

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
    f = open(path+"_named-entities.txt", 'w')

    f.write("------------ String contendo todo o texto")
    f.write("\n")
    f.write("\n")
    f.write("\n")

    for elem in content:
        f.write(elem+" ")

    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.close()


def write_named_entities(content, path):
    f = open(path+"_named-entities.txt", 'a')

    f.write("------------ Lista das Entidades Nomeadas")
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write(str(content))
    f.close()

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
    entities = sorted(list(set(entities)))

    with open(path_episodes+'/entities.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)

        for entity in entities:
            spamwriter.writerow([entity])

def clean_text(text_by_line):

	cleaned_text = []
	for line in text_by_line:
		#Condicoes para retirar parte debaixo do texto
		if ("Recap" in line or "Appearances" in line) and len(line) < 20: break
		#condicao para nao adicionar parte de cima do texto
		if len(line) > 150: cleaned_text.append(line)

	cleaned_text = remove_empty(cleaned_text)
	return cleaned_text

def create_diretory(path):
    if not (os.path.isdir(path)):
	os.mkdir(path)

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

    create_diretory(path_output)

    for season in seasons:
    	if "season" in season:
            path_season = path_episodes+'/'+season+'/'
            files = os.listdir(path_season)

	    path_season_output = path_output+'/'+season+'/'
	    create_diretory(path_season_output)

            for episode in files:
                with open(path_season + episode) as f:
                    full_content = f.read().splitlines()
                    full_content = clean_text(full_content)

		    path_episode_output = path_season_output+episode

                    write_full_content(full_content, path_episode_output)

                    write_list_of_line_contents(full_content, path_episode_output)

                    entities = list_named_entities(full_content)
                    write_named_entities(entities, path_episode_output)

                    named_entities += entities
    write_named_entities_in_csv(named_entities, path_output)

    #ainda esta apenas printando os nicknames enquanto nao os usamos para algo
    print nick_names


if __name__ == "__main__":
    do_main()
