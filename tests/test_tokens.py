from apic.tokens import TokenType, KEYWORDS, Token


# Test enum values
print(TokenType.NUMBER_INT)
print(TokenType.PLUS)
print(TokenType.THO)


# Test keywords
print(KEYWORDS["tho"])
print(KEYWORDS["fun"])
print(KEYWORDS["true"])


# Test Token
token = Token(TokenType.NUMBER_INT, "123", 1)

print(token)
print(token.type)
print(token.value)
print(token.line)
