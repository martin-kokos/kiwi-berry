from typing import NewType
import datetime as dt

IntBool = NewType('IntBool', bool)
StrBool = NewType('StrBool', bool)
SlashDate = NewType('SlashDate', dt.date)
CommaIntList = NewType('CommaIntList', list[int])
CommaStrList = NewType('CommaStr', list[str])
