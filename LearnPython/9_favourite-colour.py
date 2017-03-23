nc = {}

data = input("Name and colour: ")
while data:
  name, colour = data.split()
  nc[name] = colour
  data = input("Name and colour: ")
for n in nc:
  print(n, nc[n])
  
