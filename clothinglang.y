%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);

// variáveis globais para acumular informações
static int unit_count = 0;
static char *g_peca, *g_nome, *g_tecido, *g_cor, *g_tamanho;
%}

%union {
  char *str;
  int   num;
}

// tokens que carregam string
%token <str> PECA_TYPE STRING IDENTIFIER
%token <str> TECIDO_VAL COR_VAL TAMANHO_VAL

// keywords e operadores
%token CREATE TECIDO_KW COR_KW TAMANHO_KW
%token CORTAR COSTURAR AJUSTAR FINALIZAR EM PARA
%token <num> NUMBER

%start program

%%

// programa é zero ou mais unidades
program:
    /* vazio */
  | program unit
  ;

// uma unidade: CREATE, tipo de peça, nome, abre chaves, 3 atributos, fecha chave, processos
unit:
    CREATE PECA_TYPE STRING '{'
      {
        unit_count++;
        g_peca = $2;
        g_nome = $3;
        printf("\n=== Unidade %d: %s \"%s\" ===\n",
               unit_count, g_peca, g_nome);
      }
    attr_tec
    attr_cor
    attr_tam
    '}'
    processes
      {
        printf("Created %s named \"%s\"\n", g_peca, g_nome);
      }
  ;

// cada atributo em sua própria produção, com $3 corretíssimo
attr_tec:
    TECIDO_KW '=' TECIDO_VAL ';'
      {
        g_tecido = $3;
        printf("Define tecido: %s\n", g_tecido);
      }
  ;

attr_cor:
    COR_KW '=' COR_VAL ';'
      {
        g_cor = $3;
        printf("Define cor: %s\n", g_cor);
      }
  ;

attr_tam:
    TAMANHO_KW '=' TAMANHO_VAL ';'
      {
        g_tamanho = $3;
        printf("Define tamanho: %s\n", g_tamanho);
      }
  ;

// zero ou mais processos após a chave
processes:
    /* vazio */
  | processes process
  ;

process:
    CORTAR IDENTIFIER EM IDENTIFIER ';'
      { printf(" → Corta %s em %s\n", $2, $4); }
  | COSTURAR IDENTIFIER ';'
      { printf(" → Costura %s\n", $2); }
  | AJUSTAR IDENTIFIER PARA TAMANHO_VAL ';'
      { printf(" → Ajusta %s para %s\n", $2, $4); }
  | FINALIZAR IDENTIFIER ';'
      { printf(" → Finaliza %s\n", $2); }
  ;

%%

int main(void) {
  if (yyparse() == 0) {
    printf("\n=== Program complete ===\n");
  }
  return 0;
}

void yyerror(const char *s) {
  fprintf(stderr, "Erro sintático: %s\n", s);
}
