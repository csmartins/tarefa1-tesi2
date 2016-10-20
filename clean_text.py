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

def clean_text(text_by_line):

	cleaned_text = []
	for line in text_by_line:
		#Condicoes para retirar parte debaixo do texto
		if ("Recap" in line or "Appearances" in line) and len(line) < 20: break
		#condicao para nao adicionar parte de cima do texto
		if len(line) > 150: cleaned_text.append(line)

	cleaned_text = remove_empty(cleaned_text)
	return cleaned_text

def do_main():
	if len(sys.argv) < 2:
		print "Insuficient number of arguments."
		print "Expected: python tarefa1.py <path_to_episodes>"
		print "Path Example: episodes (if it's in the same directory of this file.)"
		return

	full_content = ""
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
				with open(path_season + episode) as f:
					full_content = f.read().splitlines()
					full_content = clean_text(full_content)
					with open(path_season_cleaned + episode, 'w') as f:
						f.write(str(full_content))

	

if __name__ == "__main__":
    do_main()
