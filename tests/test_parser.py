from pprint import pprint
from apic.lexer import Lexer
from apic.parser import Parser

#tokens = Lexer("2 + 3 * 4").tokenize()
#tokens = Lexer("10 - 5 - 2").tokenize()
#tokens = Lexer("-5").tokenize()
#tokens = Lexer("2+").tokenize()
#tokens = Lexer("x[0]").tokenize()
#tokens = Lexer("add(2, 3)").tokenize()
#tokens = Lexer("(2 + 3) * 4").tokenize()
#tokens = Lexer("[1, 2, 3]").tokenize()
tokens = Lexer(" ").tokenize()
pprint(Parser(tokens).expression())