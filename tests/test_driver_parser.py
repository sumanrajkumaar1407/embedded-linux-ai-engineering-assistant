from pathlib import Path
 
from src.kernel.driver_parser import (
    analyze_driver,
    parse_compatible_strings,
    parse_driver_dependencies,
    parse_probe_function,
)
 
 
BASE = Path(
    "data/sample/i2c_timeout/kernel/"
    "i2c_designware_platform.c"
)
 
 
def test_parse_probe_function():
    probe = parse_probe_function(BASE)
 
    assert probe == "dw_i2c_probe"
 
 
def test_parse_compatible_strings():
    compatible = parse_compatible_strings(BASE)
 
    assert compatible == ["snps,designware-i2c"]

def test_parse_driver_dependencies():
    dependencies = parse_driver_dependencies(BASE)
 
    assert "Clock framework" in dependencies
    assert "Platform driver framework" in dependencies
    assert "Device Tree" in dependencies

def test_analyze_driver():
    driver = analyze_driver(
        driver_file=BASE,
        driver_name="i2c_designware",
    )
 
    assert driver.name == "i2c_designware"
    assert driver.source.endswith("i2c_designware_platform.c")
    assert driver.probe_function == "dw_i2c_probe"
    assert driver.compatible_strings == ["snps,designware-i2c"]
 
    assert "Clock framework" in driver.dependencies
    assert "Platform driver framework" in driver.dependencies
    assert "Device Tree" in driver.dependencies
