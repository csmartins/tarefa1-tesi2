import os
import sys
import csv 
import re

'''Variaveis globais'''
path_output = "output"
path_entities_csv = "output/entities"
csv_name = "/classified_entities.csv"

classified_entities = {}
place_entities = []
family_names = []

'''Responsavel por escrever em um csv todas as entidades encontradas. 
Cada linha do csv representara na primeira coluna a classe a que pertence e 
na segunda o nome da entidade.'''
def write_classified_entities_in_csv():
    with open(path_output+csv_name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)
        for entity in classified_entities.keys():
            spamwriter.writerow((classified_entities[entity], entity))

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
        
def add_to_classified_entities(entities, tag):
    for entity in entities:
        classified_entities[entity] = tag

def tag_general_entities(entities):
    for entity in entities.keys():
        classified_entities[entity] = 'other'
        add_to_classified_entities(entities[entity], 'other')

def tag_places():
    global place_entities	
    add_to_classified_entities(place_entities, 'place')

def tag_houses():
    for entity in classified_entities.keys():
        if entity.startswith("House"):
            classified_entities[entity] = 'house'

            house = entity.split()
            if len(house) >= 2:
                family_names.append(house[1])
            # se house tem 3 palavras a terceira eh sempre um lugar
                if len(house) == 3:
                    classified_entities[house[2]] = 'place'	
    family_names.append('Snow')
    family_names.append('Sand')
    family_names.append('Karstark')
    family_names.append('Tarly')
    family_names.append('Clegane')
    family_names.append('Tully')

    for entity in classified_entities.keys():
        house = entity.split()
        if len(house) == 1 and entity in family_names:
            classified_entities[entity] = 'house'			
	
def set_places_entities(places):
    global place_entities
    place_entities = places

def tag_persons():
    all_persons = []
    for entity in classified_entities.keys():
        name = entity.split()
        if len(name) == 2 and name[0] not in ['House', 'Houses'] and name[1] in family_names:
            classified_entities[entity] = 'person'
            all_persons.append(name[0])

    for entity in classified_entities.keys():
        name = entity.split()
        if len(name) == 1 and entity in all_persons:
            classified_entities[entity] = 'person'
        

def tag_all():   
    dict_entities = generate_dict_entities()  
    
    tag_general_entities(dict_entities)
    tag_places()
    tag_houses()
    tag_persons()

    write_classified_entities_in_csv()
    
