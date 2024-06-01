from Expr import Expr


class Visitor:
	def visitExpressionStmt(self, stmt):
		pass
	def visitPrintStmt(self, stmt):
		pass

class Stmt:
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



