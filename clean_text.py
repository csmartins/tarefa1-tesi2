import re
import sys
import os

path_episodes_cleaned = "cleaned_episodes"

def create_diretory(path):
    if not (os.path.isdir(path)):
	os.mkdir(path)

def remove_empty(content):
    content = filter(None, content)
    return content

def clean_text(text):

	init = re.search(r"Plot[ ]?(Edit)?\n", full_content).start() #comeca no plot ou plot edit
	end = re.search(r"(Recap[ ]?(Edit)?\n|Appearances[ ]?(Edit)?\n)", text).start() #termina no recap ou recap edit ou appearances edit
	
	text = text[init:end]

	#remove os plot edit e summary edit do meio do texto
	text = text.replace("PlotEdit", "").replace("Plot Edit", "").replace("SummaryEdit", "").replace("Summary Edit", "") 
	#remove os Edit de inicio de descricao de cena
	text = re.sub(r"([A-Z][a-z]*[ ]?)Edit", r'\1', text) 
	#remove linhas vazias
	text = remove_empty(text)
	return text

def do_main():
	if len(sys.argv) < 2:
		print "Insuficient number of arguments."
		print "Expected: python tarefa1.py <path_to_episodes>"
		print "Path Example: episodes (if it's in the same directory of this file.)"
		return

	path_episodes = sys.argv[1]
	seasons = os.listdir(path_episodes)

	create_diretory(path_episodes_cleaned)

	for season in seasons:
		if "season" in season:
			path_season = path_episodes+'/'+season+'/'
			files = os.listdir(path_season)

			path_season_cleaned = path_episodes_cleaned+'/'+season+'/'
			create_diretory(path_season_cleaned)

			for episode in files:
				global full_content
				with open(path_season + episode) as f:
					full_content = f.read()
					full_content = clean_text(full_content) 	
				with open(path_season_cleaned + episode, 'w') as f:
					f.write(str(full_content))

	

if __name__ == "__main__":
    do_main()
