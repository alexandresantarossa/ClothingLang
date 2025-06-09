%option noyywrap
%{
#include "clothinglang.tab.h"
#include <string.h>
#include <stdlib.h>
%}
%%
[ \t\r\n]+                     /* ignora espaços e quebras */

"CREATE"                       return CREATE;
"tecido"                       return TECIDO_KW;
"cor"                          return COR_KW;
"tamanho"                      return TAMANHO_KW;

"algodao"                      { yylval.str = strdup("algodao"); return TECIDO_VAL; }
"jeans"                        { yylval.str = strdup("jeans");   return TECIDO_VAL; }
"seda"                         { yylval.str = strdup("seda");    return TECIDO_VAL; }
"malha"                        { yylval.str = strdup("malha");   return TECIDO_VAL; }
"la"                           { yylval.str = strdup("la");      return TECIDO_VAL; }
"linho"                        { yylval.str = strdup("linho");   return TECIDO_VAL; }

"azul"                         { yylval.str = strdup("azul");        return COR_VAL; }
"preto"                        { yylval.str = strdup("preto");       return COR_VAL; }
"branco"                       { yylval.str = strdup("branco");      return COR_VAL; }
"vermelho"                     { yylval.str = strdup("vermelho");    return COR_VAL; }
"verde"                        { yylval.str = strdup("verde");       return COR_VAL; }
"amarelo"                      { yylval.str = strdup("amarelo");     return COR_VAL; }
"rosa"                         { yylval.str = strdup("rosa");        return COR_VAL; }
"roxo"                         { yylval.str = strdup("roxo");        return COR_VAL; }
"laranja"                      { yylval.str = strdup("laranja");     return COR_VAL; }

"PP"                           { yylval.str = strdup("PP"); return TAMANHO_VAL; }
"P"                            { yylval.str = strdup("P");  return TAMANHO_VAL; }
"M"                            { yylval.str = strdup("M");  return TAMANHO_VAL; }
"G"                            { yylval.str = strdup("G");  return TAMANHO_VAL; }
"GG"                           { yylval.str = strdup("GG"); return TAMANHO_VAL; }

"camiseta"                     { yylval.str = strdup("camiseta"); return PECA_TYPE; }
"calca"                        { yylval.str = strdup("calca");    return PECA_TYPE; }
"blusa"                        { yylval.str = strdup("blusa");    return PECA_TYPE; }
"saia"                         { yylval.str = strdup("saia");     return PECA_TYPE; }
"vestido"                      { yylval.str = strdup("vestido");  return PECA_TYPE; }
"bermuda"                      { yylval.str = strdup("bermuda");  return PECA_TYPE; }

"CORTAR"                       return CORTAR;
"COSTURAR"                     return COSTURAR;
"AJUSTAR"                      return AJUSTAR;
"PARA"                         return PARA;
"EM"                           return EM;
"FINALIZAR"                    return FINALIZAR;

\"[^\"]*\"                     { char*s=strdup(yytext+1);s[strlen(s)-1]='\0'; yylval.str=s; return STRING; }
[0-9]+                         { yylval.num = atoi(yytext); return NUMBER; }
[A-Za-z_][A-Za-z0-9_]*         { yylval.str = strdup(yytext); return IDENTIFIER; }

"="                            return '=';
";"                            return ';';
"{"                            return '{';
"}"                            return '}';

.                              return yytext[0];
%%
