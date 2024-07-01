import logging
help(logging.Formatter)
print(dir(logging.Formatter))

# logging.Formatter의 모든 속성과 메서드를 가져옵니다.
items = dir(logging.Formatter)

# 속성과 메서드를 구분하여 저장할 리스트를 초기화합니다.
attributes = []
methods = []

# 각 항목에 대해 호출 가능한지 여부를 확인하여 속성과 메서드를 구분합니다.
for item in items:
    if callable(getattr(logging.Formatter, item)):
        methods.append(item)
    else:
        attributes.append(item)

# 결과 출력
print("Attributes:")
for attr in attributes:
    # print(attr)
    if not attr.startswith("__"):
        print(attr)

print("\nMethods:")
for method in methods:
    # print(method)
    if not method.startswith("__"):
        print(method)