from typing import NewType, List
import datetime as dt

IntBool = NewType("IntBool", bool)
StrBool = NewType("StrBool", bool)
SlashDate = NewType("SlashDate", dt.date)
CommaIntList = NewType("CommaIntList", List[int])
CommaStrList = NewType("CommaStrList", List[str])
