from constants.tokens import *


class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        if self.value:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        self.current_pos = 0

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        self.pos += 1
        self.current_pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        if self.current_char == "/" and (self.peek() == "/" or self.peek() == "*"):
            if self.peek() == "/":
                while self.current_char is not None and self.current_char != "\n":
                    self.advance()
                self.advance()
            elif self.peek() == "*":
                self.advance()  # Skip first '/'
                self.advance()  # Skip second '*'
                while self.current_char is not None:
                    if self.current_char == "*" and self.peek() == "/":
                        self.advance()
                        self.advance()
                        break
                    self.advance()
            self.skip_whitespace()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ""
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            result += self.current_char
            self.advance()
        return result

    def string(self):
        result = ""
        self.advance()  # skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == "\\":
                self.advance()
                if self.current_char == "n":
                    result += "\n"
                elif self.current_char == "t":
                    result += "\t"
                elif self.current_char == '"':
                    result += '"'
                else:
                    result += "\\" + self.current_char
            else:
                result += self.current_char
            self.advance()
        if self.current_char is None:
            raise Exception("Unterminated string")
        self.advance()  # skip the closing quote
        return result

    def get_next_token(self):
        self.skip_whitespace()
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == "/" and (self.peek() == "/" or self.peek() == "*"):
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                pos_start = self.current_pos
                num = self.integer()
                pos_end = self.current_pos
                return Token(TOKEN_INT, num, pos_start, pos_end)

            if self.current_char.isalpha():
                pos_start = self.current_pos
                id_str = self.identifier()
                pos_end = self.current_pos
                if id_str == "if":
                    return Token(TOKEN_IF, pos_start=pos_start, pos_end=pos_end)
                elif id_str == "else":
                    return Token(TOKEN_ELSE, pos_start=pos_start, pos_end=pos_end)
                elif id_str == "return":
                    return Token(TOKEN_RETURN, pos_start=pos_start, pos_end=pos_end)
                else:
                    return Token(TOKEN_ID, id_str, pos_start, pos_end)

            if self.current_char == '"':
                pos_start = self.current_pos
                return Token(
                    TOKEN_STRING,
                    self.string(),
                    pos_start=pos_start,
                    pos_end=self.current_pos,
                )

            if self.current_char == "+":
                pos_start = self.current_pos
                self.advance()
                return Token(TOKEN_PLUS, pos_start=pos_start, pos_end=self.current_pos)

            if self.current_char == "-":
                pos_start = self.current_pos
                self.advance()
                return Token(TOKEN_MINUS, pos_start=pos_start, pos_end=self.current_pos)

            if self.current_char == "*":
                pos_start = self.current_pos
                self.advance()
                return Token(TOKEN_MUL, pos_start=pos_start, pos_end=self.current_pos)

            if self.current_char == "/":
                pos_start = self.current_pos
                self.advance()
                return Token(TOKEN_DIV, pos_start=pos_start, pos_end=self.current_pos)

            if self.current_char == "(":
                pos_start = self.current_pos
                self.advance()
                return Token(
                    TOKEN_LPAREN, pos_start=pos_start, pos_end=self.current_pos
                )

            if self.current_char == ")":
                pos_start = self.current_pos
                self.advance()
                return Token(
                    TOKEN_RPAREN, pos_start=pos_start, pos_end=self.current_pos
                )

            if self.current_char == "{":
                pos_start = self.current_pos
                self.advance()
                return Token(
                    TOKEN_LBRACE, pos_start=pos_start, pos_end=self.current_pos
                )

            if self.current_char == "}":
                pos_start = self.current_pos
                self.advance()
                return Token(
                    TOKEN_RBRACE, pos_start=pos_start, pos_end=self.current_pos
                )

            if self.current_char == "=":
                pos_start = self.current_pos
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(
                        TOKEN_EQ, pos_start=pos_start, pos_end=self.current_pos
                    )
                else:
                    raise Exception("Expected = after =")

            if self.current_char == "!":
                pos_start = self.current_pos
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(
                        TOKEN_NE, pos_start=pos_start, pos_end=self.current_pos
                    )
                else:
                    raise Exception("Expected = after !")

            if self.current_char == "<":
                pos_start = self.current_pos
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(
                        TOKEN_LTE, pos_start=pos_start, pos_end=self.current_pos
                    )
                else:
                    return Token(
                        TOKEN_LT, pos_start=pos_start, pos_end=self.current_pos
                    )

            if self.current_char == ">":
                pos_start = self.current_pos
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(
                        TOKEN_GTE, pos_start=pos_start, pos_end=self.current_pos
                    )

                return Token(
                    TOKEN_GT, pos_start=pos_start, pos_end=self.current_pos
                )

            if self.current_char == ";":
                pos_start = self.current_pos
                self.advance()
                return Token(TOKEN_SEMI, pos_start=pos_start, pos_end=self.current_pos)

            self.error()

        return Token(TOKEN_EOF, pos_start=self.current_pos, pos_end=self.current_pos)
