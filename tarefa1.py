import nltk
import re
import os
import sys

s = "Barack Obama is the president of the United States. And he is famous"

def generate_named_entity(s):
    #print "generating for ", s
    sentences = nltk.sent_tokenize(s.decode('utf-8'))
    sentences = re.split('\\?+!+|!+\\?+|\\.+|!+|\\?+', s)

    tokenized = nltk.word_tokenize(sentences[0])

    pos = nltk.pos_tag(tokenized)

    return pos
    #Part-Of-Speech tags
    #ner = nltk.ne_chunk(pos, binary=True)
    #ner.draw()

def remove_empty(content):
    content = filter(None, content)
    return content

def write_full_content(content, path):
    f = open(path+"_named-entities.txt", 'a')

    for elem in content:
        f.write(elem)

    f.write("\n")

    f.write(str(content))

def write_named_entities(content, path):
    f = open(path+"_named-entities.txt", 'a')
    f.write("\n")
    f.write(str(content))

def do_main():
    if len(sys.argv) < 2:
        print "Insuficient number of arguments."
        print "Expected: python tarefa1.py <path_to_files>"
        return

    full_content = ""
    path_season = sys.argv[1]

    files = os.listdir(path_season)
    for episode in files:
        with open(path_season + episode) as f:
            #print f.readlines()
            full_content = f.read().splitlines()
            full_content = remove_empty(full_content)

            write_full_content(full_content, path_season+"../output/"+episode)

            named_entities = []
            for string in full_content:
                named_entities.append(generate_named_entity(string))

            write_named_entities(named_entities, path_season+"../output/"+episode)
            #print named_entities


if __name__ == "__main__":
    do_main()
