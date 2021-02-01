"""
Project Title: Calculator

Author: Braden Godley

Credit: 211 Starter Code
"""


ENV = dict()


def env_clear():
    """Clear all variables in calculator memory"""
    global ENV
    ENV = dict()



class Expr:
    """Abstract base class of all expressions"""

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError("Each concrete Expr subclass must define `eval`")

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation."""
        raise NotImplementedError("Each concrete Expr subclass must define __str__")

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like the constructor,
        e.g., Plus(IntConst(5), IntConst(4))"""

    def __eq__(self, other: "Expr") -> str:
        return self.eval() == other.eval()


class IntConst(Expr):
    """A subclass of Expr that contains an integer value"""

    def __init__(self, value: int):
        self.value = value

    def eval(self) -> "IntConst":
        """No calculations are required for a simple integer to be evaluated."""
        return self

    def __str__(self) -> str:
        """Simply returns the string form of its value."""
        return str(self.value)

    def __repr__(self) -> str:
        return f"IntConst({self.value})"

    def __eq__(self, other: "IntConst") -> bool:
        """"Returns true if both IntConsts have the same value"""
        return self.value == other.value

    def __add__(self, other: "IntConst") -> "IntConst":
        """Returns a new IntConst containing the total of both values."""
        total = self.value + other.value
        return IntConst(total)


class BinOp(Expr):
    """Takes two expressions in its constructor"""

    def __init__(self, exp1: Expr, exp2: Expr):
        raise NotImplementedError("Do not instantiate BinOP! (or else)")

    def _binop_init(self, exp1: Expr, exp2: Expr, op_sym: str, op_name: str):
        self.exp1 = exp1
        self.exp2 = exp2
        self.op_sym = op_sym
        self.op_name = op_name

    def __str__(self) -> str:
        """Returns an algebraic representation of the operation being done."""
        return f"({str(self.exp1)} {self.op_sym} {str(self.exp2)})"

    def __repr__(self) -> str:
        """Returns a constructor for the specific binary operator."""
        return f"{self.op_name}({repr(self.exp1)}, {repr(self.exp2)})"

    def _apply(self, val1: int, val2: int) -> int:
        raise NotImplementedError("Each concrete subclass of BinOp must implement `_apply`")

    def eval(self) -> IntConst:
        exp1_val = self.exp1.eval()
        exp2_val = self.exp2.eval()
        return IntConst(self._apply(exp1_val.value, exp2_val.value))


class Plus(BinOp):
    """Adds together two Expr instances"""

    def __init__(self, exp1: Expr, exp2: Expr):
        self._binop_init(exp1, exp2, "+", "Plus")

    def _apply(self, val1: int, val2: int) -> int:
        return val1 + val2


class Minus(BinOp):
    """Subtracts one Expr instance from another"""

    def __init__(self, exp1: Expr, exp2: Expr):
        self._binop_init(exp1, exp2, "-", "Minus")

    def _apply(self, val1: int, val2: int) -> int:
        return val1 - val2


class Times(BinOp):
    """Multiplies together two Expr instances"""

    def __init__(self, exp1: Expr, exp2: Expr):
        self._binop_init(exp1, exp2, "*", "Times")

    def _apply(self, val1: int, val2: int) -> int:
        return val1 * val2


class Div(BinOp):
    """Divides an Expr instance by another Expr instance."""

    def __init__(self, exp1: Expr, exp2: Expr):
        self._binop_init(exp1, exp2, "/", "Div")

    def _apply(self, val1: int, val2: int) -> int:
        return val1 // val2


class UnOp(Expr):
    """Takes only one expression in its constructor"""

    def __init__(self, exp: Expr):
        raise NotImplementedError("Do not instantiate UnOp! (don't do it please)")

    def _unop_init(self, exp: Expr, op_sym: str, op_name: str):
        self.exp = exp
        self.op_sym = op_sym
        self.op_name = op_name

    def _apply(self, val: int) -> int:
        raise NotImplementedError("Each concrete subclass of UnOp must implement `_apply`")

    def eval(self) -> IntConst:
        exp_val = self.exp.eval()
        return IntConst(self._apply(exp_val.value))

    def __str__(self) -> str:
        """Returns an algebraic representation of the operation
        being done on the given expression"""
        return f"{self.op_sym} {str(self.exp)}"

    def __repr__(self) -> str:
        """Returns a constructor for the specific unary operator"""
        return f"{self.op_name}({repr(self.exp)})"


class Neg(UnOp):
    """Gives the opposite of the given expression"""

    def __init__(self, exp: Expr):
        self._unop_init(exp, "~", "Neg")

    def _apply(self, val) -> int:
        return -val


class Abs(UnOp):
    """Gives the absolute value of the given expression"""

    def __init__(self, exp: Expr):
        self._unop_init(exp, "@", "Abs")

    def _apply(self, val) -> int:
        return abs(val)


class UndefinedVariable(Exception):
    """Raised when expression tries to use a variable that is not in the ENV"""
    pass


class Var(Expr):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var({self.name})"

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.Name} has not been assigned a value!")

    def assign(self, val: IntConst):
        ENV[self.name] = val


class Assign(Expr):
    """Assignment: x = E represented as Assign(x, E)"""

    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var)
        self.left = left
        self.right = right

    def eval(self) -> IntConst:
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val

    def __str__(self):
        return f"{self.left.name} = {str(self.right)}"

    def __repr__(self):
        return f"Assign({repr(self.left)}, {repr(self.right)})"
