from constants.nodes import *


class ASTNode: ...


class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"


class NumNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumNode({self.value})"


class IfNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def __repr__(self):
        return f"IfNode(condition={self.condition}, true_block={self.true_block}, false_block={self.false_block})"


class ConditionNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"ConditionNode({self.left}, {self.op}, {self.right})"


class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ReturnNode({self.value})"


class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'StringNode("{self.value}")'


class IdNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdNode({self.name})"
