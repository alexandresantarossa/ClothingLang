import sys

# ----------------------
# Lexer (Tokenizador)
# ----------------------
class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

class Tokenizador:
    def __init__(self, fonte):
        self.codigo = fonte
        self.pos = 0
        self.linha = 1
        self.proximo = None
        self.keywords = {
            "CREATE":"CREATE","CORTAR":"CORTAR","COSTURAR":"COSTURAR",
            "AJUSTAR":"AJUSTAR","FINALIZAR":"FINALIZAR","EM":"EM","PARA":"PARA",
            "tecido":"TECIDO","cor":"COR","tamanho":"TAMANHO"
        }
        self.types = {
            "algodao":"TECIDO_TYPE","jeans":"TECIDO_TYPE","seda":"TECIDO_TYPE",
            "malha":"TECIDO_TYPE","la":"TECIDO_TYPE","linho":"TECIDO_TYPE",
            "azul":"COR_TYPE","preto":"COR_TYPE","branco":"COR_TYPE",
            "vermelho":"COR_TYPE","verde":"COR_TYPE","amarelo":"COR_TYPE",
            "rosa":"COR_TYPE","roxo":"COR_TYPE","laranja":"COR_TYPE",
            "PP":"TAMANHO_TYPE","P":"TAMANHO_TYPE","M":"TAMANHO_TYPE",
            "G":"TAMANHO_TYPE","GG":"TAMANHO_TYPE",
            "camiseta":"PECA_TYPE","calca":"PECA_TYPE","blusa":"PECA_TYPE",
            "saia":"PECA_TYPE","vestido":"PECA_TYPE","bermuda":"PECA_TYPE"
        }
        self.selecionarProximo()

    def selecionarProximo(self):
        while self.pos < len(self.codigo) and self.codigo[self.pos].isspace():
            if self.codigo[self.pos] == '\n': self.linha += 1
            self.pos += 1
        if self.pos >= len(self.codigo):
            self.proximo = Token("EOF", None, self.linha); return

        c = self.codigo[self.pos]
        if c in "{}=;":
            m = {'{':'ABRE_CHAVE','}':'FECHA_CHAVE','=':'IGUAL',';':'PV'}
            self.proximo = Token(m[c], c, self.linha)
            self.pos += 1; return
        if c == '"':
            self.pos += 1
            start = self.pos
            while self.pos < len(self.codigo) and self.codigo[self.pos] != '"':
                self.pos += 1
            val = self.codigo[start:self.pos]
            self.pos += 1
            self.proximo = Token("STRING", val, self.linha); return
        if c.isalpha():
            start = self.pos
            while (self.pos < len(self.codigo) and
                   (self.codigo[self.pos].isalnum() or self.codigo[self.pos]=='_')):
                self.pos += 1
            ident = self.codigo[start:self.pos]
            if ident in self.keywords: tipo = self.keywords[ident]
            elif ident in self.types: tipo = self.types[ident]
            else: tipo = "IDENT"
            self.proximo = Token(tipo, ident, self.linha)
            return
        raise ValueError(f"Caractere inválido '{c}' na linha {self.linha}")

# ----------------------
# AST Nodes
# ----------------------
class Node:
    def Evaluate(self): pass

class CreateNode(Node):
    def __init__(self, peca,nome,tecido,cor,tamanho):
        self.peca,self.nome,self.tecido,self.cor,self.tamanho = peca,nome,tecido,cor,tamanho
    def Evaluate(self):
        print(f"\n=== Unidade: {self.peca} \"{self.nome}\" ===")
        print(f"Define tecido: {self.tecido}")
        print(f"Define cor: {self.cor}")
        print(f"Define tamanho: {self.tamanho}")
        print(f"Created {self.peca} named \"{self.nome}\"")

class CutNode(Node):
    def __init__(self,id1,id2): self.id1,self.id2 = id1,id2
    def Evaluate(self): print(f"→ Corta {self.id1} em {self.id2}")

class SewNode(Node):
    def __init__(self,id1): self.id1 = id1
    def Evaluate(self): print(f"→ Costura {self.id1}")

class AdjustNode(Node):
    def __init__(self,id1,size): self.id1,self.size = id1,size
    def Evaluate(self): print(f"→ Ajusta {self.id1} para {self.size}")

class FinalizeNode(Node):
    def __init__(self,id1): self.id1 = id1
    def Evaluate(self): print(f"→ Finaliza {self.id1}")

# ----------------------
# Parser
# ----------------------
class Parser:
    def __init__(self, fonte):
        self.lexer = Tokenizador(fonte)
        self.cur = self.lexer.proximo

    def eat(self, tipo):
        if self.cur.tipo == tipo:
            self.lexer.selecionarProximo()
            self.cur = self.lexer.proximo
        else:
            raise ValueError(f"Esperado {tipo} mas veio {self.cur.tipo}")

    def parse(self):
        stmts = []
        while self.cur.tipo != 'EOF':
            stmts.extend(self.parseUnit())
        return stmts

    def parseUnit(self):
        self.eat("CREATE")
        peca = self.cur.valor; self.eat("PECA_TYPE")
        nome = self.cur.valor; self.eat("STRING")
        self.eat("ABRE_CHAVE")
        self.eat("TECIDO"); self.eat("IGUAL")
        tecido = self.cur.valor; self.eat("TECIDO_TYPE"); self.eat("PV")
        self.eat("COR");    self.eat("IGUAL")
        cor = self.cur.valor;    self.eat("COR_TYPE");    self.eat("PV")
        self.eat("TAMANHO");self.eat("IGUAL")
        tamanho = self.cur.valor;self.eat("TAMANHO_TYPE");self.eat("PV")
        self.eat("FECHA_CHAVE")

        seq = [CreateNode(peca,nome,tecido,cor,tamanho)]
        while self.cur.tipo in ("CORTAR","COSTURAR","AJUSTAR","FINALIZAR"):
            if self.cur.tipo=="CORTAR":
                self.eat("CORTAR")
                id1=self.cur.valor; self.eat("IDENT")
                self.eat("EM")
                id2=self.cur.valor; self.eat("IDENT")
                self.eat("PV")
                seq.append(CutNode(id1,id2))
            elif self.cur.tipo=="COSTURAR":
                self.eat("COSTURAR")
                id1=self.cur.valor; self.eat("IDENT"); self.eat("PV")
                seq.append(SewNode(id1))
            elif self.cur.tipo=="AJUSTAR":
                self.eat("AJUSTAR")
                id1=self.cur.valor; self.eat("IDENT")
                self.eat("PARA")
                size=self.cur.valor; self.eat("TAMANHO_TYPE")
                self.eat("PV")
                seq.append(AdjustNode(id1,size))
            else:
                self.eat("FINALIZAR")
                id1=self.cur.valor; self.eat("IDENT"); self.eat("PV")
                seq.append(FinalizeNode(id1))
        return seq

# ----------------------
# Main
# ----------------------
def main():
    if len(sys.argv)!=2:
        print("Uso: python3 clothinglang_compiler.py <arquivo.cl>")
        return
    fonte = open(sys.argv[1], encoding='utf-8').read()
    prog = Parser(fonte).parse()
    for s in prog: s.Evaluate()
    print("\n=== Program complete ===")

if __name__=="__main__":
    main()
