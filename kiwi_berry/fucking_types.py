from typing import TypeAlias
import datetime as dt

IntBool: TypeAlias = bool
StrBool: TypeAlias = bool


class SlashDate(dt.date):

    @classmethod
    def from_url_fmt(cls, s: str):
        return cls(*dt.datetime.strptime(s, '%d/%m/%Y').date().timetuple()[:3])

    @staticmethod
    def to_url_fmt(d):
        return d.strftime('%d/%m/%Y')


class CommaIntList(list[int]):

    @classmethod
    def from_url_fmt(cls, s: str):
        return cls([int(e) for e in s.split(',')])

    @staticmethod
    def to_url_fmt(li):
        return ','.join(li)


class CommaStrList(list[str]):

    @staticmethod
    def from_url_fmt(s):
        return s.split(',')

    @staticmethod
    def to_url_fmt(li):
        return ','.join(li)
