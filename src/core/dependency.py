from dataclasses import dataclass, field
 
 
@dataclass
class DependencyNode:
    name: str
    node_type: str
    properties: dict[str, str] = field(default_factory=dict)
 
 
@dataclass
class DependencyEdge:
    source: str
    target: str
    relationship: str
 
 
@dataclass
class DependencyGraph:
    nodes: list[DependencyNode] = field(default_factory=list)
    edges: list[DependencyEdge] = field(default_factory=list)
 
    def add_node(self, node: DependencyNode) -> None:
        self.nodes.append(node)
 
    def add_edge(self, edge: DependencyEdge) -> None:
        self.edges.append(edge)
