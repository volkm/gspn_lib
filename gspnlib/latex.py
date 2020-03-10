import math
from enum import Enum

from gspnlib.gspn import Place, ImmediateTransition, TimedTransition, Arc, ArcTypes, Gspn

SCALE_FACTOR = 0.5


class Direction(Enum):
    HORIZONTAL = 0,
    VERTICAL = 1,
    ROTATED = 2


def generate_label(name, shift):
    # Rudimentary support for label positioning
    s = "label = {"
    if shift is not None and shift.x != 0 and shift.y != 0:
        scaled = shift.scale(SCALE_FACTOR)
        s += "[xshift={}, yshift={}]".format(scaled.x, -scaled.y)

    if '_' in name:
        parts = name.split('_')
        assert len(parts) == 2
        name = parts[0] + "_{" + parts[1] + "}"
    s += "${}$}}".format(name)
    return s


def generate_tikz_place(place):
    s = "\t\\node[place"
    if place.tokens > 0:
        s += ", tokens={}".format(place.tokens)
    s += ", " + generate_label(place.name, place.label_shift)
    scaled = place.position.scale(SCALE_FACTOR)
    s += "] at ({}, {})".format(scaled.x, -scaled.y)
    s += "({}) {{}};\n".format(place.name)
    return s


def generate_tikz_transition(transition):
    s = "\t\\node["

    # Check rotation
    direction = Direction.ROTATED
    if transition.rotation is not None:
        if math.isclose(transition.rotation, 0, abs_tol=5) or math.isclose(transition.rotation, 180, abs_tol=5) or math.isclose(transition.rotation, 360, abs_tol=5):
            direction = Direction.HORIZONTAL
        elif math.isclose(transition.rotation, 90, abs_tol=5) or math.isclose(transition.rotation, 270, abs_tol=5):
            direction = Direction.VERTICAL

    if isinstance(transition, TimedTransition):
        if direction == Direction.HORIZONTAL:
            s += "ttransition"
        elif direction == Direction.VERTICAL:
            s += "Ttransition"
        else:
            assert direction == Direction.ROTATED
            s += "ttransition"

    else:
        assert isinstance(transition, ImmediateTransition)
        if direction == Direction.HORIZONTAL:
            s += "itransition"
        elif direction == Direction.VERTICAL:
            s += "Itransition"
        else:
            assert direction == Direction.ROTATED
            s += "itransition"

    s += ", " + generate_label(transition.name, transition.label_shift)

    if direction == Direction.ROTATED:
        s += ", rotate={}".format(transition.rotation)
    scaled = transition.position.scale(SCALE_FACTOR)
    s += "] at ({}, {})".format(scaled.x, -scaled.y)
    s += "({}) {{}};\n".format(transition.name)
    return s


def generate_tikz_arc(arc):
    if arc.arc_type == ArcTypes.INPUT:
        return "\t\\draw[<-] ({0}) -- ({1});\n".format(arc.source, arc.target)
    elif arc.arc_type == ArcTypes.OUTPUT:
        return "\t\\draw[->] ({0}) -- ({1});\n".format(arc.source, arc.target)
    else:
        assert arc.arc_type == ArcTypes.INHIBITOR
        return "\t\\draw[o-] ({0}) -- ({1});\n".format(arc.source, arc.target)


def generate_tikz(gspn, file):
    """
    Generate tikz file from GSPN.
    :param gspn: GSPN.
    :param file: Output tikz file.
    """
    with open(file, 'w') as f:
        f.write("\\begin{tikzpicture}[auto]\n")

        # Draw places
        for place in gspn.places:
            f.write(generate_tikz_place(place))

        f.write("\n")

        # Draw transitions
        for transition in gspn.transitions:
            f.write(generate_tikz_transition(transition))

        f.write("\n")

        # Draw arcs
        for arc in gspn.arcs:
            f.write(generate_tikz_arc(arc))

        f.write("\\end{tikzpicture}\n")
