from src.core.dependency import (
    DependencyEdge,
    DependencyGraph,
    DependencyNode,
)
 
 
def build_i2c_dependency_graph() -> DependencyGraph:
    graph = DependencyGraph()
 
    graph.add_node(
        DependencyNode(
            name="CONFIG_I2C",
            node_type="kconfig",
        )
    )
 
    graph.add_node(
        DependencyNode(
            name="CONFIG_I2C_DESIGNWARE_CORE",
            node_type="kconfig",
        )
    )
 
    graph.add_node(
        DependencyNode(
            name="CONFIG_I2C_DESIGNWARE_PLATFORM",
            node_type="kconfig",
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
            node_type="device",
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
