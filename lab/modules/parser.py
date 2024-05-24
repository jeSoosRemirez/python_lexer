from constants.tokens import *
from constants.nodes import *
from modules.ast_nodes import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message=None):
        raise Exception(message or "Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type} but got {self.current_token.type}")

    def factor(self):
        token = self.current_token

        if token.type == TOKEN_INT:
            self.eat(TOKEN_INT)
            return NumNode(token.value)
        elif token.type == TOKEN_LPAREN:
            self.eat(TOKEN_LPAREN)
            node = self.expr()
            self.eat(TOKEN_RPAREN)
            return node
        elif token.type == TOKEN_STRING:
            self.eat(TOKEN_STRING)
            return StringNode(token.value)
        elif token.type == TOKEN_ID:
            self.eat(TOKEN_ID)
            return IdNode(token.value)
        else:
            self.error()

    def term(self):
        node = self.factor()

        while self.current_token.type in (TOKEN_MUL, TOKEN_DIV):
            token = self.current_token
            if token.type == TOKEN_MUL:
                self.eat(TOKEN_MUL)
            elif token.type == TOKEN_DIV:
                self.eat(TOKEN_DIV)

            node = BinOpNode(left=node, op=token.type, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (TOKEN_PLUS, TOKEN_MINUS):
            token = self.current_token
            if token.type == TOKEN_PLUS:
                self.eat(TOKEN_PLUS)
            elif token.type == TOKEN_MINUS:
                self.eat(TOKEN_MINUS)

            node = BinOpNode(left=node, op=token.type, right=self.term())

        return node

    def condition(self):
        left = self.expr()
        token = self.current_token

        if token.type in (TOKEN_EQ, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE):
            self.eat(token.type)
            right = self.expr()
            return ConditionNode(left, token.type, right)
        else:
            self.error("Invalid condition syntax")

    def statement(self):
        if self.current_token.type == TOKEN_IF:
            self.eat(TOKEN_IF)
            self.eat(TOKEN_LPAREN)
            condition = self.condition()
            self.eat(TOKEN_RPAREN)
            self.eat(TOKEN_LBRACE)
            true_block = self.parse_statements()
            self.eat(TOKEN_RBRACE)

            false_block = None
            if self.current_token.type == TOKEN_ELSE:
                self.eat(TOKEN_ELSE)
                self.eat(TOKEN_LBRACE)
                false_block = self.parse_statements()
                self.eat(TOKEN_RBRACE)

            return IfNode(condition, true_block, false_block)
        elif self.current_token.type == TOKEN_RETURN:
            self.eat(TOKEN_RETURN)
            value = self.expr()
            self.eat(TOKEN_SEMI)
            return ReturnNode(value)
        else:
            expr = self.expr()
            self.eat(TOKEN_SEMI)
            return expr

    def parse_statements(self):
        statements = []
        while (
            self.current_token.type != TOKEN_RBRACE
            and self.current_token.type != TOKEN_EOF
        ):
            statements.append(self.statement())
        return statements

    def parse(self):
        return self.parse_statements()
