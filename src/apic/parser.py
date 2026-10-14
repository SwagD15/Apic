from apic.tokens import TokenType
from apic.ast_nodes import (
    Literal, Identifier, Unary, Binary, Call, Index, ArrayLiteral,
    VarDecl, Assign, ExprStmt, Block, If, Loop, Increment, Function, Return, Program
)


class ParseError(Exception):
    def __init__(self, message, line):
        self.message = message
        self.line = line
        super().__init__(f"{message} at line {line}")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    def peek(self):
        return self.tokens[self.pos]
    def previous(self):
        return self.tokens[self.pos -1]
    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    def advance(self):
        if not self.is_at_end():
            self.pos +=1
        return self.previous()
    def check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type == type_    
    def match(self,*types):
        for types_  in  types:
            if self.check(type_):
                self.advance()
                return True
        return False
    def expect(self, type_, message):
        if self.check(type_):
            self.advance()
        raise ParseError(message, self.peek().line)                                  
    pass