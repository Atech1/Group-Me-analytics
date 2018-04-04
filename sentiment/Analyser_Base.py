# Alexander Ross (asr3bj), Analyser_Base.py
# this was created Apr, 2018

import abc


class AnalyserBase(metaclass=abc.ABCMeta):
    """this is basically to setup an interface so that everything will always work """
    @abc.abstractmethod
    def check(self, msg) -> bool:
        pass

