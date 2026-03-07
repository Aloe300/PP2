import re

text = "My email is test123@gmail.com"
match = re.search(r"\S+@\S+\.\S+", text)

if match:
    print(match.group())
#\S+   # до @
#@
#\S+   # между @ и .
#\.
#\S+   # после точки


import re

text = "I have 2 apples, 5 bananas, and 10 oranges"

numbers = re.findall(r"\d+", text)
print(numbers)





import re
s = input()
print("Yes" if re.fullmatch(r"ab*", s) else "No")

import re
s = input()
print("Yes" if re.fullmatch(r"ab{2,3}", s) else "No")

import re
s = input()
print(re.findall(r"\b[a-z]+_[a-z]+\b", s))

import re
s = input()
print(re.findall(r"\b[A-Z][a-z]+\b", s))

import re
s = input()
print("Yes" if re.fullmatch(r"a.*b", s) else "No")

import re
s = input()
print(re.sub(r"[ ,.]", ":", s))



s = input()
parts = s.split("_")
print(parts[0] + "".join(word.capitalize() for word in parts[1:]))



import re
s = input()
print(re.split(r"(?=[A-Z])", s))

import re
s = input()
print(re.sub(r"(?<!^)(?=[A-Z])", " ", s))

import re
s = input()
print(re.sub(r"([A-Z])", r"_\1", s).lower())