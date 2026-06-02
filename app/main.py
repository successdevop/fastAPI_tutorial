# text: str = "value"
# num: int = 90
# flnum: float = 37.5
#
# digits: list[int] = [1,2,3,4,5]
#
# table_5: tuple[int, ...] = (1,2,3,4,5)
#
#
# def root(numm: int):
#     return pow(numm, .5)
#
#
# root25 = root(25)
# print(root25)
from typing import Optional


# def fence(val: str = "+"):
#     def inner_fence(func):
#         def wrapper_func():
#             print(val*10)
#             func()
#             print(val*10)
#         return wrapper_func
#     return inner_fence
#
#
# @fence
# def log():
#     print("decorated!")
#
# log()