from typing import *
import json


class A(TypedDict):
    b: Required[int]


a = A()
print(a)
