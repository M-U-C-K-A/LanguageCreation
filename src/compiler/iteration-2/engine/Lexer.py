from re import match
from .Symbols import *



def scan(start: int, chars: str, regex: str) -> tuple[str, int]:
	"""
	Scan the **chars** from the **start** index to find a word who respect the **regex**
	:param start: The index where starting to search in **chars** with the **regex**.
	:param chars: The String where search for the **regex**.
	:param regex: The **regex** to search for.
	:return: [**word**: str, **end**: int] The **word** found by the regex and the index of the word's **end**.
	"""

	cChars = len(chars)

	for i in range(start, cChars):
		char = chars[i]

		if not match(regex, char):
			return chars[start:i], i - start - 1

	return chars[start:cChars], cChars - start - 1


def lexer(script: str) -> list[Token]:
	"""
	Transform the script input to a list of tokens.
	:param script: The script input of the compiler.
	"""

	tokens = []

	scriptLenght = len(script)

	i = 0

	while i < scriptLenght:
		char: str = script[i]

		if char in Symbol.IGNORES:
			i += 1
			continue

		elif script[i:i+2] == Symbol.EQUAL:
			tokens.append(Token(TokenType.OP, Symbol.EQUAL))
			i += 2

		elif char in Symbol.OPERATIONS:
			tokens.append(Token(TokenType.OP, char))

		elif char == Symbol.EOL:
			tokens.append(Token(TokenType.EOL, char))

		elif char in Symbol.BOXES:
			tokens.append(Token(TokenType.BOX, char))

		elif match("[_a-zA-Z]", char):
			word, end = scan(i, script, "[_a-zA-Z-0-9]")
			tokens.append(Token(TokenType.ID, word))
			i += end

		elif match("[.0-9]", char):
			number, end = scan(i, script, "[.0-9]")
			tokens.append(Token(TokenType.NUM, number))
			i += end

		elif char == Symbol.QUOT:
			string, end = scan(i + 1, script, "[^\"]")
			tokens.append(Token(TokenType.STR, string))
			i += end + 2

		else:
			raise Exception("Character \"" + char + "\" not allowed")

		i += 1

	# for t in tokens:
	# 	print(t)

	return tokens
