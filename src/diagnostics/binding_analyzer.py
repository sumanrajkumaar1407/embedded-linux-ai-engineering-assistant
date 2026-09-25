from dataclasses import dataclass
 
 
@dataclass
class BindingResult:
    driver_compatible: list[str]
    device_tree_compatible: str | None
    matched: bool
    reason: str
 
 
def analyze_binding(
    driver_compatible: list[str],
    device_tree_compatible: str | None,
) -> BindingResult:
    """Compare driver compatible strings with Device Tree."""
 
    if not driver_compatible:
        return BindingResult(
            driver_compatible=[],
            device_tree_compatible=device_tree_compatible,
            matched=False,
            reason="Driver has no Device Tree compatible strings.",
        )
 
    if device_tree_compatible is None:
        return BindingResult(
            driver_compatible=driver_compatible,
            device_tree_compatible=None,
            matched=False,
            reason=(
                "Device Tree does not define a compatible string "
                "for the controller."
            ),
        )
 
    matched = device_tree_compatible in driver_compatible
 
    if matched:
        reason = "Driver and Device Tree compatible strings match."
    else:
        reason = (
            "Device Tree compatible string does not match "
            "the driver's supported compatible strings."
        )
 
    return BindingResult(
        driver_compatible=driver_compatible,
        device_tree_compatible=device_tree_compatible,
        matched=matched,
        reason=reason,
    )

from pathlib import Path
 
from src.devicetree.parser import parse_i2c1_node
from src.kernel.driver_parser import (
    parse_compatible_strings,
)
 
 
def analyze_i2c1_driver_binding(
    driver_file: Path,
    dts_file: Path,
) -> BindingResult:
    """Analyze the DesignWare I2C driver against the I2C1 Device Tree node."""
 
    driver_compatible = parse_compatible_strings(driver_file)
 
    i2c1 = parse_i2c1_node(dts_file)
 
    device_tree_compatible = None
 
    if i2c1 is not None:
        device_tree_compatible = i2c1.properties.get(
            "compatible"
        )
 
    return analyze_binding(
        driver_compatible=driver_compatible,
        device_tree_compatible=device_tree_compatible,
    )
