from pathlib import Path
 
from src.devicetree.parser import (
    parse_i2c1_node,
    parse_temperature_sensor_node,
)
 
 
BASE = Path("data/sample/i2c_timeout/devicetree/board.dts")
 
 
def test_parse_i2c1_node():
    node = parse_i2c1_node(BASE)
 
    assert node is not None
    assert node.name == "i2c1"
 
    assert node.properties["status"] == "okay"
    assert node.properties["clock-frequency"] == "400000"
 
    assert "compatible" not in node.properties
 
 
def test_parse_temperature_sensor_node():
    node = parse_temperature_sensor_node(BASE)
 
    assert node is not None
    assert node.name == "temp_sensor@48"
    assert node.parent == "i2c1"
 
    assert node.properties["compatible"] == "demo,temp-sensor"
    assert node.properties["reg"] == "0x48"
    assert node.properties["status"] == "okay"
