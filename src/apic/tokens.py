from enum import Enum, auto


class TokenType(Enum):
    # Literals
    NUMBER_INT = auto()
    NUMBER_FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Keywords
    THO = auto()        # variable declaration
    CONST = auto()
    FUN = auto()
    RETURN = auto()
    IF = auto()
    ELSEIF = auto()
    ELSE = auto()
    LOOP = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    # Operators
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    EQ = auto()          # =
    EQ_EQ = auto()       # ==
    NOT_EQ = auto()      # !=
    LT = auto()          # <
    LT_EQ = auto()       # <=
    GT = auto()          # >
    GT_EQ = auto()       # >=
    PLUS_PLUS = auto()   # ++
    MINUS_MINUS = auto() # --

    # Punctuation
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    SEMICOLON = auto()   # ;

    EOF = auto()


# Maps the literal text of a keyword to its TokenType.
# The lexer reads a full identifier first, then checks this dict
# to decide if it's actually a keyword.
KEYWORDS = {
    "tho": TokenType.THO,
    "const": TokenType.CONST,
    "fun": TokenType.FUN,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    "elseif": TokenType.ELSEIF,
    "else": TokenType.ELSE,
    "loop": TokenType.LOOP,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
}


class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value      # the actual text/number, e.g. "10", "x", "hello"
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line})"