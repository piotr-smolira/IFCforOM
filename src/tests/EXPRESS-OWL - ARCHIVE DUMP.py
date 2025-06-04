import ifcopenshell
import ifcopenshell.express
from ifcopenshell.express.express_parser import parse
from ifcopenshell.express import schema
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
from collections import defaultdict

# Step 1: Parse the EXPRESS file
mapping = parse("inputs/IFC4X3_RC1.exp")
schema = mapping.schema  # This gives you access to .entities

# Set up RDF graph
g = Graph()
IFC = Namespace("https://example.org/ifc#")
g.bind("ifc", IFC)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)

# print(type(schema))  # should say <class 'schema.Schema'>
# print(schema.entities.keys())
# print(next(iter(schema.entities.values())).__class__)

#

subtypes = defaultdict(list)
entity_subtypes = defaultdict(list)

# Loop over all entities in the schema
for entity_name, entity_type in schema.entities.items():
    # print(f"Processing entity: {entity}")

    entity_uri = IFC[entity_name]

    # Declare the entity as an owl:Class
    g.add((entity_uri, RDF.type, OWL.Class))

    # Add rdfs:label
    g.add((entity_uri, RDFS.label, Literal(entity_name)))

    if entity_type.supertypes:
        for supertype in entity_type.supertypes:
            # print(entity_type.name, "   SUPERTYPE of -    ", supertype)
            # print(
            #     supertype,
            #     "   SUPERTYPE of -    ",
            #     entity_type.name,
            # )
            # Add rdfs:subClassOf for inheritance
            g.add((entity_uri, RDFS.subClassOf, IFC[supertype]))

            # print(entity_name, "   -    ", entity_type.subtype)
            print(entity_name, "   -    ", entity_type.supertype)

    """
    # Add rdfs:subClassOf for inheritance
    if entity.subtype:
        # print(f"Processing entity: {entity.subtype.name} as subtype of {entity_name}")
        subtype_uri = IFC[entity.subtype.name]
        g.add((entity_uri, RDFS.subClassOf, subtype_uri))
    """


# Step 4: Output RDF
g.serialize(destination="outputs/IFC4X3_RC1.ttl", format="turtle")


""""
for entity_name, entity_type in schema.entities.items():
    if hasattr(entity_type, "supertypes") and entity_type.supertypes:
        for supertype in entity_type.supertypes:
            entity_subtypes[supertype].append(entity_name)
# Print the subtypes for each supertype
for supertype, subtypes in entity_subtypes.items():
    print(f"Supertype: {supertype}, Subtypes: {', '.join(subtypes)}")
"""


ifc = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4x3_ADD2")

g = Graph()
IFC = Namespace("https://example.org/ifc#")
g.bind("ifc", IFC)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)


for entity in ifc.declarations():
    # Entities
    print(entity.name())
    # print(entity.is_abstract())
    # Types

    # ifc_entity = ifcopenshell.ifcopenshell_wrapper.declaration.type(entity)
    # print(ifc_entity)
    # Enumerations

    # Select
    # print(f"Processing entity: {entity}")

    """
    if isinstance(entity, ifcopenshell.ifcopenshell_wrapper.entity):
        entity_uri = IFC[entity.name()]
        g.add((entity_uri, RDF.type, OWL.Class))
        g.add((entity_uri, RDFS.label, Literal(entity.name())))
        # print(f"Processing entity: {entity.supertype()} of {entity.name()}")
        # print(f"Entity: {entity}")

    if issubclass(entity, ifcopenshell.ifcopenshell_wrapper.entity):
        # supertype_uri = IFC[entity.supertype().name()]
        # g.add((entity_uri, RDFS.subClassOf, supertype_uri))
        print(f"  Supertype: {entity.supertype().name()}")
    """
    # if entity.
    # if ifcopenshell.util.schema.get_subtypes(ifc.declaration_by_name(entity.name)):
    #    continue
    #    print(f"Entity: {entity.name()} is a subtype of {entity.supertype()}")

    # print(f"Entity: {entity.name()}")
    # print(
    #    f"  Supertype: {entity.supertype().name() if entity.supertype() else 'None'}"
    # )
    # print(f"  Subtypes: {[subtype.name() for subtype in entity.subtypes()]}")
    # print(f"  Attributes: {[attr.name() for attr in entity.all_attributes()]}")
    # print(
    #    f"  Inverse Attributes: {[inv.name() for inv in entity.all_inverse_attributes()]}"
    # )
    # print("-" * 40)

# print("-------------------------------------------------------")
# print(dir(ifcopenshell.ifcopenshell_wrapper.entity))
# parse = express_parser.parse

# print(ifcopenshell.util.schema.get_subtypes(ifc.declaration_by_name("IfcSensor")))

g.serialize(destination="outputs/IFC4X3_RC1-custom.ttl", format="turtle")


mapping = parse("inputs/IFC4X3_RC1.exp")
schema = mapping.schema  # This gives you access to .entities

my_entity = ifcopenshell.ifcopenshell_wrapper.entity

declaration = schema.declaration_by_name("IfcSensor")
print(f"Entity: {declaration.is_abstract()}")


"""
# Step 1: Parse the EXPRESS file
mapping = parse("inputs/IFC4X3_RC1.exp")
schema = mapping.schema  # This gives you access to .entities

# Iterate over all entities in the schema
for entity_name, entity_type in schema.entities.items():
    # Print the entity name and its supertype(s)
    print(f"Entity: {entity_name}")
    if entity_type.supertypes:
        for supertype in entity_type.supertypes:
            print(f"  Supertype: {supertype}")

    if entity_type.subtype:
        print(f"  Subtype: {entity_type.subtype}")

"""


ifc = ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4x3_ADD2")

for entity in ifc.declarations():
    if hasattr(entity, "supertype"):

        entity_name = entity.name()
        entity = ifc.declaration_by_name(entity_name)
        print(f"Entity: {entity}")
        print("suuuuupertype", entity.supertype())

    if hasattr(entity, "subtypes"):
        entity_name = entity.name()
        entity = ifc.declaration_by_name(entity_name)
        print(f"Entity: {entity}")
        print("SUUUUUUBTYPE", entity.subtypes())

    entity_name = ifc.declaration_by_name(entity.name())
    print(f"Entity name: {entity_name}")
    if hasattr(entity, "ABSTRACT"):
        entity_name = entity.name()
        entity = ifc.declaration_by_name(entity_name)
        print(f"Entity: {entity}")
        print("ABSTRACT", entity.is_abstract())

    # print(dir(entity))
    # print(entity.all_attributes())

"""
entity = ifc.declaration_by_name("IfcSpatialElement")
print(f"Entity abstract: {entity.is_abstract()}")
print(f"Entity supertype: {entity.supertype()}")
print(f"Entity subtype: {entity.subtypes()}")
print(f"Entity supertypes: {ifcopenshell.util.schema.get_supertypes(entity)}")
print(f"Entity subtypes: {ifcopenshell.util.schema.get_subtypes(entity)}")
"""
entity = ifc.declaration_by_name("IfcSpatialElement")
print(entity.name())
