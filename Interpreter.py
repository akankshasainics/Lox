from Expr import Visitor as eVisitor, Expr, Literal, Grouping, Unary, Binary, Variable, Assign, Logical
from Stmt import Visitor as sVisitor, Expression, Print, Stmt, Var, Block, If, While
from TokenType import tokenType
from Token import Token
from RunTimeException import RunTimeException
from Environment import Environment


class Interpreter(eVisitor, sVisitor):
    def __init__(self):
        self.environment = Environment()

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def isTruthy(self, obj: object) -> bool:
        if obj is None:
            return False
        if type(obj) ==  bool:
            return bool(obj)
        return True

    def checkNumberOperands(self, operator: Token,  left: object, right: object):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RunTimeException(operator, "Operands must be numbers.")

    def checkNumberOperand(self, operator: Token, operand: object):
        if type(operand) == float:
            return
        raise RunTimeException(operator, "Operand must be a number.")

    def visitUnaryExpr(self, expr: Unary):
        right: object = self.evaluate(expr.right)
        if expr.operator.type == tokenType.MINUS:
            return -float(right) 
        if expr.operator.type == tokenType.BANG:
            return not self.isTruthy(right)

    def isEqual(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False 
        return a.__eq__(b)

    def visitWhileStmt(self, stmt: While):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visitBinaryExpr(self, expr: Binary):
        left: object = self.evaluate(expr.left)
        right: object = self.evaluate(expr.right)

        # minus
        if expr.operator.type == tokenType.MINUS:
            self.checkNumberOperands(expr.operator, left, right);
            return float(left) - float(right)
        # divide
        if expr.operator.type == tokenType.SLASH:
            self.checkNumberOperands(expr.operator, left, right);
            if float(right) == 0.0:
                raise RunTimeException(expr.operator, "Error: Divison by zero")
            return float(left) / float(right)
        # multiply
        if expr.operator.type == tokenType.STAR:
            self.checkNumberOperands(expr.operator, left, right);
            return float(left)*float(right)
        # plus
        if expr.operator.type == tokenType.PLUS:
            if type(left) == float and type(right) == float:
                return float(left) + float(right)
            elif type(left) == str or type(right) == str:
                return self.stringify(left) + self.stringify(right)
            raise RunTimeException(expr.operator, "Operands must be two numbers or two strings")
        # greater >
        if expr.operator.type == tokenType.GREATER:
            self.checkNumberOperands(expr.operator, left, right);
            return float(left) > float(right)
        # greater equal >=
        if expr.operator.type == tokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right);
            return float(left) >=  float(right)
        # less <
        if expr.operator.type == tokenType.LESS:
            self.checkNumberOperands(expr.operator, left, right);
            return float(left) < float(right)
        # less equal <=
        if expr.operator.type == tokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right);
            return float(left) <= float(right)
        # Bang equal !=
        if expr.operator.type == tokenType.BANG_EQUAL:
            return not self.isEqual(left, right) 
        # equal equal ==
        if expr.operator.type == tokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)
        return None

    def visitExpressionStmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)

    def visitPrintStmt(self, stmt: Print) -> None:
        value: object = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visitVarStmt(self, stmt: Var):
        value: object = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visitVariableExpr(self, expr: Variable):
        return self.environment.get(expr.name)

    def visitAssignExpr(self, expr: Assign):
        value: object = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def executeBlock(self, statements: list[Stmt], environment: Environment):
        previous: Environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visitBlockStmt(self, stmt: Block):
        self.executeBlock(stmt.statements, Environment(self.environment))

    def visitIfStmt(self, stmt: If):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None
    
    def visitLogicalExpr(self, expr: Logical):
        left: object = self.evaluate(expr.left)
        if expr.operator.type == tokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        return self.evaluate(expr.right)

    def stringify(self, value: object) -> str:
        if value is None:
            return "nil"
        if type(value) == float:
            text: str = str(value)
            if len(text) >= 2 and text[-2:] == ".0":
                text = text[:-2]
            return text
        if type(value) == bool:
            return "true" if value else "false"
        return str(value)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except RunTimeException as e:
            self.lox.runtimeError(e)



        
