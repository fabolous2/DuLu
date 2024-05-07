from enum import Enum

class Test(Enum):
    TEST = 'тест'
    ACTIVE = 'активный'


print(Test.TEST.value)