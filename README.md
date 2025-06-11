# ClothingLang - APS LOGCOMP 2025.1

Atividade Prática Supervisionada de Lógica de Computação

Autor: Alexandre Santarossa


**Descrição**: ClothingLang é uma linguagem de programação projetada para a indústria da moda, focada na criação e produção de peças de vestuário. Com ela, é possível definir tecidos, cores, tamanhos e estilos de roupas, além de controlar os processos de fabricação, como corte, costura e ajustes.

## Apresentação de Slides
https://www.canva.com/design/DAGp2LUF3z0/1jQNgn-ZHqvrrTDHpgg8sQ/edit?utm_content=DAGp2LUF3z0&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Estrutura do Repositório
- **clothinglang.l**           – Definições do lexer (Flex) para tokens da linguagem (sem if/while)
- **clothinglang.y**           – Gramática Bison (EBNF → regras sintáticas); gera parser em C. (sem if/while)
- **clothinglang.output**      – Relatório de análise sintática (`bison -v`) (sem if/while)  
- **lex.yy.c**                 – Código gerado pelo Flex  (sem if/while)
- **clothinglang.tab.c**       – Código gerado pelo Bison  (sem if/while)
- **clothinglang.tab.h**       – Header gerado pelo Bison  (sem if/while)
- **clothinglang_compiler.py** – Interpretador em Python, baseado na versão 2.4 desenvolvido ao longo do semestre
- **testecompleto.cl**         – Suíte de testes de exemplo de criação de peças e processos, para utilizar na versão python
- **testeflexbison.cl**        - Suíte de testes de exemplo de criação de peças e processos, sem if ou while, para utilizar na versão Flex+Bison

## Gramática EBNF
```
LETTER = ( "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" |
          "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" );

DIGIT = ( "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" );

NUMBER       = DIGIT, { DIGIT };
STRING       = '"' , { LETTER | DIGIT | "_" | " " } , '"';
IDENTIFIER   = LETTER, { LETTER | DIGIT | "_" };

PECA_TYPE    = "camiseta" | "calca" | "blusa" | "saia" | "vestido" | "bermuda";
TECIDO_TYPE  = "algodao" | "jeans" | "seda" | "malha" | "la" | "linho";
COR_TYPE     = "azul" | "preto" | "branco" | "vermelho" | "verde" | "amarelo" | "rosa" | "roxo" | "laranja";
TAMANHO_TYPE = "PP" | "P" | "M" | "G" | "GG";

COMANDO      = "CORTAR"    , IDENTIFIER , "EM"   , IDENTIFIER , ";" 
             | "COSTURAR" , IDENTIFIER , ";" 
             | "AJUSTAR"  , IDENTIFIER , "PARA" , TAMANHO_TYPE , ";" 
             | "FINALIZAR", IDENTIFIER , ";";

CREATE       = "CREATE" , PECA_TYPE , STRING , "{"
                 , "TECIDO"  , "=" , TECIDO_TYPE  , ";"
                 , "COR"     , "=" , COR_TYPE     , ";"
                 , "TAMANHO" , "=" , TAMANHO_TYPE , ";"
               , "}" , { COMANDO };

IF           = "SE" , IDENTIFIER , "==", ( IDENTIFIER | STRING ), "{", { COMANDO }, "}"
               , "SENAO" , "{", { COMANDO }, "}";

WHILE        = "ENQUANTO" , IDENTIFIER , "==", ( IDENTIFIER | STRING ), "{", { COMANDO }, "}";

UNIT         = CREATE
             | IF
             | WHILE
             | COMANDO;

PROGRAM      = { UNIT };
```
## Versão Flex + Bison
Funciona, porém está numa versão anterior, sem condicionais ou loops, portanto, o recomendado é usar a versão Python.
### Dependências
No Linux (Ubuntu):
```
sudo apt update && sudo apt install -y flex bison gcc make
```
### Limpeza
Para remover todos os arquivos gerados pelo Flex/Bison antes de compilar do zero:
```
rm -f lex.yy.c clothinglang.tab.* clothinglang clothinglang.output
```
### Compilar e Rodar
```
# 1. Gere o parser (com relatório -v)
bison -d -v clothinglang.y

# 2. Gere o lexer
flex clothinglang.l

# 3. Compile tudo
gcc -o clothinglang clothinglang.tab.c lex.yy.c -lfl

# 4. Execute com o suite de testes
./clothinglang < testeflexbison.cl
```
## Versão Compilador Python
### Dependências
Python3.6+
### Rodar
```
python3 clothinglang_compiler.py testecompleto.cl
```
