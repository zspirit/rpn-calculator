import re
import sys

def calculate(operator, op_x, op_y):
    """ compute basic arithmetic operations """
    cases = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }
    return cases[operator](op_x, op_y)

def postfix(expression):
    """ compute postfix expression """
    res         = 0
    stack       = []
    elements    = re.split(r"\s+", expression)

    for elem in elements:
        if re.match("^[-+\\/*()]$", elem):
            op1 = stack.pop()
            op2 = stack.pop()
            res = calculate(elem, int(op2), int(op1))
            stack.append(res)
        else:
            stack.append(elem)
    return res

def main():
    """main function"""
    expression = sys.argv[1]
    print(postfix(expression))

if __name__ == '__main__':
    main()