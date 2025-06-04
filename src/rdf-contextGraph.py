from rdflib import Graph, Namespace, URIRef
import json

# Smalll script to preserve @context and @graph in JSON-LD.
# Rdflib does not support it.
# And this can be turned into a function and used when you want to update JSON-LD files.


# Load original graph
g = Graph()
g.parse("inputs/bridgeparts.jsonld")

# Extract the original context from the input file
with open("bridgeparts.jsonld", "r") as f:
    original_data = json.load(f)
    original_context = original_data.get("@context", {})

# Create a custom JSON-LD serialization
output = {"@context": original_context, "@graph": []}

# Define namespaces for querying
EX = Namespace("https://example.org/ifc#")
SCHEMA = Namespace("https://schema.org/")

# Get all subjects in the graph
subjects = set()
for s, p, o in g:
    subjects.add(s)

# Process each subject
for subject in subjects:
    subject_uri = str(subject)
    entity = {"@id": subject_uri}

    # Get type
    for _, _, obj in g.triples(
        (subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), None)
    ):
        entity["type"] = f"ex:{obj.split('#')[-1]}"
        break

    # Get name
    for _, _, obj in g.triples((subject, SCHEMA.name, None)):
        entity["name"] = str(obj)

    # Get compositionType
    for _, _, obj in g.triples((subject, EX.compositionType, None)):
        entity["compositiontype"] = str(obj)

    # Get predefinedType
    for _, _, obj in g.triples((subject, EX.predefinedType, None)):
        entity["predefinedtype"] = str(obj)

    # Get aggregates
    aggregates = []
    for _, _, obj in g.triples((subject, EX.aggregates, None)):
        aggregates.append(str(obj))
    entity["aggregates"] = aggregates

    output["@graph"].append(entity)

# Write the result to a file
with open("outputs/bridgeparts-formatted.jsonld", "w") as f:
    json.dump(output, f, indent=2)

print("Saved with preserved context and format to bridgeparts-formatted.jsonld")
