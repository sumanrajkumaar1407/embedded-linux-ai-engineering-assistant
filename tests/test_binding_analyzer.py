from pathlib import Path

from src.diagnostics.binding_analyzer import (
    analyze_binding,
    analyze_i2c1_driver_binding,
)
 
 
def test_matching_binding():
    result = analyze_binding(
        driver_compatible=["snps,designware-i2c"],
        device_tree_compatible="snps,designware-i2c",
    )
 
    assert result.matched is True
    assert (
        result.reason
        == "Driver and Device Tree compatible strings match."
    )
 
 
def test_missing_device_tree_compatible():
    result = analyze_binding(
        driver_compatible=["snps,designware-i2c"],
        device_tree_compatible=None,
    )
 
    assert result.matched is False
    assert (
        result.reason
        == "Device Tree does not define a compatible string "
        "for the controller."
    )

def test_mismatched_device_tree_compatible():
    result = analyze_binding(
        driver_compatible=["snps,designware-i2c"],
        device_tree_compatible="other,i2c-controller",
    )
 
    assert result.matched is False
    assert (
        result.reason
        == "Device Tree compatible string does not match "
        "the driver's supported compatible strings."
    )

def test_analyze_i2c1_driver_binding():
    driver_file = Path(
        "data/sample/i2c_timeout/kernel/"
        "i2c_designware_platform.c"
    )
 
    dts_file = Path(
        "data/sample/i2c_timeout/devicetree/"
        "board.dts"
    )
 
    result = analyze_i2c1_driver_binding(
        driver_file=driver_file,
        dts_file=dts_file,
    )
 
    assert result.matched is False
    assert result.device_tree_compatible is None
    assert result.driver_compatible == [
        "snps,designware-i2c"
    ]
 
    assert (
        result.reason
        == "Device Tree does not define a compatible string "
        "for the controller."
    )
