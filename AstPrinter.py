from Expr import Expr, Visitor, Binary, Unary, Literal, Grouping
from Token import Token
from TokenType import tokenType

class AstPrinter(Visitor):
    def parenthesize(self, name: str, *exprs):
        builder = "(" + name
        for expr in exprs:
            builder += " "
            builder += expr.accept(self)
        builder += ")"
        return builder

    def print(self, expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitLiteralExpr(self, expr: Literal):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

expression = Binary(
                Unary(
                    Token(tokenType.MINUS, "-", None, 1), 
                    Literal(123)
                ),
                Token(tokenType.STAR, "*", None, 1),
                Grouping(Literal(47.67))
            )

obj = AstPrinter()
print(obj.print(expression))


