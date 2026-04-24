class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero, answer is undefined.")
        return a / b
    
    def square(self, a):
        return a ** 2

    def power(self, a, b):
        return a ** b
    
    def square_root(self, a):
        if a < 0:
            raise ValueError("Cannot take the square root of a negative number.")
        return a ** 0.5
    
    def root(self, a, b):
        if a < 0 and b % 2 == 0:
            raise ValueError("Cannot take an even root of a negative number.")
        if a < 0 and b % 2 != 0:
            return -((-a) ** (1 / b))
        return a ** (1 / b)
    
    def logarithm(self, a, base):
        if a <= 0:
            raise ValueError("Logarithm is undefined for non-positive numbers.")
        if base <= 1:
            raise ValueError("Logarithm base must be greater than 1.")
        import math
        return math.log(a, base)

    def evaluate(self, expression):
        tokens = self._tokenize(expression.replace(' ', ''))
        result, pos = self._parse_expr(tokens, 0)
        if pos != len(tokens):
            raise ValueError("Invalid expression")
        return result

    def _tokenize(self, expression):
        import math
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i:i+2] == 'pi':
                tokens.append(('NUM', math.pi))
                i += 2
            elif expression[i] == 'e' and (i + 1 >= len(expression) or not expression[i + 1].isalpha()):
                tokens.append(('NUM', math.e))
                i += 1
            elif expression[i].isalpha():
                j = i
                while j < len(expression) and expression[j].isalpha():
                    j += 1
                name = expression[i:j]
                tokens.append(('NAME', name))
                i = j
            elif expression[i].isdigit() or expression[i] == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(('NUM', float(expression[i:j])))
                i = j
            elif expression[i] in '+-*/^(),':
                tokens.append(('OP', expression[i]))
                i += 1
            else:
                raise ValueError(f"Unknown character: {expression[i]}")
        return tokens

    def _parse_expr(self, tokens, pos):
        left, pos = self._parse_term(tokens, pos)
        while pos < len(tokens) and tokens[pos][0] == 'OP' and tokens[pos][1] in ('+', '-'):
            op = tokens[pos][1]
            pos += 1
            right, pos = self._parse_term(tokens, pos)
            left = self.add(left, right) if op == '+' else self.subtract(left, right)
        return left, pos

    def _parse_term(self, tokens, pos):
        left, pos = self._parse_power(tokens, pos)
        while pos < len(tokens) and tokens[pos][0] == 'OP' and tokens[pos][1] in ('*', '/'):
            op = tokens[pos][1]
            pos += 1
            right, pos = self._parse_power(tokens, pos)
            left = self.multiply(left, right) if op == '*' else self.divide(left, right)
        return left, pos

    def _parse_power(self, tokens, pos):
        base, pos = self._parse_unary(tokens, pos)
        if pos < len(tokens) and tokens[pos] == ('OP', '^'):
            pos += 1
            exp, pos = self._parse_power(tokens, pos)
            return self.power(base, exp), pos
        return base, pos

    def _parse_unary(self, tokens, pos):
        if pos < len(tokens) and tokens[pos] == ('OP', '-'):
            pos += 1
            val, pos = self._parse_atom(tokens, pos)
            return -val, pos
        return self._parse_atom(tokens, pos)

    def _parse_atom(self, tokens, pos):
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")
        tok_type, tok_val = tokens[pos]
        if tok_type == 'NUM':
            return tok_val, pos + 1
        if tok_type == 'NAME':
            if pos + 1 < len(tokens) and tokens[pos + 1] == ('OP', '('):
                pos += 2
                args = []
                if pos < len(tokens) and tokens[pos] != ('OP', ')'):
                    while True:
                        arg, pos = self._parse_expr(tokens, pos)
                        args.append(arg)
                        if pos < len(tokens) and tokens[pos] == ('OP', ','):
                            pos += 1
                            continue
                        break
                if pos >= len(tokens) or tokens[pos] != ('OP', ')'):
                    raise ValueError("Missing closing parenthesis")
                return self._eval_function(tok_val, args), pos + 1
            return self._eval_name(tok_val), pos + 1
        if tok_val == '(':
            pos += 1
            val, pos = self._parse_expr(tokens, pos)
            if pos >= len(tokens) or tokens[pos] != ('OP', ')'):
                raise ValueError("Missing closing parenthesis")
            return val, pos + 1
        raise ValueError(f"Unexpected token: {tok_val}")

    def _eval_name(self, name):
        if name == 'pi':
            return math.pi
        if name == 'e':
            return math.e
        raise ValueError(f"Unsupported name '{name}' in expression.")

    def _eval_function(self, func_name, args):
        if func_name == 'sqrt':
            if len(args) != 1:
                raise ValueError("sqrt() takes one argument.")
            return self.square_root(args[0])

        if func_name == 'log':
            if len(args) == 1:
                if args[0] <= 0:
                    raise ValueError("Logarithm is undefined for non-positive numbers.")
                return math.log(args[0])
            if len(args) == 2:
                return self.logarithm(args[0], args[1])
            raise ValueError("log() takes one or two arguments.")

        if func_name == 'root':
            if len(args) != 2:
                raise ValueError("root() takes two arguments.")
            return self.root(args[0], args[1])

        if func_name in ('sin', 'cos', 'tan'):
            if len(args) != 1:
                raise ValueError(f"{func_name}() takes one argument.")
            return getattr(math, func_name)(args[0])

        raise ValueError(f"Unsupported function '{func_name}' in expression.")

    def sin(self, a):
        import math
        return math.sin(a)
    
    def cos(self, a):
        import math
        return math.cos(a)
    
    def tan(self, a):
        import math
        return math.tan(a)

def main():
    calculator = Calculator()
    print("Welcome to the Calculator! Operations are currently running in radians.")
    print("Supported operations: +, -, *, /, ^ (power), parentheses, sqrt(), log(), sin(), cos(), tan()")
    print("Example: 2 * 4 + (3 - 1)")
    print()    
    while True:
        equation = input("Enter a math equation to solve (or 'quit' to exit): ").strip()
        
        if equation.lower() == 'quit':
            print("Thank you for using the Calculator!")
            break
        
        try:
            result = calculator.evaluate(equation)
            print(f"Result: {result}\n")
        
        except ValueError as error:
            print(f"Error: {error}\n")
        except Exception as error:
            print(f"Invalid input: {error}\n")


if __name__ == "__main__":
    main()
    #comment added