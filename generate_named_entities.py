# -*- coding: utf-8 -*-
import nltk
import os
import sys
from nltk.tree import Tree
import csv

'''Variaveis de caminho de paths'''
path_output = "output"
path_episodes_cleaned = "cleaned_episodes"

'''Variaveis globais de listas'''
named_entities = []
names_dict = {}
nick_names = []
accepted_grammatical_forms = ['NE_POS_NE', 'NE_IN_NE', 'NE_VERB', 'PLACE', 'SIMPLE_NE']
stopwords = ['Lord ', 'King ', 'Queen ', 'Sir ', 'Ser ', 'Prince ', 'Princess ', 'Regent ', 'Commander ', 'Lady ', 'Young ', 'Maester ', 'Grand Maester ', 'of ' ]

'''Remove caracteres indesejados das entidades.'''
def clear_entity(entity):
    newEntity = ''
    #Remove palavras que nao contem numeros ou letras (para casos com caracteres especiais)
    for word in entity.split():
        if word.isalnum(): newEntity += word+" "
        
    return newEntity.strip().strip('"').strip("(").strip(")").strip(".").strip("-").strip("[").strip("]").strip("{").strip("}").strip("'")

'''Remove as stopwrods da entidade.'''
def remove_stopwords(entity):
    for word in stopwords:
        if word in entity:
            entity = entity.replace(word, '').strip()
    return entity

'''Pega possiveis entidades reconhecidas como apelidos'''
def get_nicknames(s, nicks):
    quotes = [q.decode('utf-8') for q in s.split('"')[1::2]]
    if quotes != [] and nicks != []:
        for nick in nicks:
            if nick in quotes:
                nick_names.append(nick)
                
'''Remove stop words e limpa os espacos das entidades que possuem nomes próprios.'''
def refine_text_from_tree(t):
    text = ''
    for c in t:
        if c[1] in ['NNP', 'NNPS']:
            text = text + ' ' + c[0]
    	    text = remove_stopwords(text)
            text = clear_entity(text)
    return text

'''Adiciona como chave do dicionario de entidades se a mesma for uma sequencia de nomes proprios de tamanho 2
(assumimos que nesse caso sera nome e sobrenome). Caso contrario, retorna na lista nes.'''
def add_entity_to_nes(text, nes, grammatical_form):
    text_split = text.split()
    special_names = ['Hizdahr zo Loraq', 'Yezzan zo Qaggaz', 'Kraznys mo Nakloz']
    if len(text_split) >= 2:
        if text_split[0][0].isupper():
            if text_split[1][0].isupper() is not True: 
                if text in special_names and grammatical_form == 'NE_VERB':
                     pass
                else:
                     text = text_split[0]
        else:
            if text_split[1][0].isupper():
                text_split.pop(0)
                text = ' '.join(c for c in text_split)
    if len(text_split) == 2 and grammatical_form == 'SIMPLE_NE':
        if text not in names_dict.keys(): names_dict[text] = []
    else:
        nes.append(text)


'''Responsavel por fazer o chunk das entidades ao separa-las por frases, utilizando o regexParser e
as regras definidas pela nossa gramatica.'''
def generate_named_entity(s):
    sentences = nltk.sent_tokenize(s.decode('utf-8'))
    nicks = []
    nes = []
    for sentence in sentences:
        words_tokenized = nltk.word_tokenize(sentence)
        pos = nltk.pos_tag(words_tokenized)

        grammar = '''
            NE_POS_NE: {<NNP|NNPS>+<POS><NNP|NNPS>}
            NE_IN_NE: {<NNP|NNPS>+<IN><NNP|NNPS>+}
            NE_VERB: {<NNP|NNPS>+<VBZ>}
            PLACE: {<IN>+<NNP|NNPS>+<POS>*<NNP|NNPS>*}
            SIMPLE_NE: {<NNP|NNPS>+}
            '''
        regex_parser = nltk.RegexpParser(grammar)
        ner = regex_parser.parse(pos)

        for t in ner:
            if isinstance(t, nltk.tree.Tree):
                grammatical_form = t.label()
                #grammatical_form = t.node

                if grammatical_form in accepted_grammatical_forms:
                    if grammatical_form == 'NE_VERB':
                        text = refine_text_from_tree(t)
                        add_entity_to_nes(text, nes, grammatical_form)
                        
                    elif grammatical_form == 'PLACE':
                        if t[0][1] == 'IN' and t[0][0] in ['from', 'in', 'at']:
                            t.remove(t[0])
                            text = refine_text_from_tree(t)
                            add_entity_to_nes(text,nes, grammatical_form)
                        
                    else:
                        text = ' '.join([c[0] for c in t])
                        text = remove_stopwords(text)
                        text = clear_entity(text)
                        add_entity_to_nes(text,nes, grammatical_form)
    return nes

'''Responsavel por alterar a variavel global de entidades nomeadas, adicionando as encontradas em cada linha.'''
def list_named_entities(content):
    named_entities_repetition = []
    global named_entities
    for line in content:
        line_named_entities = generate_named_entity(line)
        if line_named_entities != []:
            for entity in line_named_entities:
                named_entities_repetition.append(entity.strip())

    named_entities += list(set(named_entities_repetition))


'''Responsavel por escrever em um csv todas as entidades encontradas. 
Cada linha do csv representara na primeira coluna o nome a ser considerado da entidade e 
nas demais colunas os outros nomes associados.'''
def write_named_entities_in_csv(entities, path_episodes):
    entitiesKeys = map(lambda x: x.encode('utf8'), entities.keys())
    entitiesKeys = sorted(list(set(entities.keys())))

    with open(path_episodes+'/entities.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)

        for entity in entitiesKeys:
	    listRow = [entity]
 	    for x in list(set(entities[entity])):
		listRow.append(x.encode('ascii', 'ignore'))
            spamwriter.writerow([s.encode('utf8') for s in listRow])

'''Responsavel por criar diretorios, caso nao existam.
Ou apenas abri-los, caso existam.'''
def create_diretory(path):
    if not (os.path.isdir(path)):
	os.mkdir(path)

'''Responsavel por popular o dicionario de entidades que se dirigem ao mesmo personagem.'''
def remove_multiple_names():
    named_entities_cp = named_entities
    for name in names_dict.keys():
        for entity in named_entities:
            #TO DO: Pensar em solucao para os apelidos.
            if similar_strings(name, entity) and entity not in names_dict.keys():
                names_dict[name].append(entity)
                named_entities_cp.remove(entity)
    #Adicionando como entidades o que nao soubemos classificar
    for name in named_entities_cp:
        names_dict[name] = []

'''Funcao responsavel por comparar as strings e verificar se pertencem a mesma entidade.'''
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
    full_content = ""

    seasons = os.listdir(path_episodes_cleaned)
    for season in seasons:
    	if "season" in season:
            path_season = path_episodes_cleaned+'/'+season+'/'
            files = os.listdir(path_season)
            for episode in files:
                with open(path_season + episode) as f:
                    line_content = f.read().splitlines()
                    list_named_entities(line_content)

    remove_multiple_names()
    write_named_entities_in_csv(names_dict, path_output)

if __name__ == "__main__":
    do_main()
