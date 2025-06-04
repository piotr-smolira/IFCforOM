import ifcopenshell
import ifcopenshell.util, ifcopenshell.express
from ifcopenshell.util import element, schema, attribute
import sys
import rdflib
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal

# Options for the file
raw_rdf = True

# Increase recursion limit for large IFC files. Because how rdflib library handles recursion you can hit maximum recursion depth with larger files.
sys.setrecursionlimit(10000000)

# Shorthands for modules
E = ifcopenshell.util.element
S = ifcopenshell.util.schema
W = ifcopenshell.ifcopenshell_wrapper

# 1. Open the IfC file

model = ifcopenshell.open("src/inputs/Duplex.ifc")

# 2. Get the schema

schema_version = model.schema

# 3. Get the schema version to wrapper

ifc = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema_version)

# 4. Set up Graph

g = Graph()

# 5. Declare namespaces and bind them ("in the darkness bind them")

IFC = Namespace("https://example.org/ifc#")
EXPR = Namespace("https://w3id.org/express#")
INST = Namespace("https://example.org/ifc/instances#")
g.bind("ifc", IFC)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)
g.bind("express", EXPR)


def format_uri(inst):
    return INST.term("%s_%d" % (inst.is_a(), inst.id()))


def format_value(val, base_uri):
    if isinstance(val, ifcopenshell.entity_instance):
        return INST[val.is_a() + "_" + str(val.id())]
    elif isinstance(val, (tuple, list)):
        if not val:
            return RDF.nil
        list_uri = base_uri + "_list"
        g.add((list_uri, RDF.type, RDF.List))
        g.add((list_uri, RDF.first, format_value(val[0], base_uri + "_first")))
        g.add((list_uri, RDF.rest, format_value(val[1:], base_uri + "_rest")))
        return list_uri

    else:
        return rdflib.Literal(val)


# 6. Loop through all instances


def to_rdf_lvl1(model, g, enabled=False):
    """
    Approach 1 - attributes of instances are presented as a literal for each instance, with references to other instances as URIs. RDF + RDF list (represents same structure as in IFC-STEP, i.e. globalID as string, other attributes as URIs).
    """
    for inst in model:
        # Instance URI
        inst_uri = INST[inst.is_a() + "_" + str(inst.id())]

        # Add first triple - instance class
        g.add((inst_uri, RDF.type, IFC[inst.is_a()]))

        # Add subClassOf
        # inst_declaration = S.get_declaration(inst)

        for attr_idx, value in enumerate(inst):
            if value is None:
                continue

            predicate = inst.attribute_name(attr_idx)
            print(f"Processing attribute: {inst.attribute_name(attr_idx)}")

            g.add(
                (
                    format_uri(inst),
                    IFC.term(predicate),
                    format_value(value, format_uri(inst) + "_" + predicate),
                )
            )


def to_rdf_lvl2(model, g, enabled=False):
    """
    Approach 2 - attributes of instances are presented as a separate node with a type based on the attribute name. RDF + RDF list + attributes as mix of literals and URIs (Same references as in IFC-STEP).
    """
    for inst in model:
        # Instance URI
        inst_uri = INST[inst.is_a() + "_" + str(inst.id())]

        # Add first triple - instance class
        g.add((inst_uri, RDF.type, IFC[inst.is_a()]))

        # Add subClassOf
        # inst_declaration = S.get_declaration(inst)

        for attr_idx, value in enumerate(inst):
            if value is None:
                continue

            predicate = inst.attribute_name(attr_idx)
            print(f"Processing attribute: {inst.attribute_name(attr_idx)}")

            # Create intermediate node URI for this attribute
            attr_node_uri = INST[predicate + "_" + str(inst.id())]

            # Add triple: instance -> predicate -> intermediate_node
            g.add((inst_uri, IFC.term(predicate), attr_node_uri))

            # Add triple: intermediate_node -> rdf:type -> AttributeType (optional)
            # This gives the intermediate node a type based on the attribute
            g.add((attr_node_uri, RDF.type, IFC[predicate]))

            # Add triple: intermediate_node -> hasValue -> actual_value
            # You can use a custom property like 'hasValue' or 'value'
            g.add(
                (
                    attr_node_uri,
                    IFC.hasValue,
                    format_value(value, format_uri(inst) + "_" + predicate),
                )
            )
    return


# Options:
functions = [(to_rdf_lvl1, True), (to_rdf_lvl2, False)]

to_rdf_lvl1(model, g, enabled=functions[0][1])
to_rdf_lvl2(model, g, enabled=functions[1][1])


# Output name is a custom string and name of the function
output_name = "Duplex_Piotr"

for func, enabled in functions:
    if enabled:
        # Clone or reset the graph if needed for each output
        g = rdflib.Graph()

        # Call the function
        func(model, g, enabled=True)

        # Get the function name
        func_name = func.__name__

        # Generate the filename
        output_path = f"src/outputs/{output_name}-{func_name}.ttl"

        # Serialize the output
        g.serialize(destination=output_path, format="turtle")

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    print("IFC to RDF conversion completed successfully.")
