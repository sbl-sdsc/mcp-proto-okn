"""
Graph Registry for Proto-OKN Knowledge Graphs.

Loads and queries a catalog of knowledge graphs from registry.json.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GraphInfo:
    """Metadata for a single knowledge graph."""
    name: str
    display_name: str
    named_graph_uri: str
    endpoint_url: str
    domain_tags: List[str] = field(default_factory=list)
    description_summary: str = ""
    entity_types: Dict[str, Any] = field(default_factory=dict)
    identifier_namespaces: List[str] = field(default_factory=list)
    example_queries: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "display_name": self.display_name,
            "named_graph_uri": self.named_graph_uri,
            "endpoint_url": self.endpoint_url,
            "domain_tags": self.domain_tags,
            "description_summary": self.description_summary,
            "entity_types": self.entity_types,
            "identifier_namespaces": self.identifier_namespaces,
            "example_queries": self.example_queries,
        }


class GraphRegistry:
    """Registry of Proto-OKN knowledge graphs."""

    def __init__(self, registry_path: Optional[str] = None):
        if registry_path is None:
            # Default: look for registry.json relative to this package
            pkg_dir = os.path.dirname(os.path.abspath(__file__))
            # Try package location first, then config/ in project root
            candidates = [
                os.path.join(pkg_dir, "registry.json"),
                os.path.join(pkg_dir, "..", "..", "config", "registry.json"),
                os.path.join(os.getcwd(), "config", "registry.json"),
            ]
            for candidate in candidates:
                resolved = os.path.normpath(candidate)
                if os.path.exists(resolved):
                    registry_path = resolved
                    break
            if registry_path is None:
                raise FileNotFoundError(
                    f"registry.json not found. Searched: {[os.path.normpath(c) for c in candidates]}"
                )

        with open(registry_path) as f:
            data = json.load(f)

        self._graphs: Dict[str, GraphInfo] = {}
        self._aliases: Dict[str, str] = {}

        for entry in data:
            graph = GraphInfo(
                name=entry["name"],
                display_name=entry.get("display_name", entry["name"]),
                named_graph_uri=entry.get("named_graph_uri", ""),
                endpoint_url=entry.get("endpoint_url", ""),
                domain_tags=entry.get("domain_tags", []),
                description_summary=entry.get("description_summary", ""),
                entity_types=entry.get("entity_types", {}),
                identifier_namespaces=entry.get("identifier_namespaces", []),
                example_queries=entry.get("example_queries", []),
                aliases=entry.get("aliases", []),
            )
            self._graphs[graph.name] = graph
            for alias in graph.aliases:
                self._aliases[alias] = graph.name

    def list_all(self) -> List[Dict[str, Any]]:
        """Return metadata dicts for all graphs."""
        return [g.to_dict() for g in self._graphs.values()]

    def get(self, name: str) -> Optional[GraphInfo]:
        """Get a graph by name or alias. Returns None if not found."""
        canonical = self._aliases.get(name, name)
        return self._graphs.get(canonical)

    def resolve_name(self, name: str) -> Optional[str]:
        """Resolve an alias to canonical name. Returns None if not found."""
        canonical = self._aliases.get(name, name)
        if canonical in self._graphs:
            return canonical
        return None

    def filter_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Return graphs matching a domain tag (case-insensitive)."""
        domain_lower = domain.lower()
        return [
            g.to_dict() for g in self._graphs.values()
            if any(d.lower() == domain_lower for d in g.domain_tags)
        ]

    def filter_by_entity_type(self, entity_type: str) -> List[Dict[str, Any]]:
        """Return graphs containing an entity class (case-insensitive)."""
        et_lower = entity_type.lower()
        return [
            g.to_dict() for g in self._graphs.values()
            if any(c.lower() == et_lower for c in g.entity_types.get("classes", []))
        ]

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search all graphs by keyword matching. Returns all graphs sorted by relevance."""
        query_lower = query.lower()
        terms = query_lower.split()

        scored = []
        for graph in self._graphs.values():
            score = 0

            # Check description
            desc_lower = graph.description_summary.lower()
            for term in terms:
                if term in desc_lower:
                    score += 1

            # Check domain tags
            for tag in graph.domain_tags:
                for term in terms:
                    if term in tag.lower():
                        score += 2

            # Check entity classes
            for cls in graph.entity_types.get("classes", []):
                for term in terms:
                    if term in cls.lower():
                        score += 2

            # Check predicates
            for pred in graph.entity_types.get("predicates", []):
                for term in terms:
                    if term in pred.lower():
                        score += 1

            # Check example queries
            for ex in graph.example_queries:
                for term in terms:
                    if term in ex.lower():
                        score += 1

            # Check identifier namespaces
            for ns in graph.identifier_namespaces:
                for term in terms:
                    if term in ns.lower():
                        score += 1

            # Check graph name
            for term in terms:
                if term in graph.name.lower():
                    score += 1

            scored.append((score, graph))

        # Sort by score descending, then by name for stability
        scored.sort(key=lambda x: (-x[0], x[1].name))
        return [
            {**g.to_dict(), "relevance_score": s}
            for s, g in scored
        ]

    @property
    def graph_names(self) -> List[str]:
        """Return sorted list of all canonical graph names."""
        return sorted(self._graphs.keys())
