from Expr import Expr
from Token import Token

class Visitor:
	def visitExpressionStmt(self, Stmt):
		pass
	def visitPrintStmt(self, Stmt):
		pass
	def visitVarStmt(self, Stmt):
		pass
	def visitBlockStmt(self, statements):
		pass

class Stmt :
	def __init__(self):
		pass

	def accept(self, visitor: Visitor):
		pass

class Expression(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: Visitor):
		return visitor.visitExpressionStmt(self)

class Print(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: Visitor):
		return visitor.visitPrintStmt(self)

class Var(Stmt):
	def __init__(self, name: Token,initializer: Expr):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor: Visitor):
		return visitor.visitVarStmt(self)

class Block(Stmt):
	def __init__(self, statements):
		self.statements = statements

	def accept(self, visitor: Visitor):
		return visitor.visitBlockStmt(self)