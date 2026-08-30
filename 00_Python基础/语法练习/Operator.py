import operator

a = [1, 2]
b = [1, 3]
c = [2, 3]
print(operator.eq(a, b))
print(operator.eq(c, b))
# operator.lt(a, b) 与 a < b 相同，
# operator.le(a, b) 与 a <= b 相同，
# operator.eq(a, b) 与 a == b 相同，
# operator.ne(a, b) 与 a != b 相同，
# operator.gt(a, b) 与 a > b 相同，
# operator.ge(a, b) 与 a >= b 相同。
