import os
import sys
import csv 
import re

path_output = "output"
path_episodes_cleaned = "cleaned_episodes"
path_entities_csv = "output/entities"

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
	    entitiesList = line[0].split(',',1)
	    entitiesList = [x for x in entitiesList if x]
	    mydict[entitiesList[0]] = []
	    if len(entitiesList) > 1: mydict[entitiesList[0]] = entitiesList[1:]
    return mydict

'''Adiciona a tag das entidades em todas as palavras que se encontram no dicionario'''
def mark_entities(text, dictEnts):
    edited_text = text
    for key in dictEnts.keys():
        if key == 'Summary':
            print dictEnts[key]
        pattern = re.compile(r'(?<!<entidade:)\b'+key+r'\b')
        edited_text = pattern.sub("<entidade:"+key+">"+key+"</entidade>", edited_text)
        for value in dictEnts[key]:
            pattern = re.compile(r'(?<!<entidade:)\b'+value+r'\b')
            edited_text = pattern.sub("<entidade:"+key+">"+value+"</entidade>", edited_text)
    return edited_text

def do_main():
    dict_entities = generate_dict_entities()    

    full_content = ""

    seasons = os.listdir(path_episodes_cleaned)
    create_diretory(path_output)

    for season in seasons:
        if "season" in season:
            path_season = path_episodes_cleaned+'/'+season+'/'
            files = os.listdir(path_season)
            path_season_output = path_output+'/'+season+'/'
            create_diretory(path_season_output)

            for episode in files:		
                marked_content = ""
                with open(path_season + episode) as f:
                    full_content = f.read()
                    marked_content = mark_entities(full_content, dict_entities)
                with open(path_season_output+episode, 'w') as fWriter:
                    fWriter.write(marked_content)		
		
if __name__ == "__main__":
    do_main()
