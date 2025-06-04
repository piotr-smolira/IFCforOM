import ifcopenshell
import ifcopenshell.util
from ifcopenshell.util import element, schema, attribute

# import ifcopenshell.ifcopenshell_wrapper as W
import rdflib
from rdflib import Graph, Namespace, RDF, RDFS, OWL

# 1. Open the IfC file

model = ifcopenshell.open("src/inputs/smallhouse.ifc")
E = ifcopenshell.util.element
W = ifcopenshell.ifcopenshell_wrapper

# 2. Get the schema
schema_version = model.schema

# 3. Get the schema version to wrapper
ifc = ifcopenshell.ifcopenshell_wrapper.schema_by_name(schema_version)

# 4. Set up Graph
g = Graph()

# 5. Declare namespaces
IFC = Namespace("https://example.org/ifc#")
g.bind("ifc", IFC)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)

# 6. Loop through all instances:
for entity in model:
    # print(entity)
    # print(entity.is_a())
    entity_declaration = ifc.declaration_by_name(entity.is_a())
    # print(f"Entity: {dir(entity_declaration)}")
    for attr in entity_declaration.all_attributes():
        print(attr)
    # print(entity.get_info())
    # print(entity.is_a())
    # if isinstance(entity, W.entity):
    # print(entity.Name)
    # for attr in entity.all_attributes():
    #    print(attr)


for entity in model:
    # It prints out entire entity as it appears in IFC file, e.g
    print("The STEP entity is: ", entity)
    # You can get info about attributes of an instance as you normally would, e.g. name, type, get_info()
    print(entity.get_info())
    # Get entity type
    print(entity.is_a())
    # Get entity name. IF statement is necessary to ensure that the entity is actual instance such as walls, properties, tasks etc.
    # For more information check submodule: ifcopenshell.entity_instance
    # if isinstance(entity, ifcopenshell.ifcopenshell_wrapper.entity_instance):
    if hasattr(entity, "Name"):
        print(entity.Name)


"""
# 6. Loop through all declarations and get ones that are in the IFC model
for decl in ifc.declarations():
    if isinstance(decl, W.entity):
        # print(decl.name())
        # Loop through all instance of the model by type name. Instead of explicitly findning one type after another with model.by_type("IfcWall"), declarations' names are used.
        for instance in model.by_type(decl.name()):
            # print(f"Entity: {decl.name()}")
            print(instance)
# Get all entities in the IFC file
# Get all types used in the file
types_in_file = set(entity.is_a() for entity in model)

# Iterate over each type and print the entities
# for ifc_type in sorted(types_in_file):
# entities = model.by_type(ifc_type)
# for entity in entities:
# print(f"{ifc_type} - {getattr(entity, 'GlobalId', 'No GlobalId')}")

"""

"""
# 4. Loop through all declarations and print the existing ones
for entity in ifc.declarations():
    if isinstance(entity, W.entity):
        # Entities
        # print(entity.name())
        for instance in model.by_type(entity.name()):
            # print(f"Entity: {entity.name()}, INFO: {instance.get_info()}")
            # print(entity.name())
            # print(instance)
            entity_uri = IFC[entity.name() + "_" + str(instance.id())]

            for attr in instance.get_info().keys():
                # print(f"Attribute: {attr}, Value: {instance.get_info()[attr]}")
                attr_value = instance.get_info()[attr]
                # attr_type = instance.attribute_type(attr)
                # print(instance)
                # print(f"Attribute: {attr}, Type: {attr_type}, Value: {attr_value}")
                # print(f"Attribute: {attr}, Value: {attr_value}")
                if isinstance(attr_value, list):

                    for value in attr_value:
                        g.add((entity_uri, IFC[attr], rdflib.Literal(value)))
                else:
                    g.add((entity_uri, IFC[attr], rdflib.Literal(attr_value)))

            g.add((entity_uri, RDF.type, OWL.Class))
"""
# print(
#     "Aggregation: ",
#     entity.name(),
#     "    -----    ",
#     E.get_aggregate(instance),
# )
# print(
#     "Components: ",
#     entity.name(),
#     "    -----    ",
#     E.get_components(instance),
# )
# print(
#     "Containted: ",
#     entity.name(),
#     "    -----    ",
#     E.get_contained(instance),
# )

# Get subtypes
# subtypes = ifcopenshell.util.schema.get_subtypes(entity)
# print(
#    f"Entity: {entity.name()}, Subtypes: {[subtype.name() for subtype in subtypes]}"
# )

g.serialize(destination="src/outputs/smallhouse-1.ttl", format="turtle")

"""
# Give me one wall
wall = 

any_attry = wall.GlobalId
print(f"GlobalId: {any_attry}")
attr_type = wall.attribute_type("GlobalId")
print(f"Attribute Type: {attr_type}")
# print(wall.__class__)
print(wall.__getattr__)
# attr_type = W.entity_instance.get_attribute_category(wall, "GlobalId")
"""

"""
printthis = ifc.declaration_by_name("IfcWall")
# print(f"Attribute Type: {printthis}")
# print(dir(printthis))
for decl in ifc.declarations():
    if isinstance(decl, W.entity):
        print("Declaration:      ", decl)
        for attr in decl.all_attributes():
            ty = attr.type_of_attribute()
            print("Attribute type:      ", ty)
            while isinstance(ty, W.aggregation_type):
                ty = ty.type_of_element()
                print("Element type:       ", ty)
            while isinstance(ty, W.named_type):
                ty = ty.declared_type()
                print("Declared type:      ", ty)
            # if isinstance(ty, (W.entity, W.select_type)):
"""


print("-----------------")
wall = model.by_type("IfcWall")[0]
wall_declaration = ifc.declaration_by_name("IfcWall")
for attr in wall_declaration.all_attributes():
    # print(attr)
    # print(attr.type_of_attribute())
    print(dir(attr.type_of_attribute()))
    someattribute = attr.type_of_attribute().as_named_type()


for attr_idx, value in enumerate(wall):
    if value is None:
        continue
print(wall.get_info())


""""
for decl in ifc.declarations():
    if isinstance(decl, W.entity):
        for attr in decl.all_attributes():
            ty = attr.type_of_attribute()
            # print(ty)
"""

print("nominal value: ", model.by_type("IfcPropertySingleValue")[0].NominalValue)
myinst = model.by_type("IfcPropertySingleValue")[0].NominalValue
print(isinstance(myinst, ifcopenshell.ifcopenshell_wrapper.entity_instance))
myinst2 = model.by_type("IfcWall")[2].Name
print(myinst2)
print(isinstance(myinst2, ifcopenshell.ifcopenshell_wrapper.entity_instance))
# my = W.attribute.type_of_attribute("PredefinedType")

"""
# Give me wall attribute types
for attr in wall.get_info().keys():
    print(
        f"Attribute: {attr}, Type: {wall.attribute_type(attr)}, Value: {wall.get_info()[attr]}"
    )
"""
for i in wall.get_info():
    print(i)

# ifcopenshell_wrapper.entity_instance


# I think it more clear now for me. The if statement fixed issue for IfcLocalPlacement has no attribute 'Name', but at the same time I can't say if this omitted some instances that have attribute 'Name'.
