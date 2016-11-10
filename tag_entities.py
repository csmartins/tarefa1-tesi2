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
tagged_entities = {}
place_entities = []
person_entities = []
family_names = []

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
    
def add_to_tagged_entities(entities, tag):
	for entity in entities:
		tagged_entities[entity] = tag

def tag_general_entities(entities):
	for entity in entities.keys():
		tagged_entities[entity] = 'other'
    	add_to_tagged_entities(entities[entity], 'other')

def populate_family_names(dict_entities):
	for tagged in tagged_entities:
		if tagged[0] == 'house':
			house = tagged[1].split()
			# se house tem 3 palavras a terceira eh sempre um lugar
			if len(house) == 2:
				family_names.append(house[1])

def tag_places():
	add_to_tagged_entities(place_entities, 'place')

def tag_houses():
	for entity in tagged_entities:
		if entity.startswith("House"):
        	tagged_entities[entity] = 'house'

			house = tagged[1].split()
			# se house tem 3 palavras a terceira eh sempre um lugar
			family_names.append(house[1])
			if len(house) == 3:
				tagged_entities[tagged[2]] = 'place'				
	
def tag_persons():
	pass

def tag_all(places):
	global place_entities
	place_entities = places	
    
	dict_entities = generate_dict_entities()  
    
	tag_general_entities(dict_entities)
	tag_places()
	tag_houses()
	tag_persons()
    write_tagged_entities_in_csv()
    
