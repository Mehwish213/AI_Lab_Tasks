class SimpleCalculator:
    def __init__(self, expression):
        self.expr = expression.replace(" ", "")   

    def solve(self):
       
        while "(" in self.expr:
            close = self.expr.find(")")
            open = self.expr.rfind("(", 0, close)
            inside = self.expr[open+1:close]

           
            result = SimpleCalculator(inside).solve()
            self.expr = self.expr[:open] + str(result) + self.expr[close+1:]

        self.expr = self._solve_mul_div(self.expr)

     
        self.expr = self._solve_add_sub(self.expr)

        return int(self.expr)

    def _solve_mul_div(self, exp):
        i = 0
        while i < len(exp):
            if exp[i] in "*/":
                left, li = self._get_left_number(exp, i-1)
                right, ri = self._get_right_number(exp, i+1)

                if exp[i] == "*":
                    res = left * right
                else:
                    res = left // right  

                exp = exp[:li] + str(res) + exp[ri:]
                i = 0   
            else:
                i += 1
        return exp

    def _solve_add_sub(self, exp):
        i = 1   
        while i < len(exp):
            if exp[i] in "+-":
                left, li = self._get_left_number(exp, i-1)
                right, ri = self._get_right_number(exp, i+1)

                if exp[i] == "+":
                    res = left + right
                else:
                    res = left - right

                exp = exp[:li] + str(res) + exp[ri:]
                i = 0
            else:
                i += 1
        return exp

    def _get_left_number(self, exp, i):
        num = ""
        while i >= 0 and exp[i].isdigit():
            num = exp[i] + num
            i -= 1
        return int(num), i+1

    def _get_right_number(self, exp, i):
        num = ""
        while i < len(exp) and exp[i].isdigit():
            num += exp[i]
            i += 1
        return int(num), i




expr = "(8 - 2)*3 +6/2"
calc = SimpleCalculator(expr)
print(f"{expr} = {calc.solve()}")

