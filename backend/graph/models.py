from typing import List, Dict, Any
from enum import Enum
from dataclasses import dataclass, field

class EntityType(str, Enum):
    Person = "Person"
    Team = "Team"
    Project = "Project"
    Service = "Service"
    Incident = "Incident"
    Document = "Document"
    Ticket = "Ticket"
    Decision = "Decision"

class RelationshipType(str, Enum):
    WORKS_ON = "WORKS_ON"
    OWNS = "OWNS"
    CAUSED = "CAUSED"
    DISCUSSED_IN = "DISCUSSED_IN"
    REFERENCES = "REFERENCES"
    DEPENDS_ON = "DEPENDS_ON"
    CREATED = "CREATED"
    RESOLVED = "RESOLVED"
    BELONGS_TO = "BELONGS_TO"

@dataclass
class GraphNode:
    """
    Model representing a node/entity in the knowledge graph.
    """
    node_id: str
    label: EntityType
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GraphEdge:
    """
    Model representing a directed relationship link in the knowledge graph.
    """
    source_id: str
    target_id: str
    type: RelationshipType
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GraphDelta:
    """
    Represents changes to be applied to the knowledge graph.
    """
    nodes_to_upsert: List[GraphNode] = field(default_factory=list)
    edges_to_upsert: List[GraphEdge] = field(default_factory=list)
    nodes_to_delete: List[str] = field(default_factory=list)
    edges_to_delete: List[str] = field(default_factory=list)
