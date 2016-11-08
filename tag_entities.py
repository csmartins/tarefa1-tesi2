import os
import sys
import csv 
import re

'''Variaveis globais'''
path_output = "output"
path_entities_csv = "output/entities"
csv_name = "/tagged_entities.csv"

tags = ["person", "place", "family", "battle", "other"]
places_names = ["Castle", "Cities", "Free City", "Sept"]
tagged_entities = []
place_entities = []
person_entities = []

'''Responsavel por escrever em um csv todas as entidades encontradas. 
Cada linha do csv representara na primeira coluna a classe a que pertence e 
na segunda o nome da entidade.'''
def write_tagged_entities_in_csv():
    with open(path_output+csv_name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)
        for entity in tagged_entities:
			for ent in entity[1]:
				spamwriter.writerow((entity[0], ent))

'''Responsavel por criar diretorios, caso nao existam. Ou apenas abri-los, caso existam.'''
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
    
def add_to_tagged_entities(entity, related_entities, tag):
	entities = []
	entities.append(entity)
	entities.extend(related_entities)

	tagged_entities.append((tag, entities))

'''Adiciona a tag de classificacao das entidades'''
def tag_entity(entity, related_entities):
    if entity.startswith("House"):
        add_to_tagged_entities(entity, related_entities, 'house')
        return None
    
	#for place in places_names:
	#	if place in entity:
	#		add_to_tagged_entities(entity, related_entities, 'place')
	#		return None
    if entity in place_entities:
        add_to_tagged_entities(entity, related_entities, 'place')
        return None
    else:
        for ent in related_entities:
            if ent in place_entities:
                add_to_tagged_entities(entity, related_entities, 'place')
                return None

    if entity in person_entities:
        add_to_tagged_entities(entity, related_entities, 'person')
        return None
    else:
        for ent in related_entities:
            if ent in person_entities:
                add_to_tagged_entities(entity, related_entities, 'person')
                return None
    
    add_to_tagged_entities(entity, related_entities, 'other')
    return None

def populate_place_entities(places):
	place_entities = places

def populate_person_entities(persons):
	person_entities = persons

def tag(places, persons):
    global place_entities, person_entities
    
    place_entities = places
    person_entities = persons

    dict_entities = generate_dict_entities()  
    
    for entity in dict_entities.keys():
    	tag_entity(entity, dict_entities[entity])
  
    write_tagged_entities_in_csv()
    
