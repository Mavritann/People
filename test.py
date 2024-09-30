import random

arr = []
c = []
max = 0

for j in range(20):
	for i in range(12783):
		arr.append(random.choices(["no", "yes"], weights = [12783, 2.4]))
	m = arr.count(["yes"])
	c.append(m)
	if m > max:
		max = m
	arr = []
#print(arr.count(["yes"]))
print(max)
print(c)
print(sum(c)/20)

class Test:
	def __init__(self, a):
		self.a = 0
		
	def show(self):
		print("Hello", self.a)
		
new = Test(6)
new.show()
