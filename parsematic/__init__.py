"""# Parsematic

This is a basic math parser that can parse mathematical expressions.

## Usage

Import the MathParser class:

```Python
from math_parser import MathParser
```

Create a MathParser instance:

```Python
parser = MathParser()
```

Use the parse() method to parse and evaluate an expression:

```Python
result = parser.parse("2 + 3 * (4 - 1)")
print(result) # Output: 11
```

Or, use it from the command line

```Python
python -m yampy "2 + 3 * (4 - 1)"
```
"""

import math
import operator
import re
from abc import ABC
from argparse import ArgumentError
from typing import Callable, List, Tuple, Union


def is_number(n: str) -> bool:
    """Checks if n is a number or not.

    Args:
        n (str)

    Returns:
        bool
    """
    if n.isnumeric():
        return True
    if len(n) > 0 and re.match(r"^-?\d+(?:\.\d+)?$", n):
        return True

    return False


class MathObj(ABC):
    """Abstract base class for Mathematical Objects"""

    def __init__(self) -> None:
        ...

    def __repr__(self) -> str:
        """
        Returns a string representation of the MathObj instance.

        :return: A string representation of the MathObj instance.
        :rtype: str
        """
        return "MathObj()"

    def calc(self) -> Union[int, float]:
        """
        Calculates and returns the result.

        :param self: The instance of the class.
        :return: The calculated result, which can be an integer or a float.
        """
        return 0


class MathNum(MathObj):
    """MathNum class for handling all kinds of numbers."""

    def __init__(self, n: Union[str, int, float]) -> None:
        """MathNum class for handling all kinds of numbers.

        Args:
            n (str): Any real number in string form.
        """
        super().__init__()  # just to shut up pylint
        if isinstance(n, int):
            self.conv: Callable = int
            self.value: int = n
        elif isinstance(n, float):
            self.conv: Callable = float
            self.value: float = n
        elif is_number(n):
            if "." in n:
                self.conv: Callable = float
            else:
                self.conv: Callable = int
            self.value: str = n
        else:
            raise ValueError(f"Invalid number {n}")

    def __repr__(self) -> str:
        return repr(self.calc())

    def calc(self) -> Union[int, float]:
        return self.conv(self.value)


class MathConst(MathObj):
    """MathConst class for handling all kinds of constants."""

    constants = {
        "PI": MathNum(math.pi),
        "TAU": MathNum(math.tau),
        "E": MathNum(math.e),
        "INF": MathNum(math.inf),
        "NAN": MathNum(math.nan),
    }

    def __repr__(self) -> str:
        return "MathConst()"


class MathOp(MathObj):
    """MathOp class for handling all mathematical operations."""

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
        super().__init__()
        self.op: Callable = self.operators.get(op, None)
        if self.op is None:
            raise ValueError(f"Unknown operator {op}")
        self.value1: MathObj = value1
        self.value2: MathObj = value2
        if (op in ("/", "//")) and value2 == 0:
            self.op: Callable = self.ret_nan

    def __repr__(self) -> str:
        return f"{self.op.__name__}({self.value1}, {self.value2})"

    def calc(self) -> Union[int, float]:
        return self.op(self.value1.calc(), self.value2.calc())

    def ret_nan(self, *args) -> math.nan:
        """
        A function that returns `nan`.

        Parameters:
            *args: Variable number of arguments.

        Returns:
            `nan`: A constant value representing not a number (NaN).
        """
        del args
        return math.nan


class MathFunc(MathObj):
    """MathFunc class for handling all mathematical functions."""

    funcs = {
        "fact": (math.factorial, 1, 1),
        "factorial": (math.factorial, 1, 1),
        "sin": (math.sin, 1, 1),
        "cos": (math.cos, 1, 1),
        "tan": (math.tan, 1, 1),
        "abs": (abs, 1, 1),
        "sqrt": (math.sqrt, 1, 1),
        "log": (math.log, 1, 2),
        "log2": (math.log2, 1, 1),
        "log10": (math.log10, 1, 1),
        "gcd": (math.gcd, 2, 1000),
        "lcm": (lambda a, b: (a * b) // math.gcd(a, b), 2, 1000),
        "xor": (operator.xor, 2, 2),
        "int": (int, 1, 1),
        "float": (float, 1, 1),
        "min": (min, 2, 1000),
        "max": (max, 2, 1000),
        "not": (operator.not_, 1, 1),
        "round": (round, 1, 2),
        "ceil": (math.ceil, 1, 1),
        "floor": (math.floor, 1, 1),
        "chr": (chr, 1, 1),
        "bin": (bin, 1, 1),
        "hex": (hex, 1, 1),
        "oct": (oct, 1, 1),
        "hash": (hash, 1, 1),
        "hypot": (math.hypot, 1, 1000),
    }

    def __init__(self, funcname: str, *args) -> None:
        """MathFunc class for handling all mathematical functions.

        Args:
            funcname (str): Function name.
        """
        super().__init__()
        self.func, self.min_args, self.max_args = self.funcs.get(
            funcname, (None, None, None)
        )
        if self.func is None:
            raise ValueError(f"Unknown function {funcname}")
        self.args: Tuple[MathObj] = (
            args
            if self.max_args >= len(args) >= self.min_args
            else ArgumentError(
                "",
                message=f"Invalid number of arguments to function {funcname}. Expected \
                \bbetween {self.min_args}-{self.max_args}. Got {len(args)}.",
            )
        )

    def __repr__(self) -> str:
        return f"{self.func.__name__}({', '.join(repr(x) for x in self.args)})"

    def calc(self) -> Union[int, float]:
        return self.func(*(x.calc() for x in self.args))


class MathParser:
    """MathParser class for parsing math. (duh)"""

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

        def should_combine_tokens(
            token: str, tokens: List[str], i: int
        ) -> bool:
            return token == "-" and (
                i == 0 or (tokens[i - 1] in MathOp.operators)
            )

        updated_tokens: List[MathObj] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if should_combine_tokens(token, tokens, i):
                updated_tokens.append(token + tokens[i + 1])
                i += 1
            elif token in MathConst.constants:
                updated_tokens.append(MathConst.constants[token])
            else:
                updated_tokens.append(token)
            i += 1

        updated_tokens = [
            MathNum(token) if is_number(token) else token
            for token in updated_tokens
        ]

        while "(" in updated_tokens:
            funcargs = False
            p1, p2 = self.find_parentheses(updated_tokens)
            if updated_tokens[p1 - 1] in MathFunc.funcs:
                funcargs = True
            expr = updated_tokens[p1 + 1 : p2]

            for op in MathOp.operators:
                try:
                    found = expr.index(op)
                    while found != -1:
                        expr[found] = MathOp(
                            op, expr[found - 1], expr[found + 1]
                        )
                        del expr[found + 1]
                        del expr[found - 1]
                        found = expr.index(op)
                except ValueError:
                    continue

            if len(expr) > 1:
                pass

            if funcargs:
                updated_tokens[p1 - 1] = MathFunc(updated_tokens[p1 - 1], *expr)
                updated_tokens = updated_tokens[:p1] + updated_tokens[p2 + 1 :]

            else:
                updated_tokens = (
                    updated_tokens[:p1] + expr + updated_tokens[p2 + 1 :]
                )

        tokens: List[MathObj] = updated_tokens
        iters = 0
        while len(tokens) > 1 and iters < 100:
            for op in MathOp.operators:
                try:
                    found = tokens.index(op)
                    while found != -1:
                        tokens[found] = MathOp(
                            op, tokens[found - 1], tokens[found + 1]
                        )
                        del tokens[found + 1]
                        del tokens[found - 1]
                        found = tokens.index(op)
                except ValueError:
                    continue
                except IndexError as err:
                    raise SyntaxError(
                        f"Invalid syntax. tokens={tokens}"
                    ) from err
            iters += 1

        if len(tokens) == 0:
            return MathObj()
        return tokens[0]

    def find_parentheses(self, expr: Union[str, list]) -> Tuple[int, int]:
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
            raise SyntaxError(f"Mismatched parentheses. expr={expr}")
        if c1 == 0:
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
                f"The argument expr should be a str or list type. Got {type(expr)}. expr={expr}"
            )

        return (p1, p2)

    def calculate(self, tokens: MathObj) -> Union[int, float]:
        """Calculates the given tokens (MathObj) and returns the value.

        Args:
            tokens (MathObj): The given token

        Returns:
            int|float: The result
        """
        return tokens.calc()

    def parse(self, expression: str) -> Union[int, float]:
        """Parses the given expression and returns the calculated result.

        Args:
            expression (str): The expression to be parsed.

        Returns:
            int|float: The calculated result
        """
        tokens: MathObj = self.tokenize(expression)
        return self.calculate(tokens)
