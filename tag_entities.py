import os
import sys
import csv 
import re

'''Variaveis globais'''
path_output = "output"
path_entities_csv = "output/entities"
csv_name = "/tagged_entities.csv"
tags = ["person", "place", "family", "battle", "other"]

'''Responsavel por escrever em um csv todas as entidades encontradas. 
Cada linha do csv representara na primeira coluna o nome da entidade e 
na segunda a classe a que pertence.'''
def write_tagged_entities_in_csv(tagged_entities):
    with open(path_output+csv_name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)
        for entity in tagged_entities:
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
    
'''Cria tupla de entidade e sua classe caracteristica.'''
def create_tuples_entity_tag(dict_entities):
    listTuples = []
    for key in dict_entities.keys():
        listTuples.append(tag_entity(key))
        for value in dict_entities[key]:
            listTuples.append(tag_entity(value))
    listTuples = list(set(listTuples))
    listTuples.sort(key=lambda x: x[0])
    return listTuples
    
'''Adiciona a tag de classificacao das entidades'''
def tag_entity(entity):
    tag = "other"
    return (entity, tag)

def do_main():
    dict_entities = generate_dict_entities()  
    tagged_entities = create_tuples_entity_tag(dict_entities)  
    write_tagged_entities_in_csv(tagged_entities)
    
		
if __name__ == "__main__":
    do_main()
