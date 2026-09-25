from dataclasses import dataclass, field
from pathlib import Path
import re
 
 
@dataclass
class DeviceTreeNode:
    name: str
    properties: dict[str, str] = field(default_factory=dict)
    children: list["DeviceTreeNode"] = field(default_factory=list)
    parent: str | None = None
 
 
def create_node(
    name: str,
    properties: dict[str, str] | None = None,
    parent: str | None = None,
) -> DeviceTreeNode:
    """Create a Device Tree node."""
 
    return DeviceTreeNode(
        name=name,
        properties=properties or {},
        parent=parent,
    )
 
 
def parse_i2c1_node(dts_file: Path) -> DeviceTreeNode | None:
    """
    Parse the &i2c1 node from a Device Tree source file.
 
    This is intentionally focused on our first I2C diagnostic scenario.
    """
 
    content = dts_file.read_text(encoding="utf-8")
 
    match = re.search(
        r"&i2c1\s*\{(.*?)\n\};",
        content,
        re.DOTALL,
    )
 
    if not match:
        return None
 
    node_content = match.group(1)

    # Remove nested child nodes before parsing properties
    # belonging directly to &i2c1.
    node_content = re.sub(
        r"\w+@[^\s{]+\s*\{.*?\n\s*\};",
        "",
        node_content,
        flags=re.DOTALL,
    )

    properties: dict[str, str] = {}
 
    status = re.search(
        r'status\s*=\s*"([^"]+)"\s*;',
        node_content,
    )
 
    if status:
        properties["status"] = status.group(1)
 
    clock = re.search(
        r"clock-frequency\s*=\s*<([^>]+)>;",
        node_content,
    )
 
    if clock:
        properties["clock-frequency"] = clock.group(1)
 
    compatible = re.search(
        r'compatible\s*=\s*"([^"]+)"\s*;',
        node_content,
    )
 
    if compatible:
        properties["compatible"] = compatible.group(1)
 
    return create_node(
        name="i2c1",
        properties=properties,
    )

def parse_temperature_sensor_node(dts_file: Path,) -> DeviceTreeNode | None:
    """Parse the temp_sensor@48 child node."""

    content = dts_file.read_text(encoding="utf-8")

    match = re.search(
        r"temp_sensor@48\s*\{(.*?)\n\s*\};",
        content,
        re.DOTALL,
    )

    if not match:
        return None

    node_content = match.group(1)

    properties: dict[str, str] = {}

    compatible = re.search(
        r'compatible\s*=\s*"([^"]+)"\s*;',
        node_content,
    )

    if compatible:
        properties["compatible"] = compatible.group(1)

    reg = re.search(
        r"reg\s*=\s*<([^>]+)>;",
        node_content,
    )

    if reg:
        properties["reg"] = reg.group(1)

    status = re.search(
        r'status\s*=\s*"([^"]+)"\s*;',
        node_content,
    )

    if status:
        properties["status"] = status.group(1)

    return create_node(
        name="temp_sensor@48",
        properties=properties,
        parent="i2c1",
    )
