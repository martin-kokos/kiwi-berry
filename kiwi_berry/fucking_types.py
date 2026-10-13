import datetime as dt
from typing import NewType

IntBool = NewType("IntBool", bool)
StrBool = NewType("StrBool", bool)
SlashDate = NewType("SlashDate", dt.date)
CommaIntList = NewType("CommaIntList", list[int])
CommaStrList = NewType("CommaStrList", list[str])
