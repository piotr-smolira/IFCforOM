import ifcopenshell
import ifcopenshell.express
from ifcopenshell.express.express_parser import parse
from ifcopenshell.express import schema
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
from collections import defaultdict

# Step 1: Parse the EXPRESS file
mapping = parse("src/inputs/IFC4X3_RC1.exp")
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
g.serialize(destination="src/outputs/IFC4X3_RC1.ttl", format="turtle")


""""
for entity_name, entity_type in schema.entities.items():
    if hasattr(entity_type, "supertypes") and entity_type.supertypes:
        for supertype in entity_type.supertypes:
            entity_subtypes[supertype].append(entity_name)
# Print the subtypes for each supertype
for supertype, subtypes in entity_subtypes.items():
    print(f"Supertype: {supertype}, Subtypes: {', '.join(subtypes)}")
"""
