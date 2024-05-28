from Token import Token

class Visitor:
	def visitBinaryExpr(self, expr):
		pass
	def visitGroupingExpr(self, expr):
		pass
	def visitLiteralExpr(self, expr):
		pass
	def visitUnaryExpr(self, expr):
		pass

class Expr :
	def __init__(self):
		pass

	def accept(self, visitor: Visitor):
		pass

class Binary(Expr):
	def __init__(self, left: Expr,operator: Token,right: Expr):
		self.left = left
		self.operator = operator
		self.right = right
	left: Expr
	operator: Token
	right: Expr

	def accept(self, visitor: Visitor):
		return visitor.visitBinaryExpr(self)

class Grouping(Expr):
	def __init__(self, expression: Expr):
		self.expression = expression
	expression: Expr

	def accept(self, visitor: Visitor):
		return visitor.visitGroupingExpr(self)

class Literal(Expr):
	def __init__(self, value: object):
		self.value = value
	value: object

	def accept(self, visitor: Visitor):
		return visitor.visitLiteralExpr(self)

class Unary(Expr):
	def __init__(self, operator: Token,right: Expr):
		self.operator = operator
		self.right = right
	operator: Token
	right: Expr

	def accept(self, visitor: Visitor):
		return visitor.visitUnaryExpr(self)
