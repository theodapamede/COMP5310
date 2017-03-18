cars = {}
colour = input("Car: ")
while colour:
  if colour in cars:
    cars[colour] = cars[colour] + 1
  else:
    cars[colour] = 1
  colour = input("Car: ")
for c in cars:
  print("Cars that are", c + ":", cars[c])
