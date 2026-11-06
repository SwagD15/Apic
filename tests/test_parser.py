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

# tokens = Lexer(" ").tokenize()
# pprint(Parser(tokens).expression())

#source = 'outf("hello");'
#source = 'tho x = 10 + 5;'
#source = ' x = 20;/x[0] = 5;'
#source = 'if (x > 10) { outf("big"); } else { outf("small"); }'
#source = 'loop(i = 0; i < 10; i++) { outf(i); }'
#source = 'fun add(a, b) { return a + b; }'

source = 'fun add(a, b) { return a + b; }'
pprint(Parser(Lexer(source).tokenize()).parse())