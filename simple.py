import ifcopenshell
import ifcopenshell.util.pset
from ifcopenshell import util
from ifcopenshell.api import root, attribute, spatial, geometry


# Create an IFC file with the specified schema
ifc = ifcopenshell.file(schema="IFC4x3_ADD2")

# Create a project entity
project = ifcopenshell.api.root.create_entity(
    ifc, ifc_class="IfcProject", name="Operation and Maintenance"
)

# Create a site
site = ifcopenshell.api.root.create_entity(ifc, ifc_class="IfcSite", name="Bridge Site")

# Create a bridge
bridge = ifcopenshell.api.root.create_entity(
    ifc, ifc_class="IfcBridge", predefined_type="CABLE_STAYED", name="East Bridge"
)

# Create a bridge part

## Create abutments
bridge_abutment = ifcopenshell.api.root.create_entity(
    ifc,
    ifc_class="IfcBridgePart",
    predefined_type="ABUTMENT",
    name="Abutment 15",
)


## Change abutment composition type
ifcopenshell.api.attribute.edit_attributes(
    ifc, product=bridge_abutment, attributes={"CompositionType": "ELEMENT"}
)

# Assign project to site
ifcopenshell.api.aggregate.assign_object(ifc, products=[site], relating_object=project)

# Create aggregation of bridge topology
ifcopenshell.api.aggregate.assign_object(ifc, products=[bridge], relating_object=site)
ifcopenshell.api.aggregate.assign_object(
    ifc, products=[bridge_abutment], relating_object=bridge
)

bearing_01 = ifcopenshell.api.root.create_entity(
    ifc, ifc_class="IfcBearing", predefined_type="POT", name="Bearing AB15 SØ"
)

# Define sensor metadata
sensors = [
    # Temperature sensors
    {
        "name": "AB0170KTT-34",
        "type": "TEMPERATURESENSOR",
        "description": "Temperature sensor at bearing, Abutment 15 N -",
    },
    {
        "name": "AB0170KTT-43",
        "type": "TEMPERATURESENSOR",
        "description": "Temperature sensor at bearing, Abutment 15 S -",
    },
]

# Create sensor entities and store references
sensor_entities = {}

for sensor in sensors:
    entity = ifcopenshell.api.root.create_entity(
        ifc, ifc_class="IfcSensor", predefined_type=sensor["type"], name=sensor["name"]
    )
    ifcopenshell.api.attribute.edit_attributes(
        ifc, product=entity, attributes={"Description": sensor["description"]}
    )
    sensor_entities[sensor["name"]] = entity

# Assign sensors to spatial structures

ifcopenshell.api.spatial.assign_container(
    ifc,
    products=[
        bearing_01,
        sensor_entities["AB0170KTT-34"],
        sensor_entities["AB0170KTT-43"],
    ],
    relating_structure=bridge_abutment,
)

# Set the sensor type
sensor_type_temperature = ifcopenshell.api.root.create_entity(
    ifc, ifc_class="IfcSensorType", predefined_type="TEMPERATURESENSOR"
)

# Assign sensor type to sensor instances
for sensor in sensor_entities:
    ifcopenshell.api.type.assign_type(
        ifc,
        related_objects=[sensor_entities[sensor]],
        relating_type=sensor_type_temperature,
    )

# Add psets to type
sensor_temperature_pset = ifcopenshell.api.pset.add_pset(
    ifc, product=sensor_type_temperature, name="Pset_SensorTypeTemperatureSensor"
)

sensor_history_pset = ifcopenshell.api.pset.add_pset(
    ifc, product=sensor_type_temperature, name="Pset_SensorPHistory"
)

# Write the project to the IFC file
ifc.write("outputs/simple.ifc")
