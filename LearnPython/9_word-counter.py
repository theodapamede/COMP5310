words = {}
msg = input("Enter line: ")
while msg:
  word = msg.split()
  for i in range(0, len(word)):
    if word[i] in words:
      words[word[i]] = words[word[i]] + 1
    else:
      words[word[i]] = 1
  msg = input("Enter line: ")
for msg in sorted(words):
  print(msg, words[msg])
