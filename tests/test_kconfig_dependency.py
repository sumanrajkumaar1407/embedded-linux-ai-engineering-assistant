from pathlib import Path
 
from src.rca.dependency_builder import build_kconfig_dependency_graph
 
 
BASE = Path("data/sample/i2c_timeout/kernel/.config")
 
 
def test_kconfig_dependency_graph():
    graph = build_kconfig_dependency_graph(BASE)
 
    node_names = {node.name for node in graph.nodes}
 
    assert "CONFIG_I2C" in node_names
    assert "CONFIG_I2C_DESIGNWARE_CORE" in node_names
    assert "CONFIG_I2C_DESIGNWARE_PLATFORM" in node_names
 
    edges = {
        (edge.source, edge.target, edge.relationship)
        for edge in graph.edges
    }
 
    assert (
        "CONFIG_I2C",
        "CONFIG_I2C_DESIGNWARE_CORE",
        "depends_on",
    ) in edges
 
    assert (
        "CONFIG_I2C_DESIGNWARE_CORE",
        "CONFIG_I2C_DESIGNWARE_PLATFORM",
        "depends_on",
    ) in edges
