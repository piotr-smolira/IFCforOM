import ifcopenshell
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, split_uri
from ifcopenshell.api import root, attribute, aggregate

# Create an IFC file with IFC4X3_ADD2 schema
ifc = ifcopenshell.file(schema="IFC4X3_ADD2")

# Get project outline in JSON-LD
g = Graph()
g.parse("inputs/bridgeparts.jsonld")

# Define namespaces
EX = Namespace("https://example.org/ifc#")
SCHEMA = Namespace("https://schema.org/")

# Spatial containers creation
entity_list = []

# Map RDF URIs to created IFC entities
uri_to_ifc_entity = {}

# Create a project, site, bridge, and bridge parts
for s in g.subjects(RDF.type, None):
    class_type = g.value(s, RDF.type)
    ifctype = split_uri(class_type)[1]
    composition_type = g.value(s, EX.compositionType)
    predefined_type = g.value(s, EX.predefinedType)
    description = g.value(s, EX.description)
    name = g.value(s, SCHEMA.name)

    if ifctype == "IfcProject":
        entity = ifcopenshell.api.root.create_entity(ifc, ifc_class=ifctype, name=name)
    else:
        # Create a new entity in the IFC file
        entity = ifcopenshell.api.root.create_entity(
            ifc, ifc_class=ifctype, predefined_type=predefined_type, name=name
        )

    if composition_type:
        # Edit the attributes of the entity
        entity = ifcopenshell.api.attribute.edit_attributes(
            ifc,
            product=entity,
            attributes={
                "CompositionType": composition_type,
                "Description": description,
            },
        )
    else:
        entity = ifcopenshell.api.attribute.edit_attributes(
            ifc,
            product=entity,
            attributes={
                "Description": description,
            },
        )

    entity_list.append(entity)

    # Save mapping from RDF URI to IFC entity
    uri_to_ifc_entity[str(s)] = entity


# Aggregate the entities
# It does not automatically resolve the hierarchy (Project -> Site -> Bridge -> BridgeParts (with composition types)). It uses the aggregation property from the JSON-LD file.
for s, p, o in g.triples((None, EX.aggregates, None)):
    relating_uri = str(s)
    related_uri = str(o)

    relating_object = uri_to_ifc_entity.get(relating_uri)
    related_object = uri_to_ifc_entity.get(related_uri)

    if relating_object and related_object:
        # Assign aggregation (support multiple)
        # Assign related object (instances) to relating object (type)
        if relating_object.is_a("IfcPropertyDefinition"):  # To exclude Psets
            None
        elif relating_object.is_a("IfcTypeProduct"):
            ifcopenshell.api.type.assign_type(
                ifc, related_objects=[related_object], relating_type=relating_object
            )
        else:
            aggregate.assign_object(
                ifc, relating_object=relating_object, products=[related_object]
            )


"""
# Generate Psets
for s, p, o in g.triples((None, EX.hasPset, None)):
    subject_uri = str(s)
    related_uri = str(o)

    subject_object = uri_to_ifc_entity.get(subject_uri)
    related_object = uri_to_ifc_entity.get(related_uri)

    if subject_object and related_object:
        # Assign Pset to the object
        ifcopenshell.api.pset.assign_pset(
            ifc, product=subject_object, pset=related_object
        )
"""

ifc.write("outputs/fromJSONLD.ifc")
