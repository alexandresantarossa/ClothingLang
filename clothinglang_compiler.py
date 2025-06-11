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
            "CREATE":"CREATE", "CORTAR":"CORTAR", "COSTURAR":"COSTURAR",
            "AJUSTAR":"AJUSTAR", "FINALIZAR":"FINALIZAR", "EM":"EM", "PARA":"PARA",
            "tecido":"TECIDO", "cor":"COR", "tamanho":"TAMANHO",
            "SE":"SE", "SENAO":"SENAO", "ENQUANTO":"ENQUANTO"
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
            if self.codigo[self.pos] == '\n':
                self.linha += 1
            self.pos += 1
        if self.pos >= len(self.codigo):
            self.proximo = Token("EOF", None, self.linha)
            return

        c = self.codigo[self.pos]
        if c in "{}=;":
            mapa = {'{':'ABRE_CHAVE','}':'FECHA_CHAVE','=':'IGUAL',';':'PV'}
            self.proximo = Token(mapa[c], c, self.linha)
            self.pos += 1
            return

        if c == '"':
            self.pos += 1
            início = self.pos
            while self.pos < len(self.codigo) and self.codigo[self.pos] != '"':
                self.pos += 1
            val = self.codigo[início:self.pos]
            self.pos += 1
            self.proximo = Token("STRING", val, self.linha)
            return

        if c.isalpha():
            início = self.pos
            while (self.pos < len(self.codigo)
                   and (self.codigo[self.pos].isalnum() or self.codigo[self.pos]=='_')):
                self.pos += 1
            ident = self.codigo[início:self.pos]
            if ident in self.keywords:
                tipo = self.keywords[ident]
            elif ident in self.types:
                tipo = self.types[ident]
            else:
                tipo = "IDENT"
            self.proximo = Token(tipo, ident, self.linha)
            return

        if c.isdigit():
            início = self.pos
            while self.pos < len(self.codigo) and self.codigo[self.pos].isdigit():
                self.pos += 1
            num = int(self.codigo[início:self.pos])
            self.proximo = Token("NUMBER", num, self.linha)
            return

        raise ValueError(f"Caractere inválido '{c}' na linha {self.linha}")

# ----------------------
# AST Nodes
# ----------------------
class Node:
    def Evaluate(self): pass

class CreateNode(Node):
    def __init__(self, peca, nome, tecido, cor, tamanho):
        self.peca, self.nome = peca, nome
        self.tecido, self.cor, self.tamanho = tecido, cor, tamanho
    def Evaluate(self):
        global LAST_PIECE
        LAST_PIECE = self
        print(f"\n=== Unidade: {self.peca} \"{self.nome}\" ===")
        print(f"Define tecido: {self.tecido}")
        print(f"Define cor: {self.cor}")
        print(f"Define tamanho: {self.tamanho}")
        print(f"Created {self.peca} named \"{self.nome}\"")

class IfNode(Node):
    def __init__(self, attr, val, true_cmds, false_cmds):
        self.attr = attr
        self.val = val
        self.true_cmds = true_cmds
        self.false_cmds = false_cmds
    def Evaluate(self):
        piece = LAST_PIECE
        current = getattr(piece, self.attr)
        if current == self.val:
            for c in self.true_cmds: c.Evaluate()
        else:
            for c in self.false_cmds: c.Evaluate()

class WhileNode(Node):
    def __init__(self, attr, val, cmds):
        self.attr = attr
        self.val = val
        self.cmds = cmds
    def Evaluate(self):
        piece = LAST_PIECE
        while getattr(piece, self.attr) == self.val:
            for c in self.cmds: c.Evaluate()

class CutNode(Node):
    def __init__(self, id1, id2): self.id1, self.id2 = id1, id2
    def Evaluate(self): print(f"→ Corta {self.id1} em {self.id2}")

class SewNode(Node):
    def __init__(self, id1): self.id1 = id1
    def Evaluate(self): print(f"→ Costura {self.id1}")

class AdjustNode(Node):
    def __init__(self, id1, size): self.id1, self.size = id1, size
    def Evaluate(self):
        print(f"→ Ajusta {self.id1} para {self.size}")
        LAST_PIECE.tamanho = self.size

class FinalizeNode(Node):
    def __init__(self, id1): self.id1 = id1
    def Evaluate(self): print(f"→ Finaliza {self.id1}")

LAST_PIECE = None

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
            raise ValueError(f"Esperado {tipo} mas veio {self.cur.tipo} (linha {self.cur.linha})")

    def parse(self):
        nodes = []
        while self.cur.tipo != 'EOF':
            if self.cur.tipo == "CREATE":
                nodes.extend(self.parseCreate())
            elif self.cur.tipo == "SE":
                nodes.append(self.parseIf())
            elif self.cur.tipo == "ENQUANTO":
                nodes.append(self.parseWhile())
            else:
                nodes.append(self.parseCommand())
        return nodes

    def parseCreate(self):
        self.eat("CREATE")
        p = self.cur.valor; self.eat("PECA_TYPE")
        n = self.cur.valor; self.eat("STRING")
        self.eat("ABRE_CHAVE")

        self.eat("TECIDO"); self.eat("IGUAL")
        t = self.cur.valor; self.eat(self.cur.tipo); self.eat("PV")

        self.eat("COR"); self.eat("IGUAL")
        c = self.cur.valor; self.eat(self.cur.tipo); self.eat("PV")

        self.eat("TAMANHO"); self.eat("IGUAL")
        z = self.cur.valor; self.eat(self.cur.tipo); self.eat("PV")

        self.eat("FECHA_CHAVE")

        seq = [CreateNode(p, n, t, c, z)]
        while self.cur.tipo in ("CORTAR","COSTURAR","AJUSTAR","FINALIZAR"):
            seq.append(self.parseCommand())
        return seq

    def parseCommand(self):
        t = self.cur.tipo
        if t == "CORTAR":
            self.eat("CORTAR"); id1=self.cur.valor; self.eat("IDENT")
            self.eat("EM"); id2=self.cur.valor; self.eat("IDENT"); self.eat("PV")
            return CutNode(id1, id2)
        if t == "COSTURAR":
            self.eat("COSTURAR"); id1=self.cur.valor; self.eat("IDENT"); self.eat("PV")
            return SewNode(id1)
        if t == "AJUSTAR":
            self.eat("AJUSTAR"); id1=self.cur.valor; self.eat("IDENT")
            self.eat("PARA"); size=self.cur.valor; self.eat("TAMANHO_TYPE"); self.eat("PV")
            return AdjustNode(id1, size)
        if t == "FINALIZAR":
            self.eat("FINALIZAR"); id1=self.cur.valor; self.eat("IDENT"); self.eat("PV")
            return FinalizeNode(id1)
        raise ValueError(f"Processo inesperado: {t} (linha {self.cur.linha})")

    def parseIf(self):
        self.eat("SE")
        attr = self.cur.valor; self.eat(self.cur.tipo)
        self.eat("IGUAL"); self.eat("IGUAL")
        val = self.cur.valor; self.eat(self.cur.tipo)
        cond = True
        self.eat("ABRE_CHAVE")
        tr = []
        while self.cur.tipo in ("CORTAR","COSTURAR","AJUSTAR","FINALIZAR"):
            tr.append(self.parseCommand())
        self.eat("FECHA_CHAVE")
        self.eat("SENAO")
        self.eat("ABRE_CHAVE")
        fl = []
        while self.cur.tipo in ("CORTAR","COSTURAR","AJUSTAR","FINALIZAR"):
            fl.append(self.parseCommand())
        self.eat("FECHA_CHAVE")
        return IfNode(attr, val, tr, fl)

    def parseWhile(self):
        self.eat("ENQUANTO")
        attr = self.cur.valor; self.eat(self.cur.tipo)
        self.eat("IGUAL"); self.eat("IGUAL")
        val = self.cur.valor; self.eat(self.cur.tipo)
        cond = True
        self.eat("ABRE_CHAVE")
        cmds = []
        while self.cur.tipo in ("CORTAR","COSTURAR","AJUSTAR","FINALIZAR"):
            cmds.append(self.parseCommand())
        self.eat("FECHA_CHAVE")
        return WhileNode(attr, val, cmds)

# ----------------------
# Main
# ----------------------
def main():
    if len(sys.argv) != 2:
        print("Uso: python3 clothinglang_compiler.py <arquivo.cl>")
        return
    fonte = open(sys.argv[1], encoding='utf-8').read()
    prog = Parser(fonte).parse()
    for node in prog:
        node.Evaluate()
    print("\n=== Program complete ===")

if __name__ == "__main__":
    main()
