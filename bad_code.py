# 1) out of memory
# 2) file descriptor leak
# 3) split() caveats
my_str = open('blablabla.txt').read()
x = my_str.split()
print(x[0])


