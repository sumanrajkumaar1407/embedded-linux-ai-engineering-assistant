from pathlib import Path
 
from src.core.dependency import DependencyGraph
from src.rca.dependency_builder import add_device_tree_dependencies
 
 
BASE = Path("data/sample/i2c_timeout/devicetree/board.dts")
 
 
def test_add_device_tree_dependencies():
    graph = DependencyGraph()
 
    graph = add_device_tree_dependencies(
        graph=graph,
        dts_file=BASE,
    )
 
    node_names = {node.name for node in graph.nodes}
 
    assert "i2c1" in node_names
    assert "temp_sensor@48" in node_names
 
    edges = {
        (edge.source, edge.target, edge.relationship)
        for edge in graph.edges
    }
 
    assert (
        "i2c1",
        "temp_sensor@48",
        "contains",
    ) in edges
