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
        for type_  in  types:
            if self.check(type_):
                self.advance()
                return True
        return False
    def expect(self, type_, message):
        if self.check(type_):
           return self.advance()  
        raise ParseError(message, self.peek().line) 
    def expression(self):
        return self.equality()

    def equality(self):
        left = self.comparison()
        while self.match(TokenType.EQ_EQ, TokenType.NOT_EQ):
            operator = self.previous().type
            right = self.comparison()
            left = Binary(left, operator, right)
        return left

    def comparison(self):
        left = self.term()
        while self.match(TokenType.LT, TokenType.LT_EQ, TokenType.GT, TokenType.GT_EQ):
            operator = self.previous().type
            right = self.term()
            left = Binary(left, operator, right)
        return left

    def term(self):
        left = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().type
            right = self.factor()
            left = Binary(left, operator, right)
        return left

    def factor(self):
        left = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous().type
            right = self.unary()
            left = Binary(left, operator, right)
        return left

    def unary(self):
        if self.match(TokenType.MINUS):
            operator = self.previous().type
            operand = self.unary()
            return Unary(operator, operand)
        return self.postfix()

    def postfix(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LPAREN):
                if not isinstance(expr, Identifier):
                    raise ParseError("Can only call functions by name", self.previous().line)
                args = self.arguments()
                self.expect(TokenType.RPAREN, "Expected ')' after arguments")
                expr = Call(expr.name, args)
            elif self.match(TokenType.LBRACKET):
                index = self.expression()
                self.expect(TokenType.RBRACKET, "Expected ']' after index")
                expr = Index(expr, index)
            else:
                break
        return expr

    def arguments(self):
        args = []
        if not self.check(TokenType.RPAREN):
            args.append(self.expression())
            while self.match(TokenType.COMMA):
                args.append(self.expression())
        return args

    def primary(self):
        if self.match(TokenType.NUMBER_INT):
            return Literal(int(self.previous().value))
        if self.match(TokenType.NUMBER_FLOAT):
            return Literal(float(self.previous().value))
        if self.match(TokenType.STRING):
            return Literal(self.previous().value)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.NULL):
            return Literal(None)
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.previous().value)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                elements.append(self.expression())
                while self.match(TokenType.COMMA):
                    elements.append(self.expression())
            self.expect(TokenType.RBRACKET, "Expected ']' after array elements")
            return ArrayLiteral(elements)
        raise ParseError("Expected expression", self.peek().line)                                     
    