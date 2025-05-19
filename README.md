# Example JSONLD/TTL to IFC

This script explores possibilities setting up project using Semantic Web Technologies and exporting it to IFC.

# Installation
1. Create Python environment `python -m venv .env` or, e.g.  `python3.12 -m venv .env` for specific Python version.
Use `requirements.txt` to get packages.
Just in case: `pip install ifcopenshell` and `pip install rdflib`

# Guide
There are two versions of development - **Simple** and with **JSON-LD**.

## Simple

Quick one - from scratch and very rough in `simple.py`.
The output is `output-simple.ifc`.

The output gives simple bridge spatial structure breakdown, IfcBearing, 2 IfcSensors, IfcSensorType, 2 Psets. Now example on IfcTimeSeries is lacking.

---

## With JSON-LD

Some of the files are tests.
The main ones are:
- jsonLD-to-IFC.py
- bridgeparts.jsonld OR bridgeparts.ttl
- output-fromJSONLD.ifc

# How to use it?
Just run `jsonLD-to-IFC.py`

# How to modify it?
You can update your input file (`bridgeparts.py`).
Adjust `jsonLD-to-IFC.py` accordingly.

# Current TODOs:
[] Example of using TimeSeries.

[] Making sure aggregation does not violate schema (COMPLEX, ELEMENT, PARTIAL; and Bridge a BridgePart - it should not allow me to have IfcBridgePart aggregating IfcBridge (but maybe it should essentially in some scenarios?)).

# Shortcomings
The script can go only through just a few things like project, spatial containers, elements, psets.