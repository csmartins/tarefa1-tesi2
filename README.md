# Trabalho Game of Thrones - tesi2 - reconhecimento de entidades nomeadas

## clean_text.py

É o arquivo responsável pelo pré processamento do texto de entrada. Ele trabalha com a retirada da parte não interessante do texto e retorna os arquivos limpos. É necessário que o caminho da pasta contendo os episódios seja passado como parâmetro.

Como rodar: python clean_text.py <path_to_episodes>

Cria uma pasta "clean_text" com o mesmo formato da pasta de episódios, contendo os textos limpos.

## generate_named_entities.py
É o arquivo responsável por gerar o csv com as entidades nomeadas encontradas em todos os arquivos já pré processados. O arquivo csv retorna as entidades cuja referência é a mesma em uma única linha.

Como rodar: python generate_named_entities.py

Espera-se que a pasta "cleaned_text" esteja preenchida.

Gera um arquivo "entities.csv" na pasta output.


## mark_entities.py
É o arquivo responsável por gerar os textos limpos com a marcação de cada entidade no decorrer dos mesmos.

Como rodar: python mark_entities.py

Espera-se que a pasta "cleaned_text" e o arquivo "entities.csv" estejam preenchidos.

Cria as pastas com mesmo formato dos episódios na pasta "output".


## regras_gramatica.txt
É um arquivo texto responsável por caracterizar todas as regras de gramática utilizadas pelo programa "generate_named_entities.py" para encontrar as entidades nomeadas dos textos.
 
