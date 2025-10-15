def func(x):
    x[0] += 5


obj = [10]
print(obj)
func(obj.copy())
print(obj)