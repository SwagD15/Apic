from apic.tokens import TokenType, KEYWORDS, Token

class LexerError(Exception):
    def __init__(self, message, line):
        self.message = message
        self.line = line
        super().__init__(f"{message} at line {line}")

class Lexer:

    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1

    # --- core helpers ---
    def peek(self):
        if self.pos >= len(self.source):
            return None   
        return self.source[self.pos]    
    def peek_next(self):
        if self.pos + 1 >= len(self.source):
            return None
        return self.source[self.pos + 1]

    def advance(self):
        char = self.source[self.pos]
        self.pos += 1
        if char == "\n":
            self.line += 1
        return char    
    def match(self, expected):
        if self.peek() != expected:
            return False
        self.advance()
        return True  
    def is_at_end(self):
        return self.pos >= len(self.source)
    # --- skipping ---
    def skip_whitespaces(self):
        while not self.is_at_end() and self.peek() in (" ", "\t", "\n", "\r"):
            self.advance()
    def skip_comment(self):
        start_line = self.line

        # consume the opening "##"
        self.advance()
        self.advance()

        while not (self.peek() == "#" and self.peek_next() == "#"):
             if self.is_at_end():
                raise LexerError("Unterminated comment", start_line)
             self.advance()

        # consume the closing "##"
        self.advance()
        self.advance() 
    # --- scanning individual token types ---
    def scan_number(self):
        start = self.pos

        # read the integer part
        while not self.is_at_end() and self.peek().isdigit():
            self.advance()

        is_float = False

        # a '.' only counts as a decimal point if a digit follows it
        if self.peek() == "." and self.peek_next() is not None and self.peek_next().isdigit():
            is_float = True
            self.advance()  # consume the '.'

            while not self.is_at_end() and self.peek().isdigit():
                self.advance()

            # a second decimal point like 1.2.3 is an error
            if self.peek() == "." and self.peek_next() is not None and self.peek_next().isdigit():
                raise LexerError("Invalid number: multiple decimal points", self.line)

        value = self.source[start:self.pos]
        token_type = TokenType.NUMBER_FLOAT if is_float else TokenType.NUMBER_INT
        return Token(token_type, value, self.line)
    def scan_string(self):
        start_line = self.line

        # consume the opening quote
        self.advance()

        start = self.pos

        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == "\n":
                raise LexerError("Unterminated string", start_line)
            self.advance()

        if self.is_at_end():
            raise LexerError("Unterminated string", start_line)

        value = self.source[start:self.pos]

        # consume the closing quote
        self.advance()

        return Token(TokenType.STRING, value, start_line)         
    def scan_identifier_or_keyword(self):
        start = self.pos

        while not self.is_at_end() and (self.peek().isalnum() or self.peek() == "_"):
            self.advance()

        word = self.source[start:self.pos]
        token_type = KEYWORDS.get(word, TokenType.IDENTIFIER)

        return Token(token_type, word, self.line)   
    def scan_operator_or_punctuation(self):
        line = self.line
        char = self.advance()

        punctuation = {
           "(": TokenType.LPAREN,
           ")": TokenType.RPAREN,
           "{": TokenType.LBRACE,
           "}": TokenType.RBRACE,
           "[": TokenType.LBRACKET,
           "]": TokenType.RBRACKET,
           ",": TokenType.COMMA,
           ";": TokenType.SEMICOLON,
        }
        if char in punctuation:
            return Token(punctuation[char],char,line)
        # operators that may be one or two characters (check two-char form first)
        if char == "=":
            if self.match("="):
                return Token(TokenType.EQ_EQ,"==",line)
            return Token(TokenType.EQ,"=",line)
        if char == "!":
            if self.match("="):
                return Token(TokenType.NOT_EQ,"!=",line)
            raise LexerError("Unexpected character '!' (did you mean '!='?)", line)
        if char == "<":
            if self.match("="):
                return Token(TokenType.LT_EQ,"<=",line)
            return Token(TokenType.LT,"<",line)
        if char == ">":
            if self.match("="):
                return Token(TokenType.GT_EQ,">=",line)
            return Token(TokenType.GT,">", line)
        if char == "+":
            if self.match("+"):
                return Token(TokenType.PLUS_PLUS,"++",line)
            return Token(TokenType.PLUS,"+",line)
        if char == "-" :
            if self.match("-"):
                return Token(TokenType.MINUS_MINUS,"--",line)
            return Token(TokenType.MINUS,"-",line)
        # single-character operators
        if char == "*":
            return Token(TokenType.STAR,"*",line)
        if char == "/":
            return Token(TokenType.SLASH,"/",line)
        raise LexerError(f"Unexpected character '{char}'", line)
 # --- main entry point ---
    def tokenize(self):
        tokens = []

        while not self.is_at_end():
            self.skip_whitespaces()

            if self.is_at_end():
                break

            char = self.peek()

            # comment: "##" ... "##"
            if char == "#" and self.peek_next() == "#":
                self.skip_comment()
                continue

            if char.isdigit():
                tokens.append(self.scan_number())
            elif char == '"':
                tokens.append(self.scan_string())
            elif char.isalpha() or char == "_":
                tokens.append(self.scan_identifier_or_keyword())
            else:
                tokens.append(self.scan_operator_or_punctuation())

        tokens.append(Token(TokenType.EOF, None, self.line))
        return tokens
# if __name__ == "__main__":
#     source = '''## calculate sum ##
# tho x = 10;
# tho y = 20.5;
# if (x < y) {
#     outf("y is bigger");
# }'''
#     for tok in Lexer(source).tokenize():
#         print(tok)                                                                           