from apic.lexer import Lexer, LexerError
from apic.tokens import TokenType


def test_integers():
    lexer = Lexer("123 456 789")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.NUMBER_INT
    assert tokens[0].value == "123"

    assert tokens[1].type == TokenType.NUMBER_INT
    assert tokens[1].value == "456"

    assert tokens[2].type == TokenType.NUMBER_INT
    assert tokens[2].value == "789"

    assert tokens[3].type == TokenType.EOF

    print("✓ integer test passed")


def test_floats():
    lexer = Lexer("3.14 10.5 0.25")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.NUMBER_FLOAT
    assert tokens[0].value == "3.14"

    assert tokens[1].type == TokenType.NUMBER_FLOAT
    assert tokens[1].value == "10.5"

    assert tokens[2].type == TokenType.NUMBER_FLOAT
    assert tokens[2].value == "0.25"

    assert tokens[3].type == TokenType.EOF

    print("✓ float test passed")


def test_strings():
    lexer = Lexer('"hello" "world"')
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello"

    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "world"

    assert tokens[2].type == TokenType.EOF

    print("✓ string test passed")


def test_identifiers():
    lexer = Lexer("hello world my_variable _test")
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "hello"

    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "world"

    assert tokens[2].type == TokenType.IDENTIFIER
    assert tokens[2].value == "my_variable"

    assert tokens[3].type == TokenType.IDENTIFIER
    assert tokens[3].value == "_test"

    print("✓ identifier test passed")


def test_keywords():
    source = "tho const fun return if elseif else loop true false null"

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected = [
        TokenType.THO,
        TokenType.CONST,
        TokenType.FUN,
        TokenType.RETURN,
        TokenType.IF,
        TokenType.ELSEIF,
        TokenType.ELSE,
        TokenType.LOOP,
        TokenType.TRUE,
        TokenType.FALSE,
        TokenType.NULL,
    ]

    for token, expected_type in zip(tokens, expected):
        assert token.type == expected_type

    assert tokens[-1].type == TokenType.EOF

    print("✓ keyword test passed")


def test_operators():
    source = "+ - * / = == != < <= > >= ++ --"

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected = [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.SLASH,
        TokenType.EQ,
        TokenType.EQ_EQ,
        TokenType.NOT_EQ,
        TokenType.LT,
        TokenType.LT_EQ,
        TokenType.GT,
        TokenType.GT_EQ,
        TokenType.PLUS_PLUS,
        TokenType.MINUS_MINUS,
        TokenType.EOF,
    ]

    actual = [token.type for token in tokens]

    assert actual == expected

    print("✓ operator test passed")


def test_punctuation():
    source = "( ) { } [ ] , ;"

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected = [
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.LBRACKET,
        TokenType.RBRACKET,
        TokenType.COMMA,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]

    actual = [token.type for token in tokens]

    assert actual == expected

    print("✓ punctuation test passed")


def test_comments():
    source = """
    tho x = 10;

    ## this is a comment ##
    
    tho y = 20;
    """

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected = [
        TokenType.THO,
        TokenType.IDENTIFIER,
        TokenType.EQ,
        TokenType.NUMBER_INT,
        TokenType.SEMICOLON,

        TokenType.THO,
        TokenType.IDENTIFIER,
        TokenType.EQ,
        TokenType.NUMBER_INT,
        TokenType.SEMICOLON,

        TokenType.EOF,
    ]

    actual = [token.type for token in tokens]

    assert actual == expected

    print("✓ comment test passed")


def test_whitespace():
    source = "   \t\n  tho   x   =   10   ;   "

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected = [
        TokenType.THO,
        TokenType.IDENTIFIER,
        TokenType.EQ,
        TokenType.NUMBER_INT,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]

    actual = [token.type for token in tokens]

    assert actual == expected

    print("✓ whitespace test passed")


def test_unterminated_string():
    lexer = Lexer('"hello')

    try:
        lexer.tokenize()
        assert False, "Expected LexerError"
    except LexerError as error:
        assert "Unterminated string" in str(error)

    print("✓ unterminated string test passed")


def test_unterminated_comment():
    lexer = Lexer("## hello world")

    try:
        lexer.tokenize()
        assert False, "Expected LexerError"
    except LexerError as error:
        assert "Unterminated comment" in str(error)

    print("✓ unterminated comment test passed")


def test_invalid_bang():
    lexer = Lexer("!")

    try:
        lexer.tokenize()
        assert False, "Expected LexerError"
    except LexerError as error:
        assert "did you mean '!='?" in str(error)

    print("✓ invalid ! test passed")


def test_invalid_number():
    lexer = Lexer("1.2.3")

    try:
        lexer.tokenize()
        assert False, "Expected LexerError"
    except LexerError as error:
        assert "multiple decimal points" in str(error)

    print("✓ invalid number test passed")


def test_complete_program():
    source = """
    tho x = 10;
    const y = 20;

    if x >= y {
        return false;
    } else {
        return true;
    }
    """

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    expected = [
        TokenType.THO,
        TokenType.IDENTIFIER,
        TokenType.EQ,
        TokenType.NUMBER_INT,
        TokenType.SEMICOLON,

        TokenType.CONST,
        TokenType.IDENTIFIER,
        TokenType.EQ,
        TokenType.NUMBER_INT,
        TokenType.SEMICOLON,

        TokenType.IF,
        TokenType.IDENTIFIER,
        TokenType.GT_EQ,
        TokenType.IDENTIFIER,
        TokenType.LBRACE,

        TokenType.RETURN,
        TokenType.FALSE,
        TokenType.SEMICOLON,

        TokenType.RBRACE,

        TokenType.ELSE,
        TokenType.LBRACE,

        TokenType.RETURN,
        TokenType.TRUE,
        TokenType.SEMICOLON,

        TokenType.RBRACE,

        TokenType.EOF,
    ]

    actual = [token.type for token in tokens]

    assert actual == expected

    print("✓ complete program test passed")


if __name__ == "__main__":
    test_integers()
    test_floats()
    test_strings()
    test_identifiers()
    test_keywords()
    test_operators()
    test_punctuation()
    test_comments()
    test_whitespace()
    test_unterminated_string()
    test_unterminated_comment()
    test_invalid_bang()
    test_invalid_number()
    test_complete_program()

    print()
    print("================================")
    print("All lexer tests passed!")
    print("================================")