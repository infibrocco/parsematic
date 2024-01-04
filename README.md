<img src="https://img.shields.io/github/actions/workflow/status/infibrocco/parsematic/python-package.yml?style=for-the-badge" height="25"> <img src="https://img.shields.io/badge/license-MIT-0?style=for-the-badge" height="25"> <img src="https://img.shields.io/github/repo-size/infibrocco/parsematic?style=for-the-badge" height="25"> <img src="https://sloc.xyz/github/infibrocco/parsematic/?style=for-the-badge" height="25"> <img src="https://img.shields.io/github/stars/infibrocco/parsematic?style=for-the-badge" height="25"> <img src="https://img.shields.io/badge/python_version-3.7%2C%203.8%2C%203.9%2C%203.10%203.11%2C%203.12-37?style=for-the-badge" height="25">
<img src="https://forthebadge.com/images/featured/featured-built-with-love.svg" height="25">
<img src="https://forthebadge.com/images/featured/featured-powered-by-electricity.svg" height="25">
<img src="https://img.shields.io/badge/code_style-black-000000.svg?style=for-the-badge" height="25">
<img src="https://img.shields.io/badge/imports-isort-1674b1?style=for-the-badge&labelColor=ef8336" height="25">
<img src="https://img.shields.io/badge/mypy-checked-2a6db2?style=for-the-badge" height="25">

# Parsematic

This is a basic math parser that can parse mathematical expressions.

## Features

Parses a variety of mathematical expressions, including:

- Integers `(0, 1, 5, -7)`, Floats `(3.14159, 2.7, 0.5)`

- Basic arithmetic operations `(+, -, \*, /, \*\*, //, %)`

- Constants `PI, TAU, NAN, E, INF`

- Comparison operators `(==, !=, <, >, <=, >=)`

- Parentheses for grouping

- Mathematical functions `(sin, cos, tan, abs, sqrt, log, fact, gcd, lcm, xor, int, float, min, max)`

## Usage

First, install it with:

```
pip install parsematic
```

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
python -m parsematic "2 + 3 * (4 - 1)"
```

Supported Operators:

- Arithmetic operators: `+, -, \_, / (true division), // (floor division), \*\* (exponentiation), % (modulo)`
- Comparison operators: `==, !=, <, >, <=, >=`
- Supported Functions
  `sin, cos, tan, abs, sqrt, log,
fact (factorial),
gcd (greatest common divisor),
lcm (least common multiple),
xor (bitwise exclusive or),
int, float (type conversions),
min, max`

## Error Handling

The parser will raise exceptions for invalid syntax or unsupported operations.

## Additional Notes

The parser currently does support constants or user-defined functions (although you have to modify MathFunc.funcs). (but not variables within the parser itself)

## Contributing

Pull requests are welcome!
