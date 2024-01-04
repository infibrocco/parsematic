import math
import operator
import re
from abc import ABC
from argparse import ArgumentError
from typing import Callable, List, Tuple


def is_number(n: str) -> bool:
    """Checks if n is a number or not.

    Args:
        n (str)

    Returns:
        bool
    """
    if n.isnumeric():
        return True
    elif len(n) > 0:
        if re.match(r"^-?\d+(?:\.\d+)?$", n):
            return True

    return False


class MathObj(ABC):
    # Abstract base class for Mathematical Objects
    def __init__(self) -> None:
        ...

    def __repr__(self) -> str:
        return "MathObj()"

    def calc(self) -> int | float:
        return 0


class MathNum(MathObj):
    def __init__(self, n: str) -> None:
        """MathNum class for handling all kinds of numbers.

        Args:
            n (str): Any real number in string form.
        """
        if is_number(n):
            if "." in n:
                self.conv: Callable = float
            else:
                self.conv: Callable = int
            self.value: str = n
        else:
            raise ValueError(f"Invalid number {n}")

    def __repr__(self) -> str:
        return repr(self.calc())

    def calc(self) -> int | float:
        return self.conv(self.value)


class MathOp(MathObj):
    operators = {
        "**": operator.pow,
        "//": operator.floordiv,
        "/": operator.truediv,
        "*": operator.mul,
        "%": operator.mod,
        "+": operator.add,
        "-": operator.sub,
        "==": operator.eq,
        "!=": operator.ne,
        "<": operator.lt,
        ">": operator.gt,
        "<=": operator.le,
        ">=": operator.ge,
    }

    def __init__(self, op: str, value1: MathObj, value2: MathObj) -> None:
        """MathOp class for handling all mathematical operations.

        Args:
            op (str): The operator (eg. +, -, *).
            value1 (MathObj): The first value to operate on.
            value2 (MathObj): The second value to operate on.
        """
        self.op: Callable = self.operators.get(op, None)
        if self.op == None:
            raise ValueError(f"Unknown operator {op}")
        self.value1: MathObj = value1
        self.value2: MathObj = value2

    def __repr__(self) -> str:
        return f"{self.op.__name__}({self.value1}, {self.value2})"

    def calc(self) -> int | float:
        return self.op(self.value1.calc(), self.value2.calc())


class MathFunc(MathObj):
    funcs = {
        "fact": (math.factorial, 1, 1),
        "factorial": (math.factorial, 1, 1),
        "sin": (math.sin, 1, 1),
        "cos": (math.cos, 1, 1),
        "tan": (math.tan, 1, 1),
        "abs": (abs, 1, 1),
        "sqrt": (math.sqrt, 1, 1),
        "log": (math.log, 1, 2),
        "gcd": (math.gcd, 2, 1000),
        "lcm": (math.lcm, 2, 1000),
        "xor": (operator.xor, 2, 2),
        "int": (int, 1, 1),
        "float": (float, 1, 1),
        "min": (min, 2, 1000),
        "max": (max, 2, 1000),
        "not": (operator.not_, 1, 1),
    }

    def __init__(self, funcname: str, *args) -> None:
        """MathFunc class for handling all mathematical functions.

        Args:
            funcname (str): Function name.
        """
        self.func, self.min_args, self.max_args = self.funcs.get(
            funcname, (None, None, None)
        )
        if self.func == None:
            raise ValueError(f"Unknown function {funcname}")
        self.args: Tuple[MathObj] = (
            args
            if self.max_args >= len(args) >= self.min_args
            else ArgumentError(
                f"Invalid number of arguments to function {funcname}. Expected between {self.min_args}-{self.max_args}. Got {len(args)}."
            )
        )

    def __repr__(self) -> str:
        return f"{self.func.__name__}({', '.join(repr(x) for x in self.args)})"

    def calc(self) -> int | float:
        return self.func(*(x.calc() for x in self.args))


class MathParser:
    def __init__(self):
        """MathParser class for parsing math. (duh)"""
        self.pattern: re.Pattern = re.compile(
            r"\d+\.\d+|\d+|\/\/|\*\*|\+|\-|\*|\/|\w+|\(|\)"
        )

    def tokenize(self, expression: str) -> MathObj:
        """Tokenize the expression into a MathObj (MathNum, MathOp, MathFunc) representing numbers, operators and functions.

        Args:
            expression (str): The expression to tokenize.

        Returns:
            MathObj: A mathematical object representing the expression.
        """

        tokens: List[str] = re.findall(self.pattern, expression)
        # print(f"{tokens=}")

        # Add support for negative numbers
        updated_tokens: List[MathObj] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == "-" and (
                i == 0
                or (tokens[i - 1] in MathOp.operators.keys() and tokens[i - 1] != ")")
            ):
                # Combine "-" with the following number to form a negative number token
                combined_token = token + tokens[i + 1]
                updated_tokens.append(combined_token)
                i += 1  # Skip the next token since it has been combined
            else:
                updated_tokens.append(token)
            i += 1

        for i, v in enumerate(updated_tokens):
            if is_number(v):
                updated_tokens[i] = MathNum(v)

        while updated_tokens.count("(") > 0:
            funcargs = False
            p1, p2 = self.find_parentheses(updated_tokens)
            if updated_tokens[p1 - 1] in MathFunc.funcs.keys():
                funcargs = True
            expr = updated_tokens[p1 + 1 : p2]

            for op in MathOp.operators.keys():
                try:
                    found = expr.index(op)
                    while found != -1:
                        expr[found] = MathOp(op, expr[found - 1], expr[found + 1])
                        del expr[found + 1]
                        del expr[found - 1]
                        found = expr.index(op)
                except ValueError:
                    continue
            if len(expr) != 1:
                raise Exception(f"idk. heres the {expr=}")
            if funcargs:
                updated_tokens[p1 - 1] = MathFunc(updated_tokens[p1 - 1], *expr)
                updated_tokens = updated_tokens[:p1] + updated_tokens[p2 + 1 :]

            else:
                updated_tokens = updated_tokens[:p1] + expr + updated_tokens[p2 + 1 :]

        tokens: List[MathObj] = updated_tokens
        iters = 0
        while len(tokens) > 1 and iters < 100:
            for op in MathOp.operators.keys():
                try:
                    found = tokens.index(op)
                    while found != -1:
                        tokens[found] = MathOp(op, tokens[found - 1], tokens[found + 1])
                        del tokens[found + 1]
                        del tokens[found - 1]
                        found = tokens.index(op)
                except ValueError:
                    continue
                except IndexError:
                    raise SyntaxError(f"Invalid syntax. {tokens=}")
            iters += 1

        if len(tokens) == 0:
            return MathObj()
        # print(tokens)
        return tokens[0]

    def find_parentheses(self, expr: str | list) -> Tuple[int, int]:
        """Finds the index of the innermost parentheses in a given expression

        Args:
            expr (str | list): The expression to find parentheses in

        Raises:
            SyntaxError: If mismatched parentheses
            TypeError: If incorrect type of expression

        Returns:
            Tuple[int, int]: The index of the first ')' and the last '(' before the first ')'.
        """
        c1: int = expr.count("(")
        if c1 != expr.count(")"):
            raise SyntaxError(f"Mismatched parentheses. {expr=}")
        elif c1 == 0:
            return (None, None)

        p1 = p2 = -1
        if isinstance(expr, list):
            p2 = expr.index(")")
            p1 = max(idx for idx, val in enumerate(expr[:p2]) if val == "(")

        elif isinstance(expr, str):
            p2 = expr.find(")")
            p1 = expr[:p2].rfind("(")

        else:
            raise TypeError(
                f"The argument expr should be a str or list type. Got {type(expr)}. {expr=}"
            )

        return (p1, p2)

    def calculate(self, tokens: MathObj) -> int | float:
        """Calculates the given tokens (MathObj) and returns the value.

        Args:
            tokens (MathObj): The given token

        Returns:
            int|float: The result
        """
        return tokens.calc()

    def parse(self, expression: str) -> int | float:
        """Parses the given expression and returns the calculated result.

        Args:
            expression (str): The expression to be parsed.

        Returns:
            int|float: The calculated result
        """
        tokens: MathObj = self.tokenize(expression)
        return self.calculate(tokens)
