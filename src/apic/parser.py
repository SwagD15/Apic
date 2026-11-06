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
    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return Program(statements)

    def declaration(self):
        if self.match(TokenType.THO):
            return self.var_declaration(False)
        if self.match(TokenType.CONST):
            return self.var_declaration(True)
        if self.match(TokenType.FUN):
            return self.function_declaration()
        return self.statement()

    def var_declaration(self, is_const):
        name = self.expect(TokenType.IDENTIFIER, "Expected variable name").value
        if self.match(TokenType.LBRACKET):          # array form: tho x[] = [1, 2];
            self.expect(TokenType.RBRACKET, "Expected ']' in array declaration")
        self.expect(TokenType.EQ, "Expected '=' after variable name")
        value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after declaration")
        return VarDecl(name, value, is_const)

    def function_declaration(self):
        name = self.expect(TokenType.IDENTIFIER, "Expected function name").value
        self.expect(TokenType.LPAREN, "Expected '(' after function name")
        params = self.parameters()
        self.expect(TokenType.RPAREN, "Expected ')' after parameters")
        body = self.block()
        return Function(name, params, body)

    def parameters(self):
        params = []
        if not self.check(TokenType.RPAREN):
            params.append(self.expect(TokenType.IDENTIFIER, "Expected parameter name").value)
            while self.match(TokenType.COMMA):
                params.append(self.expect(TokenType.IDENTIFIER, "Expected parameter name").value)
        return params
    def statement(self):
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.LOOP):
            return self.loop_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.check(TokenType.LBRACE):
            return self.block()
        return self.assignment_or_expression_statement()

    def assignment_or_expression_statement(self):
        expr = self.expression()
        if self.match(TokenType.EQ):
            if not isinstance(expr, (Identifier, Index)):
                raise ParseError("Invalid assignment target", self.previous().line)
            value = self.expression()
            self.expect(TokenType.SEMICOLON, "Expected ';' after assignment")
            return Assign(expr, value)
        self.expect(TokenType.SEMICOLON, "Expected ';' after expression")
        return ExprStmt(expr)

    def block(self):
        self.expect(TokenType.LBRACE, "Expected '{'")
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.expect(TokenType.RBRACE, "Expected '}' to close block")
        return Block(statements)

    def return_statement(self):
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after return")
        return Return(value)    
    def if_statement(self):
        self.expect(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after condition")
        then_block = self.block()

        elseifs = []
        while self.match(TokenType.ELSEIF):
            self.expect(TokenType.LPAREN, "Expected '(' after 'elseif'")
            cond = self.expression()
            self.expect(TokenType.RPAREN, "Expected ')' after condition")
            elseifs.append((cond, self.block()))

        else_block = None
        if self.match(TokenType.ELSE):
            else_block = self.block()

        return If(condition, then_block, elseifs, else_block)

    def loop_statement(self):
        self.expect(TokenType.LPAREN, "Expected '(' after 'loop'")

        target = self.expression()
        if not isinstance(target, Identifier):
            raise ParseError("Loop initializer must assign to a variable", self.previous().line)
        self.expect(TokenType.EQ, "Expected '=' in loop initializer")
        initializer = Assign(target, self.expression())
        self.expect(TokenType.SEMICOLON, "Expected ';' after loop initializer")

        condition = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected ';' after loop condition")

        incr_target = self.expression()
        if self.match(TokenType.PLUS_PLUS):
            increment = Increment(incr_target, TokenType.PLUS_PLUS)
        elif self.match(TokenType.MINUS_MINUS):
            increment = Increment(incr_target, TokenType.MINUS_MINUS)
        else:
            raise ParseError("Expected '++' or '--' in loop increment", self.peek().line)
        self.expect(TokenType.RPAREN, "Expected ')' after loop clauses")

        body = self.block()
        return Loop(initializer, condition, increment, body)        