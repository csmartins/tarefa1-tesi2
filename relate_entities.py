import os
import sys
import csv 
import nltk

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

    
'''Remove caracteres especiais da string da relacao.'''
def clean_entity(entity):
    newEntity = ''
    #Remove palavras que nao contem numeros ou letras (para casos com caracteres especiais)
    for word in entity.split():
        if word.isalnum(): newEntity += word+" "
    return newEntity

'''Funcao responsavel por obter as triplas de relacoes a partir da arvore sintatica gerada. Cria as strings das relacoes e entidades para formar as triplas.'''
def get_triple_from_relation(ner):
    triples = []
    for t in ner:
        if isinstance(t, nltk.tree.Tree):
            grammatical_form = t.label()
            #grammatical_form = t.node

            if grammatical_form == 'RELATION':
                ne1 = ""
                middle = ""
                ne2 = ""
                findVerb = False
                for x in t:
                    if isinstance(x[0], unicode):
                        findVerb = True
                        middle += x[0]+" "
                    else:
                        if findVerb == False:
                            for y in x[0]:
                                ne1 += y[0]+" "
                                ne1 = clean_entity(ne1)                     
                                            
                        else:
                            for y in x[0]:
                                ne2 += y[0]+" "
                                ne2 = clean_entity(ne2)
                if ne1 != '' and middle != '' and ne2 != '':
                    triples.append((ne1, middle, ne2))
    return triples

'''Funcao responsavel por parsear o regex da gramatica de relacoes e obter as triplas a partir da arvore sintatica.'''
def generate_relation_triples(ner):
    grammar = '''
            NE: {<NE_POS_NE|NE_IN_NE|PLACE|SIMPLE_NE>} 
            RELATION: {<NE>+<IN>?<DT>?<V.*>+<IN>?<DT>?<NE>+}
            '''
    regex_parser = nltk.RegexpParser(grammar)
    ner = regex_parser.parse(ner)

    return get_triple_from_relation(ner)

