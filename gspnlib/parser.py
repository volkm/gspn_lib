import xml.etree.ElementTree as ET

from gspnlib.gspn import Position, Place, ImmediateTransition, TimedTransition, Arc, ArcTypes, Gspn


def is_pnpro_file(file):
    """
    Checks whether the given file is a GSPN in the PNPRO format of GreatSPN.
    :param file: File.
    :return: True iff the file is a PNPRO file.
    """
    return file.endswith(".pnpro") or file.endswith(".PNPRO")


def parse_gspn_pnpro(file):
    """
    Parse GSPN from PNPRO file.
    :param file: File.
    :return: GSPN.
    """
    tree = ET.parse(file)
    root = tree.getroot()
    assert root.tag == "project"
    gspn_xml = root[0]
    assert gspn_xml.tag == "gspn"
    gspn = Gspn(gspn_xml.attrib["name"])
    nodes_xml = gspn_xml.find("nodes")
    arcs_xml = gspn_xml.find("edges")

    # Places
    for node in nodes_xml.findall("place"):
        name = node.attrib["name"]
        tokens = int(node.attrib.get("marking", 0))
        position = Position(float(node.attrib["x"]), float(node.attrib["y"]))
        label_x = node.attrib.get("label-x", 0)
        label_y = node.attrib.get("label-y", 0)
        label_shift = Position(float(label_x), float(label_y))
        gspn.places.append(Place(name, tokens, position, label_shift))

    # Transitions
    for node in nodes_xml.findall("transition"):
        name = node.attrib["name"]
        transition_type = node.attrib["type"]

        # Set positioning information
        position = Position(float(node.attrib["x"]), float(node.attrib["y"]))
        rotation = node.attrib.get("rotation", None)
        if rotation is not None:
            rotation = float(rotation)
        label_x = node.attrib.get("label-x", 0)
        label_y = node.attrib.get("label-y", 0)
        label_shift = Position(float(label_x), float(label_y))

        # Create transitions
        if transition_type == "EXP":
            delay = node.attrib["delay"]
            nservers = node.attrib["nservers"]
            gspn.transitions.append(TimedTransition(name, delay, nservers, position, rotation, label_shift))
        else:
            assert transition_type == "IMM"
            gspn.transitions.append(ImmediateTransition(name, position, rotation, label_shift))

    for arc in arcs_xml:
        source = arc.attrib["head"]
        target = arc.attrib["tail"]
        arc_type = arc.attrib["kind"]
        if arc_type == "INPUT":
            gspn.arcs.append(Arc(source, target, ArcTypes.INPUT))
        elif arc_type == "OUTPUT":
            # Switch source and target to let transition be source
            gspn.arcs.append(Arc(target, source, ArcTypes.OUTPUT))
        else:
            assert arc_type == "INHIBITOR"
            gspn.arcs.append(Arc(source, target, ArcTypes.INHIBITOR))
    return gspn


def parse_gspn(file):
    """
    Parse GSPN from file.
    :param file: File.
    :return: GSPN.
    """
    if is_pnpro_file(file):
        return parse_gspn_pnpro(file)
    else:
        raise IOError("File type of '{}' not known.".format(file))
