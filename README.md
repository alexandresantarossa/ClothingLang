# ClothingLang - APS LOGCOMP 25.1

Atividade Prática Supervisionada de Lógica de Computação

Alexandre Santarossa
#

**Descrição**: ClothingLang é uma linguagem de programação projetada para a indústria da moda, focada na criação e produção de peças de vestuário. Com ela, é possível definir tecidos, cores, tamanhos e estilos de roupas, além de controlar os processos de fabricação, como corte, costura e ajustes.
#

**Gramática EBNF**
```
LETTER = ( "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" |
          "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" );

DIGIT = ( "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" );

NUMBER = DIGIT, {DIGIT};

STRING = '"', {LETTER | " "}, '"';

IDENTIFIER = LETTER, {LETTER | DIGIT | "_"};  

VALUE = STRING | NUMBER;

TECIDOS = "algodão" | "jeans" | "seda" | "malha" | "lã" | "linho" ;

COR = "azul" | "preto" | "branco" | "vermelho" | "verde" | "amarelo" | "rosa" | "roxo" | "laranja" ;

TAMANHO = "PP" | "P" | "M" | "G" | "GG";

PECA = "camiseta" | "calça" | "blusa" | "saia" | "vestido" | "bermuda" ;

PECA_DE_ROUPA = "CREATE", PECA, STRING, "{", 
    "tecido", "=", TECIDOS, ";", 
    "cor", "=", COR, ";", 
    "tamanho", "=", TAMANHO, ";", 
    "}" ;

PROCESSO = "CORTAR", IDENTIFIER, "EM", IDENTIFIER, ";"
         | "COSTURAR", IDENTIFIER, ";"
         | "AJUSTAR", IDENTIFIER, "PARA", TAMANHO, ";"
         | "FINALIZAR", IDENTIFIER, ";";

PRODUCAO = PECA_DE_ROPA, {PROCESSO};

COMENTARIO = "/*", {LETTER | DIGIT | " "}, "*/";
