# Python Xadrez comando de voz
Um jogo de xadrez em python controlado por comandos de voz.

Implementação original: https://github.com/boosungkim/python-chess

## Instalação

### Linux
```
sudo apt install jackd2
sudo apt install python3-pyaudio
sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && sudo pip install pyaudio
cd python-chess
pip install pygame
pip install SpeechRecognition
```

## Usando a aplicação
- Para executar utilize `python3 -W ignore chess_gui.py`.
- Então escolha entre 'comando de voz' e 'mouse' no terminal
- Para realizar movimentos por comando de voz é necessário falar a linha e a coluna desejada no seguinte formato.
### Correto
```
linha 1 coluna 2
coluna 3 linha 4
```
### Incorreto
```
1 2
linha 1 3
1 coluna 4
```

É possível observar o que o interpretador entendeu pelo terminal.