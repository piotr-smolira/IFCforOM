from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, split_uri
import uuid

g = Graph()
g.parse("inputs/bridgeparts.jsonld")

# Namespaces
EX = Namespace("https://example.org/ifc#")
SCHEMA = Namespace("https://schema.org/")
BASE = "https://example.org/ifc/"


# Replace URIs with UUIDs if set to True
if True:  # Set to True if you want to replace URIs
    # Find all subjects to replace
    old_uris = set(s for s in g.subjects() if isinstance(s, URIRef))

    # Generate new URIs
    uri_map = {old: URIRef(BASE + str(uuid.uuid4())) for old in old_uris}

    # Create a new graph with replaced URIs
    new_graph = Graph()
    for s, p, o in g:
        new_s = uri_map.get(s, s)
        new_o = uri_map.get(o, o) if isinstance(o, URIRef) else o
        new_graph.add((new_s, p, new_o))

    # Replace the original graph with the new one
    g = new_graph

# Namespace binding
g.bind("ex", "https://example.org/ifc#")
g.bind("schema", "https://schema.org/")

# Output
g.serialize(destination="outputs/bridgeparts.ttl", format="turtle")
