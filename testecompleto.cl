CREATE camiseta "CamisaComLogo" {
    tecido = algodao;
    cor = vermelho;
    tamanho = G;
}
CORTAR CamisaComLogo EM detaEvt;
COSTURAR CamisaComLogo;
AJUSTAR CamisaComLogo PARA GG;
FINALIZAR CamisaComLogo;

CREATE blusa "BlusaComCapuz" {
    tecido = malha;
    cor = verde;
    tamanho = M;
}

CREATE calca "CalcaJeans" {
    tecido = jeans;
    cor = preto;
    tamanho = P;
}

COSTURAR BlusaComCapuz;
COSTURAR CalcaJeans;
FINALIZAR BlusaComCapuz;
FINALIZAR CalcaJeans;

CREATE bermuda "ShortLinho" {
    tecido = linho;
    cor = branco;
    tamanho = PP;
}
CORTAR ShortLinho EM tecidoShort;
AJUSTAR ShortLinho PARA M;


CREATE camiseta "CamisaComLogoEspecial" {
    tecido = malha;
    cor = azul;
    tamanho = M;
}

SE cor == "azul" {
    CORTAR CamisaComLogoEspecial EM tecidoAzul;
} SENAO {
    CORTAR CamisaComLogoEspecial EM tecidoPadrao;
}


CREATE calca "CalcaJeansGrande" {
    tecido = jeans;
    cor = cinza;
    tamanho = GG;
}

ENQUANTO tamanho == "GG" {
    AJUSTAR CalcaJeansGrande PARA G;
    CORTAR CalcaJeansGrande EM tecidoJeans;
}
FINALIZAR CalcaJeansGrande;
