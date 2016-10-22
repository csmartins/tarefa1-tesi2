# -*- coding: utf-8 -*-
import nltk
import os
import sys
from nltk.tree import Tree
import csv
#import Levenshtein

#nltk.help.upenn_tagset() PARA A POSTERIDADE

path_output = "output"
path_episodes_cleaned = "cleaned_episodes"

named_entities = []
names_dict = {}

nick_names = []

accepted_grammatical_forms = ['NE_POS_NE', 'NE_IN_NE', 'NE_VERB', 'PLACE', 'SIMPLE_NE']

def clear_entity(entity):
    return entity.strip().strip('"').strip("(").strip(")").strip(".").strip("-").strip("[").strip("]").strip("{").strip("}").strip("'").strip()


def get_nicknames(s, nicks):
    quotes = [q.decode('utf-8') for q in s.split('"')[1::2]]
    if quotes != [] and nicks != []:
        for nick in nicks:
            if nick in quotes:
                nick_names.append(nick)

def generate_named_entity(s):
    sentences = nltk.sent_tokenize(s.decode('utf-8'))
    nicks = []
    nes = []
    for sentence in sentences:
        sentence_nes = []
        words_tokenized = nltk.word_tokenize(sentence)
        pos = nltk.pos_tag(words_tokenized)

        grammar = '''
            NE_POS_NE: {<NNP|NNPS>+<POS><NNP|NNPS>}
            NE_IN_NE: {<NNP|NNPS>+<IN><NNP|NNPS>+}
            NE_VERB: {<NNP|NNPS>+<VBZ>}
            PLACE: {<IN>+<NNP|NNPS>+<POS>*<NNP|NNPS>*}
            SIMPLE_NE: {<NNP|NNPS>+}
            '''

        #ner = nltk.ne_chunk(pos, binary=True)
        regex_parser = nltk.RegexpParser(grammar)
        ner = regex_parser.parse(pos)

        for t in ner:
            if isinstance(t, nltk.tree.Tree):
                grammatical_form = t.label()
                #grammatical_form = t.node

                if grammatical_form in accepted_grammatical_forms:
                    if grammatical_form == 'NE_VERB':
                        text = ''
                        for c in t:
                            if c[1] in ['NNP', 'NNPS']:
                                text = text + ' ' + c[0]
                                text = clear_entity(text)

                        if len(text.split()) == 2:
                            if text not in names_dict.keys(): names_dict[text] = []
                        else:
                            sentence_nes.append(text)
                            nes.append(text)
                    elif grammatical_form == 'PLACE':
			text = ''                        
			for c in t:
                            if c[1] in ['NNP', 'NNPS']:
                                text = text + ' ' + c[0]
                                text = clear_entity(text)

                        if len(text.split()) == 2:
                            if text not in names_dict.keys(): names_dict[text] = []
                        else:
                            sentence_nes.append(text)
                            nes.append(text)
                    else:
                        text = ' '.join([c[0] for c in t])
                        text = clear_entity(text)
                        if len(text.split()) == 2:
                            if text not in names_dict.keys(): names_dict[text] = []
                        else:
                            sentence_nes.append(text)
                            nes.append(text)
        #print "Sentence: ", sentence
        #print "Generated NEs: ", sentence_nes

    #get_nicknames(s, nicks)
    return nes

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

    nes = list(set(named_entities_repetition))
    return nes

def write_named_entities_in_csv(entities, path_episodes):
    entities = map(lambda x: x.encode('utf8'), entities)
    entities = sorted(list(set(entities)))

    with open(path_episodes+'/entities.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)

        for entity in entities:
            spamwriter.writerow([entity])

def create_diretory(path):
    if not (os.path.isdir(path)):
	os.mkdir(path)

def remove_multiple_names():
    named_entities_cp = named_entities
    for name in names_dict.keys():
        for entity in named_entities:
            '''TO DO: Pensar em solucao para os apelidos.'''
            if similar_strings(name, entity) and entity not in names_dict.keys():
                names_dict[name].append(entity)
                named_entities_cp.remove(entity)
    '''Adicionando como entidades o que nao soubemos classificar'''
    for name in named_entities_cp:
        names_dict[name] = []

def similar_strings(s1, s2):
    if (s1 in s2) or (s2 in s1) :
        return True
    else:
        #distance = Levenshtein.distance(s1, s2)
        words2 = s2.split()
        totalWords2 = len(words2)
        words1 = s1.split()
        totalWords1 = len(words1)
        countEqual = 0
        if totalWords2 > 1 :
            for word in words2:
                if word in words1:
                    countEqual += 1
            if countEqual >= (totalWords1/2 + 1) or countEqual >= (totalWords2/2 + 1): return True

    return False

def do_main():
    print "Attention! You must pre proccess your text running:"
    print "python clean_text.py <path_to_episodes>"

    if len(sys.argv) < 1:
        print "Insuficient number of arguments."
        print "Expected: python tarefa1.py"
    	return

    full_content = ""
    global named_entities
    entities = []

    seasons = os.listdir(path_episodes_cleaned)
    create_diretory(path_output)

    for season in seasons:
    	if "season" in season:
            path_season = path_episodes_cleaned+'/'+season+'/'
            files = os.listdir(path_season)
            path_season_output = path_output+'/'+season+'/'
            create_diretory(path_season_output)

            for episode in files:
                with open(path_season + episode) as f:
                    full_content = f.read().splitlines()
                    full_content = filter(None, full_content)

                    path_episode_output = path_season_output+episode

                    write_full_content(full_content, path_episode_output)
                    print "Generating for ", season, "-", episode
                    entities = list_named_entities(full_content)
                    #tagged_content = insert_tags(full_content, entities)

                    write_list_of_line_contents(full_content, path_episode_output)
                    write_named_entities(entities, path_episode_output)
                    named_entities += entities

    remove_multiple_names()
    write_named_entities_in_csv(names_dict.keys(), path_output)

if __name__ == "__main__":
    do_main()
