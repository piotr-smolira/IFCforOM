import rdflib, ifcopenshell
from rdflib.namespace import *

F = ifcopenshell.open("input.ifc")
G = rdflib.Graph()


IFC = Namespace("http://example.org/mini-ifc/%s/" % F.schema)
INST = Namespace("http://example.org/ifc-files/i.ifc/")


def format_uri(inst):
    return INST.term("%s_%d" % (inst.is_a(), inst.id()))


def format_value(val, base):

    if isinstance(val, ifcopenshell.entity_instance):
        return format_uri(val)

    elif isinstance(val, (tuple, list)):

        if not val:
            return RDF.nil

        list_uri = base + "_list"
        G.add((list_uri, RDF.type, RDF.List))
        G.add((list_uri, RDF.first, format_value(val[0], base + "_first")))
        G.add((list_uri, RDF.rest, format_value(val[1:], base + "_rest")))
        return list_uri

    else:
        return rdflib.Literal(val)


for inst in F:

    G.add((format_uri(inst), RDF.type, IFC.term(inst.is_a())))
    for attr_idx, value in enumerate(inst):
        if value is None:
            continue
        predicate = inst.attribute_name(attr_idx)
        G.add(
            (
                format_uri(inst),
                IFC.term(predicate),
                format_value(value, format_uri(inst) + "_" + predicate),
            )
        )

G.serialize(destination="output.ttl", format="turtle")
