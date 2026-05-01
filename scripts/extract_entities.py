#!/usr/bin/env python3
"""
Generate a <kg>_entities.csv using the FRINK SPARQL endpoint.

Supports both the KG-specific endpoint and the federation endpoint with FROM <graph>.
"""

import csv
import re
import sys
import time
from collections import defaultdict
from typing import Dict, Iterable, List, Set

import requests

KG = ""
GRAPH_URI = ""
ENDPOINTS: List[str] = []
OUTFILE = ""
HEADER = ["URI", "Label", "Description", "Type", "EdgePropertyOf", "SourceClass", "TargetClass"]

PREFIXES = """
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX dc:   <http://purl.org/dc/elements/1.1/>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
"""

DESCRIPTION_PREDICATES = "rdfs:comment|skos:definition|dct:description|dc:description"


def configure_kg(kg: str) -> None:
    """Configure graph, endpoints, and output file for the command-line KG argument."""
    if not kg or kg.startswith("-") or not re.fullmatch(r"[A-Za-z0-9_-]+", kg):
        raise ValueError("KG must be a non-empty identifier using only letters, numbers, underscores, or hyphens")

    global KG, GRAPH_URI, ENDPOINTS, OUTFILE
    KG = kg
    GRAPH_URI = f"https://purl.org/okn/frink/kg/{KG}"
    ENDPOINTS = [
        f"https://frink.apps.renci.org/{KG}/sparql",
        "https://frink.apps.renci.org/federation/sparql",
    ]
    OUTFILE = f"{KG}_entities.csv"


def _decode_tsv_cell(cell: str) -> str:
    """Decode SPARQL Results TSV cells. IRIs are returned as <...>; literals are quoted."""
    cell = cell.strip()
    if not cell:
        return ""
    if cell.startswith("<") and cell.endswith(">"):
        return cell[1:-1]
    # Minimal literal handling; csv.reader already unescapes tabs/newlines at row level poorly,
    # so keep this conservative and robust.
    if cell.startswith('"'):
        # Strip datatype/lang suffix if present after closing quote.
        m = re.match(r'^"(.*)"(?:@[a-zA-Z-]+|\^\^<[^>]+>)?$', cell)
        if m:
            s = m.group(1)
            return (
                s.replace(r"\t", "\t")
                 .replace(r"\n", " ")
                 .replace(r"\r", " ")
                 .replace(r'\"', '"')
                 .replace(r"\\", "\\")
            ).strip()
    return cell


def run_select_tsv(query: str, endpoint: str, timeout: int = 180) -> List[Dict[str, str]]:
    """Run SELECT query and parse text/tab-separated-values; avoids JSON parser failures."""
    last = None
    headers = {"Accept": "text/tab-separated-values"}
    for method in ("POST", "GET"):
        for attempt in range(3):
            try:
                if method == "POST":
                    r = requests.post(endpoint, data={"query": query}, headers=headers, timeout=timeout)
                else:
                    r = requests.get(endpoint, params={"query": query}, headers=headers, timeout=timeout)
                r.raise_for_status()
                text = r.text.replace("\x00", "")
                lines = text.splitlines()
                if not lines:
                    return []
                # SPARQL TSV header cells start with ?var
                header = [h[1:] if h.startswith("?") else h for h in lines[0].split("\t")]
                out = []
                for line in lines[1:]:
                    if not line.strip():
                        continue
                    parts = line.split("\t")
                    # Pad/truncate defensively, since literals may occasionally contain malformed tabs.
                    if len(parts) < len(header):
                        parts += [""] * (len(header) - len(parts))
                    if len(parts) > len(header):
                        parts = parts[: len(header) - 1] + [" ".join(parts[len(header) - 1 :])]
                    out.append({k: _decode_tsv_cell(v) for k, v in zip(header, parts)})
                return out
            except Exception as e:
                last = e
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"SPARQL TSV query failed against {endpoint}: {last}")


def run_ask(query: str, endpoint: str, timeout: int = 60) -> bool:
    headers = {"Accept": "application/sparql-results+json"}
    r = requests.post(endpoint, data={"query": query}, headers=headers, timeout=timeout)
    r.raise_for_status()
    return bool(r.json().get("boolean"))


def select_query(body: str, endpoint: str, select: str = "*", distinct: bool = True) -> str:
    distinct_s = "DISTINCT " if distinct else ""
    if endpoint.endswith("/federation/sparql"):
        return PREFIXES + f"\nSELECT {distinct_s}{select} FROM <{GRAPH_URI}> WHERE {{\n{body}\n}}"
    return PREFIXES + f"\nSELECT {distinct_s}{select} WHERE {{\n{body}\n}}"


def pick_endpoint() -> str:
    for endpoint in ENDPOINTS:
        probes = [
            PREFIXES + "\nASK WHERE { ?s ?p ?o }",
            PREFIXES + f"\nASK WHERE {{ GRAPH <{GRAPH_URI}> {{ ?s ?p ?o }} }}",
        ]
        for q in probes:
            try:
                if run_ask(q, endpoint):
                    print(f"Using endpoint: {endpoint}", file=sys.stderr)
                    return endpoint
            except Exception as e:
                print(f"Endpoint probe failed for {endpoint}: {e}", file=sys.stderr)
    raise RuntimeError("No endpoint responded to ASK probe")


def label_from_uri(uri: str) -> str:
    x = uri.rstrip("/#").split("#")[-1].split("/")[-1]
    x = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", x)
    return x.replace("_", " ").replace("-", " ")


def get_classes(endpoint: str) -> Set[str]:
    classes: Set[str] = set()

    class_queries = [
        ("explicit owl/rdfs classes", """
          { ?class a owl:Class . FILTER(isIRI(?class)) }
          UNION
          { ?class a rdfs:Class . FILTER(isIRI(?class)) }
        """),
        ("biolink categories", """
          ?x biolink:category ?class .
          FILTER(isIRI(?class))
        """),
        ("rdf:type object classes", """
          ?x a ?class .
          FILTER(isIRI(?class))
          FILTER(?class NOT IN (rdf:Property, owl:ObjectProperty, owl:DatatypeProperty, owl:AnnotationProperty))
        """),
    ]

    for name, body in class_queries:
        q = select_query(body, endpoint, select="?class")
        try:
            rows = run_select_tsv(q, endpoint, timeout=240)
            before = len(classes)
            classes.update(r.get("class", "") for r in rows if r.get("class"))
            print(f"Class discovery ({name}): +{len(classes) - before}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: class discovery failed ({name}): {e}", file=sys.stderr)

    return classes


def get_predicates(endpoint: str) -> Dict[str, Dict[str, Set[str]]]:
    pred: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: {"sources": set(), "targets": set()})

    # First get only distinct predicate IRIs. This should be small for oard-kg.
    q = select_query("""
      ?s ?predicate ?o .
      FILTER(isIRI(?predicate))
    """, endpoint, select="?predicate")
    for r in run_select_tsv(q, endpoint, timeout=240):
        p = r.get("predicate", "")
        if p and p != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
            pred[p]
    print(f"Predicate discovery: {len(pred)} predicates", file=sys.stderr)

    # For each predicate, infer source/target from categories. This avoids a giant all-predicate join.
    for idx, p in enumerate(sorted(pred), 1):
        body = f"""
          ?s <{p}> ?o .
          OPTIONAL {{ ?s biolink:category ?sourceClass . FILTER(isIRI(?sourceClass)) }}
          OPTIONAL {{ ?o biolink:category ?targetClass . FILTER(isIRI(?targetClass)) }}
        """
        q2 = select_query(body, endpoint, select="?sourceClass ?targetClass")
        try:
            for r in run_select_tsv(q2, endpoint, timeout=180):
                if r.get("sourceClass"):
                    pred[p]["sources"].add(r["sourceClass"])
                if r.get("targetClass"):
                    pred[p]["targets"].add(r["targetClass"])
            print(f"  [{idx}/{len(pred)}] source/target inferred for {label_from_uri(p)}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: source/target inference failed for {p}: {e}", file=sys.stderr)

    # Add explicit rdf:Property/owl property declarations, if any exist but are unused in triples.
    q_props = select_query("""
      { ?predicate a rdf:Property . }
      UNION { ?predicate a owl:ObjectProperty . }
      UNION { ?predicate a owl:DatatypeProperty . }
      FILTER(isIRI(?predicate))
    """, endpoint, select="?predicate")
    try:
        for r in run_select_tsv(q_props, endpoint, timeout=120):
            if r.get("predicate"):
                pred[r["predicate"]]
    except Exception as e:
        print(f"Warning: explicit property discovery failed: {e}", file=sys.stderr)

    # Add explicit rdfs:domain/rdfs:range when available.
    for p in sorted(pred):
        q_dr = select_query(f"""
          OPTIONAL {{ <{p}> rdfs:domain ?sourceClass . FILTER(isIRI(?sourceClass)) }}
          OPTIONAL {{ <{p}> rdfs:range ?targetClass . FILTER(isIRI(?targetClass)) }}
        """, endpoint, select="?sourceClass ?targetClass")
        try:
            for r in run_select_tsv(q_dr, endpoint, timeout=60):
                if r.get("sourceClass"):
                    pred[p]["sources"].add(r["sourceClass"])
                if r.get("targetClass"):
                    pred[p]["targets"].add(r["targetClass"])
        except Exception:
            pass

    return pred


def metadata_for(uris: Iterable[str], endpoint: str) -> Dict[str, Dict[str, str]]:
    uri_list = sorted(set(u for u in uris if u))
    meta = {u: {"label": "", "description": ""} for u in uri_list}
    batch = 25
    for i in range(0, len(uri_list), batch):
        vals = " ".join(f"<{u}>" for u in uri_list[i : i + batch])
        body = f"""
          VALUES ?uri {{ {vals} }}
          OPTIONAL {{ ?uri rdfs:label ?label . FILTER(LANG(?label) = "" || LANGMATCHES(LANG(?label), "en")) }}
          OPTIONAL {{ ?uri {DESCRIPTION_PREDICATES} ?description . FILTER(LANG(?description) = "" || LANGMATCHES(LANG(?description), "en")) }}
        """
        q = select_query(body, endpoint, select="?uri ?label ?description", distinct=False)
        try:
            for r in run_select_tsv(q, endpoint, timeout=120):
                u = r.get("uri", "")
                if not u or u not in meta:
                    continue
                if r.get("label") and not meta[u]["label"]:
                    meta[u]["label"] = r["label"]
                if r.get("description") and not meta[u]["description"]:
                    meta[u]["description"] = r["description"]
        except Exception as e:
            print(f"Warning: metadata batch failed: {e}", file=sys.stderr)
    return meta


def detect_edge_properties(endpoint: str, predicates: Dict[str, Dict[str, Set[str]]]) -> Dict[str, str]:
    mappings: Dict[str, str] = {}
    # Common RDF reification pattern.
    body = """
      ?edge rdf:predicate ?edgePredicate ;
            ?property ?value .
      FILTER(isIRI(?edgePredicate))
      FILTER(isIRI(?property))
      FILTER(?property NOT IN (rdf:subject, rdf:predicate, rdf:object, rdf:type))
    """
    q = select_query(body, endpoint, select="?property ?edgePredicate")
    try:
        for r in run_select_tsv(q, endpoint, timeout=180):
            prop = r.get("property", "")
            edge_pred = r.get("edgePredicate", "")
            if prop and edge_pred:
                mappings[prop] = edge_pred
    except Exception as e:
        print(f"Warning: RDF reification edge-property detection failed: {e}", file=sys.stderr)

    # Heuristic fallback used by many OKN reified/analysis-result schemas.
    for p, io in predicates.items():
        if p in mappings:
            continue
        if any(s.endswith("LogOddsAnalysisResult") or s.endswith("ConceptCountAnalysisResult") for s in io["sources"]):
            mappings[p] = "https://w3id.org/biolink/vocab/has_study_results"
    return mappings


def clean_text(s: str) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", s or "").strip()


def join(vals: Iterable[str]) -> str:
    return "|".join(sorted(v for v in vals if v))


def write_csv(classes: Set[str], predicates: Dict[str, Dict[str, Set[str]]], metadata: Dict[str, Dict[str, str]], edge_props: Dict[str, str]):
    rows_out: List[List[str]] = []

    for uri in sorted(classes):
        rows_out.append([
            uri,
            clean_text(metadata.get(uri, {}).get("label") or label_from_uri(uri)),
            clean_text(metadata.get(uri, {}).get("description", "")),
            "Class",
            "",
            "",
            "",
        ])

    for uri, io in sorted(predicates.items()):
        rows_out.append([
            uri,
            clean_text(metadata.get(uri, {}).get("label") or label_from_uri(uri)),
            clean_text(metadata.get(uri, {}).get("description", "")),
            "Predicate",
            edge_props.get(uri, ""),
            join(io["sources"]),
            join(io["targets"]),
        ])

    with open(OUTFILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER)
        w.writerows(rows_out)

    # Validation requested by user.
    with open(OUTFILE, newline="", encoding="utf-8") as f:
        parsed = list(csv.reader(f))
    assert parsed[0] == HEADER, f"Header mismatch: {parsed[0]}"
    bad = [i for i, r in enumerate(parsed, start=1) if len(r) != 7]
    assert not bad, f"Rows without exactly 7 columns: {bad[:10]}"
    bad_types = [r[3] for r in parsed[1:] if r[3] not in {"Class", "Predicate"}]
    assert not bad_types, f"Invalid Type values: {bad_types[:10]}"

    print(f"Wrote {OUTFILE} with {len(rows_out)} entities", file=sys.stderr)
    print("Validation passed: header, exactly 7 columns/row, parseable CSV, Type in {Class, Predicate}", file=sys.stderr)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <kg>", file=sys.stderr)
        print("Example: create_entities.py rdkg", file=sys.stderr)
        sys.exit(2)

    try:
        configure_kg(sys.argv[1])
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    endpoint = pick_endpoint()
    classes = get_classes(endpoint)
    predicates = get_predicates(endpoint)
    uris = set(classes) | set(predicates.keys())
    metadata = metadata_for(uris, endpoint)
    edge_props = detect_edge_properties(endpoint, predicates)
    write_csv(classes, predicates, metadata, edge_props)


if __name__ == "__main__":
    main()
