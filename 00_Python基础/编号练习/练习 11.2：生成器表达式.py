# TODO 1: 用生成器表达式计算 1 到 100 的平方和
# 提示: sum(x * x for x in range(1, 101))
a = sum(x**2 for x in range(1,101))
print(a)

# TODO 2: 对比列表推导式和生成器表达式的内存占用
# 用 sys.getsizeof() 观察
import sys

list_compr = [x for x in range(100000)]        # 列表推导式
gen_expr = (x for x in range(100000))  # 生成器表达式
# 生成器表达式是用括号包裹的是吗，这个知识点快忘记了，你帮我回忆一下

print(f"列表占用: {sys.getsizeof(list_compr)} 字节")   # 很大
print(f"生成器占用: {sys.getsizeof(gen_expr)} 字节")   # 很小（固定）
