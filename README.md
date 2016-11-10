# Trabalho Game of Thrones - tesi2 - reconhecimento de entidades nomeadas

## clean_text.py

É o arquivo responsável pelo pré processamento do texto de entrada. Ele trabalha com a retirada da parte não interessante do texto e retorna os arquivos limpos. É necessário que o caminho da pasta contendo os episódios seja passado como parâmetro.

Como rodar: python clean_text.py \<path_to_episodes\>

Cria uma pasta "clean_text" com o mesmo formato da pasta de episódios, contendo os textos limpos.

## generate_named_entities.py
É o arquivo responsável por gerar o csv com as entidades nomeadas encontradas em todos os arquivos já pré processados. O arquivo csv retorna as entidades cuja referência é a mesma em uma única linha.

Como rodar: python generate_named_entities.py

Espera-se que a pasta "cleaned_text" esteja preenchida.

Gera um arquivo "entities.csv" na pasta output.

Atenção!!!!! 

Por conta de uma falta de retrocompatibilidade da biblioteca NLTK os seguintes erros podem ser gerados quando o arquivo é executado:

NotImplementedError : Use l a b e l ( ) t o a c c e s s a node l a b e l .
A t t r i b u t e E r r o r : ’ Tree ’ o b j e c t has no a t t r i b u t e ’ l a b e l ’

O erro é corrigido trocando os comentários das linhas 129 e 130 do arquivo generate named entities.py e das linhas 41 e 42 do arquivo relate entities.py.


## mark_entities.py
É o arquivo responsável por gerar os textos limpos com a marcação de cada entidade no decorrer dos mesmos.

Como rodar: python mark_entities.py

Espera-se que a pasta "cleaned_text" e o arquivo "entities.csv" estejam preenchidos.

Cria as pastas com mesmo formato dos episódios na pasta "output".

## entity classifier.py
É o arquivo responsável por gerar um csv de todas as entidades nomeadas encontradas pelo nosso gerador e sua respectiva classe de descrição (person,place, house, battle ou other).
Este classificador é chamado pelo próprio gerador de entidades nomeadas, não sendo possível executá-lo sozinho.

Gera um arquivo ”classified entities.csv”na pasta output.

## relate_entities.py
É o arquivo responsável por gerar um csv de todas as relações entre entidades nomeadas encontradas nos arquivos de "output".

Esse arquivo é chamado pelo gerador de entidades nomeadas, não sendo possível executá-lo sozinho.

Gera um arquivo "related_entities.csv" na pasta output.

## tf-idf.py
Arquivo responsável por retornar os 5 documentos em que o texto da consulta passada como parâmetro possui mais ocorrências. Para tal usa-se a técnica de TF-IDF. Também recebe o caminho para os episódios.

Como rodar: 
$python tf-idf.py \<consulta\> \<caminho_para_os_episodios\>

Exemplo:
$ python tf-idf.py "Jon Snow Death" cleaned_episodes

## regras_gramatica.txt
É um arquivo texto responsável por caracterizar todas as regras de gramática utilizadas pelo programa "generate_named_entities.py" para encontrar as entidades nomeadas dos textos.

## anotacoes.txt
É um arquivo texto que armazena anotações diversas de coisas a fazer ou experimentos no decorrer do trabalho.
 
