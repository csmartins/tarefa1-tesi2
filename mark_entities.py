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
	    entitiesList = line[0].split(',')
	    mydict[entitiesList[0]] = []
	    if len(entitiesList) > 1: mydict[entitiesList[0]] = entitiesList[1:]
    return mydict
    
def create_dict_replace(key, value):
    #value+' ': "<entidade:"+key+">"+value+"</entidade> "
    return {' '+value+' ': " <entidade:"+key+">"+value+"</entidade> ", ' '+value+', ': " <entidade:"+key+">"+value+"</entidade>, ",' '+value+'.': " <entidade:"+key+">"+value+"</entidade>.", "\n"+value+' ': "\n<entidade:"+key+">"+value+"</entidade> ", ' '+value+"\n": " <entidade:"+key+">"+value+"</entidade>\n", ' '+value+"!": " <entidade:"+key+">"+value+"</entidade>!", ' '+value+"?": " <entidade:"+key+">"+value+"</entidade>?", ' '+value+":": " <entidade:"+key+">"+value+"</entidade>:"}

'''Adiciona a tag das entidades em todas as palavras que se encontram no dicionario'''
def mark_entities(text, dictEnts):
    edited_text = text

    for key in dictEnts.keys():
        possible_matches_key = create_dict_replace(key, key)
        
        for match in possible_matches_key.keys():
            new_text = edited_text
            new_text = new_text.replace(match, possible_matches_key[match]) 
            if new_text.find("<entidade:<") == -1:
                edited_text = new_text
                
        for value in dictEnts[key]:
            possible_matches_value = create_dict_replace(key, value)
        
            for match in possible_matches_value.keys():
                new_text = edited_text
                new_text = new_text.replace(match, possible_matches_value[match]) 
                if new_text.find("<entidade:<") == -1:
                    edited_text = new_text
                    
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
