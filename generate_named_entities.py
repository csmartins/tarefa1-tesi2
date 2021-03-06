# -*- coding: utf-8 -*-
import nltk
import os
import sys
from nltk.tree import Tree
import csv
import Levenshtein
import entity_classifier
import relate_entities

'''Variaveis de caminho de paths'''
path_output = "output"
path_episodes_cleaned = "cleaned_episodes"
special_names_to_ignore = ['Hizdahr zo Loraq', 'Yezzan zo Qaggaz', 'Kraznys mo Nakloz']
special_first_word_to_consider = ['Battle', 'Master', 'Castle']
csv_name = "/entities.csv"

'''Variaveis globais de listas'''
named_entities = []
names_dict = {}
accepted_grammatical_forms = ['NE_POS_NE', 'NE_IN_NE', 'NE_VERB', 'PLACE', 'SIMPLE_NE']
stopwords = ['Lord ', 'King ', 'Queen ', 'Sir ', 'Ser ', 'Prince ', 'Princess ', 'Regent ', 'Commander ', 'Lady ', 'Young ', 'Maester ', 'Grand Maester ', 'The', 'Khal' ]

place_entities = []
person_entities = []
triples = []

'''Remove caracteres indesejados das entidades.'''
def clear_entity(entity):
    newEntity = ''
    #Remove palavras que nao contem numeros ou letras (para casos com caracteres especiais)
    for word in entity.split():
        if word.isalnum(): newEntity += word+" "
        
    return newEntity.strip().strip('"').strip("(").strip(")").strip(".").strip("-").strip("[").strip("]").strip("{").strip("}").strip("'")

'''Remove as stopwords da entidade.'''
def remove_stopwords(entity):
    for word in stopwords:
        if word in entity:
            entity = entity.replace(word, '').strip()
    return entity

'''Remove stop words e limpa os espacos das entidades que possuem nomes próprios.'''
def refine_text_from_tree(t):
    text = ''
    for c in t:
        if c[1] in ['NNP', 'NNPS']:
            text = text + ' ' + c[0]
    	    text = remove_stopwords(text)
            text = clear_entity(text)
    return text

'''Remove palavras minusculas no meio de entidades. Transforma as duas entidades da ponta em entidades diferentes. Ignora caso a palavra possua 'of' como minuscula.'''    
def remove_middle_words_lower(text):
    text_split = text.split()
    if len(text_split) <= 1 or (" of " in text): 
        return [text]
        
    else:
        newEntities = []
        newEntity = text_split[0]+" "
        for x in range(1, len(text_split)):
            if text_split[x][0].isupper() is not True:
                newEntities.append(newEntity.strip())
                newEntity = ""
            else:
                newEntity += text_split[x]+" "
        if newEntity != "": 
            newEntities.append(newEntity.strip())
    return newEntities
    
'''Se entidade comecar com letra minuscula, so pega a partir da primeira palavra com letra maiuscula'''
def remove_initial_words_lower(text):
    result = ""
    text_split = text.split()
    if (len(text) > 0 and text[0].isupper() is not True and len(text_split) > 1):
        for i in range(0, len(text_split)):
            if text_split[i][0].isupper() is True:
                text_split = text_split[i:]
                for x in text_split:
                    result += x+" "
                break
    if(result != ""): 
        text = result
    return text.strip()


'''Adiciona como chave do dicionario de entidades se a mesma for uma sequencia de nomes proprios de tamanho 2
(assumimos que nesse caso sera nome e sobrenome). Caso contrario, verifica se entidade possui palavra de letra minuscula no meio: se sim, separa em entidades tudo o que não for minusculo e retorna na lista nes, se não apenas retorna na lista.'''
def add_entity_to_nes(text, nes, grammatical_form):
    text_split = text.split()
    
    #Condicoes para nao considerar como entidade
    if len(text_split) == 0 or (text in special_names_to_ignore and grammatical_form == 'NE_VERB') or (text in names_dict.keys() or (len(text) > 0 and text[0].isupper() is not True and len(text_split) == 1)):
        pass
                
    #Se forem 2 palavras como simple_ne adiciona como chave
    elif len(text_split) == 2 and grammatical_form == 'SIMPLE_NE':
        if text not in names_dict.keys():
            names_dict[text.strip()] = []
    
    else:
        nes.append(text)


'''Responsavel por fazer o chunk das entidades ao separa-las por frases, utilizando o regexParser e
as regras definidas pela nossa gramatica.'''
def generate_named_entity(s):
    sentences = nltk.sent_tokenize(s.decode('utf-8'))
    nes = []
    global triples 
    for sentence in sentences:
        words_tokenized = nltk.word_tokenize(sentence)
        pos = nltk.pos_tag(words_tokenized)
        if len(pos) == 0 : continue
        grammar = '''
            NE_POS_NE: {<NNP|NNPS>+<POS><NNP|NNPS>}
            NE_IN_NE: {<NNP|NNPS>+<IN><NNP|NNPS>+}
            PLACE: {<IN>+<NNP|NNPS>+<POS>*<NNP|NNPS>*}
            SIMPLE_NE: {<NNP|NNPS>+}
            '''
        regex_parser = nltk.RegexpParser(grammar)
        ner = regex_parser.parse(pos)
        
        triples += relate_entities.generate_relation_triples(ner)    
        for t in ner:
            if isinstance(t, nltk.tree.Tree):
                grammatical_form = t.label()
                #grammatical_form = t.node

                if grammatical_form in accepted_grammatical_forms:
                    if grammatical_form == 'PLACE':
                        if t[0][1] == 'IN' and t[0][0] in ['from', 'in', 'at']:
                            t.remove(t[0])
                            text = refine_text_from_tree(t)
                            text = remove_initial_words_lower(text)
                            entities_text = remove_middle_words_lower(text)
                            for ent in entities_text:
                                add_entity_to_nes(ent.strip(),nes, grammatical_form)
                                place_entities.append(ent)				
                        
                    else:
                        text = ' '.join([c[0] for c in t])
                        text = remove_stopwords(text)
                        text = clear_entity(text)
                        text = remove_initial_words_lower(text)
                        entities_text = remove_middle_words_lower(text)
                        for ent in entities_text:
                            add_entity_to_nes(ent.strip(),nes, grammatical_form)
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
    named_entities_repetition += named_entities
    named_entities = list(set(named_entities_repetition))

'''Responsavel por escrever em um csv todas as entidades encontradas. 
Cada linha do csv representara na primeira coluna o nome a ser considerado da entidade e 
nas demais colunas os outros nomes associados.'''
def write_named_entities_in_csv(entities, path_episodes):
    entitiesKeys = map(lambda x: x.encode('utf8'), entities.keys())
    entitiesKeys = sorted(list(set(entities.keys())))

    with open(path_episodes+csv_name, 'wb') as csvfile:
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
            if len(entity) == 0 : continue
            if entity not in names_dict.keys() and entity.split()[0] not in special_first_word_to_consider and  similar_strings(name, entity):
                names_dict[name].append(entity)
                named_entities_cp.remove(entity)
                
    #Adicionando como entidades o que nao soubemos classificar
    for name in named_entities_cp:
        if len(name) == 0: continue
        
        encontrou = False
        if name.split()[0] not in special_first_word_to_consider:
            for nameKey in names_dict.keys():
                if similar_strings(nameKey, name):
                    if name.strip() != nameKey.strip(): names_dict[nameKey].append(name)
                    encontrou = True
                    break
                    
        if encontrou == False: 
            names_dict[name.strip()] = []

'''Responsavel por juntar as keys que sao similares, por exemplo: White Walker e White Walkers'''            
def remove_similar_keys():
    for key1 in names_dict.keys():        
        for key2 in names_dict.keys():
            if key1 != key2 and key1 in names_dict.keys() and key2 in names_dict.keys() and Levenshtein.distance(key1, key2) <= 1:
                #condicao para nao juntar Aemon e Aegon Targaryen
                if key1 == "Aemon Targaryen" or key1 == "Aegon Targaryen" or key2 == "Aemon Targaryen" or key2 == "Aegon Targaryen": continue
                union_keys_names_dict(key1,key2)
    union_keys_names_dict("Daenerys Targaryen", "Daenarys")            

'''Responsavel por receber duas chaves do dicionario de entidades e concatena-los, copiando tanto a chave como os 
valores de um para os valores de outro.'''
def union_keys_names_dict(key1, key2):
    values = names_dict[key1]
    values.append(key2)
    values += names_dict[key2]
    names_dict[key1] = values
    del names_dict[key2]    

'''Funcao responsavel por comparar as strings e verificar se pertencem a mesma entidade.'''
def similar_strings(s1, s2):
    if (s1 in s2) or (s2 in s1) :
        return True
    else:
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
    remove_similar_keys()
    write_named_entities_in_csv(names_dict, path_output)

    entity_classifier.set_places_entities(place_entities)
    entity_classifier.tag_all()
    relate_entities.write_related_entities_in_csv(triples)

if __name__ == "__main__":
    do_main()
