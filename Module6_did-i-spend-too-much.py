x = input("Enter the expenses: ")
ex = x.split()
n = len(ex)
a = 0
for i in range(0, n):
  c = int(ex[i])
  a = a + c
print("Total: " + "$" + str(a))
