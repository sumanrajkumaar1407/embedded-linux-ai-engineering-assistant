from pathlib import Path
 
from src.core.dependency import (
    DependencyEdge,
    DependencyGraph,
    DependencyNode,
)
from src.kernel.config_parser import parse_kernel_config
 
 
def build_kconfig_dependency_graph(
    config_file: Path,
) -> DependencyGraph:
    """Build a dependency graph from a Linux kernel .config file."""
 
    configs = parse_kernel_config(str(config_file))
 
    graph = DependencyGraph()
 
    config_map = {
        config.name: config
        for config in configs
    }
 
    # Add every Kconfig option as a node.
    for config in configs:
        graph.add_node(
            DependencyNode(
                name=config.name,
                node_type="kernel_config",
                properties={
                    "value": config.value,
                    "enabled": str(config.enabled),
                },
            )
        )
 
    # Known dependency relationships.
    dependencies = {
        "CONFIG_I2C_DESIGNWARE_CORE": "CONFIG_I2C",
        "CONFIG_I2C_DESIGNWARE_PLATFORM": (
            "CONFIG_I2C_DESIGNWARE_CORE"
        ),
    }
 
    for child, parent in dependencies.items():
        if child not in config_map:
            continue
 
        if parent not in config_map:
            continue
 
        graph.add_edge(
            DependencyEdge(
                source=parent,
                target=child,
                relationship="depends_on",
            )
        )
 
    return graph

def build_i2c_dependency_graph() -> DependencyGraph:
    """Build the original I2C dependency graph for the sample scenario."""
 
    graph = DependencyGraph()
 
    graph.add_node(
        DependencyNode(
            name="CONFIG_I2C",
            node_type="kernel_config",
            properties={"value": "y", "enabled": "True"},
        )
    )
 
    graph.add_node(
        DependencyNode(
            name="CONFIG_I2C_DESIGNWARE_CORE",
            node_type="kernel_config",
            properties={"value": "y", "enabled": "True"},
        )
    )
 
    graph.add_node(
        DependencyNode(
            name="CONFIG_I2C_DESIGNWARE_PLATFORM",
            node_type="kernel_config",
            properties={"value": "n", "enabled": "False"},
        )
    )
 
    graph.add_node(
        DependencyNode(
            name="i2c_designware",
            node_type="driver",
        )
    )
 
    graph.add_node(
        DependencyNode(
            name="i2c1",
            node_type="device_tree",
        )
    )
 
    graph.add_node(
        DependencyNode(
            name="temp_sensor@48",
            node_type="device_tree",
        )
    )
 
    graph.add_edge(
        DependencyEdge(
            source="CONFIG_I2C",
            target="CONFIG_I2C_DESIGNWARE_CORE",
            relationship="enables",
        )
    )
 
    graph.add_edge(
        DependencyEdge(
            source="CONFIG_I2C_DESIGNWARE_PLATFORM",
            target="i2c_designware",
            relationship="builds",
        )
    )
 
    graph.add_edge(
        DependencyEdge(
            source="i2c_designware",
            target="i2c1",
            relationship="binds_to",
        )
    )
 
    graph.add_edge(
        DependencyEdge(
            source="i2c1",
            target="temp_sensor@48",
            relationship="contains",
        )
    )
 
    return graph
