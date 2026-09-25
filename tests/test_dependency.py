from src.rca.dependency_builder import build_i2c_dependency_graph
 
 
def test_i2c_dependency_graph():
    graph = build_i2c_dependency_graph()
 
    assert len(graph.nodes) == 6
    assert len(graph.edges) == 4
 
    assert any(
        edge.relationship == "builds"
        and edge.target == "i2c_designware"
        for edge in graph.edges
    )
 
    assert any(
        edge.relationship == "binds_to"
        and edge.source == "i2c_designware"
        for edge in graph.edges
    )
 
