from enum import Enum
import math


class TransitionType(Enum):
    IMMEDIATE = "IMM",
    EXPONENTIAL = "EXP"


class ArcTypes(Enum):
    INPUT = "INPUT",
    OUTPUT = "OUTPUT",
    INHIBITOR = "INHIBITOR"


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def scale(self, factor):
        return Position(self.x * factor, self.y * factor)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Place:
    def __init__(self, name, tokens=0, position=None, label_shift=None):
        self.name = name
        self.tokens = tokens
        self.position = position
        self.label_shift = label_shift


class Transition:
    def __init__(self, name, type, position=None, rotation=None, label_shift=None):
        self.name = name
        assert isinstance(type, TransitionType)
        self.type = type
        self.position = position
        self.rotation = 0 if rotation is None else 360 - math.degrees(rotation)
        self.label_shift = label_shift


class ImmediateTransition(Transition):
    def __init__(self, name, position=None, rotation=None, label_shift=None):
        Transition.__init__(self, name, TransitionType.IMMEDIATE, position, rotation, label_shift)


class TimedTransition(Transition):
    def __init__(self, name, delay, nservers=1, position=None, rotation=None, label_shift=None):
        Transition.__init__(self, name, TransitionType.EXPONENTIAL, position, rotation, label_shift)
        self.delay = delay
        self.nservers = nservers


class Arc:
    def __init__(self, source, target, arc_type):
        self.source = source
        self.target = target
        assert isinstance(arc_type, ArcTypes)
        self.arc_type = arc_type


class Gspn:
    def __init__(self, name):
        self.name = name
        self.places = []
        self.transitions = []
        self.arcs = []

    def __str__(self):
        return "GSPN '{}' with {} places, {} transitions and {} arcs".format(self.name, len(self.places), len(self.transitions), len(self.arcs))
