from pathlib import Path
 
from src.rca.integrated import (
    RCAFinding,
    build_i2c_integrated_rca,
    detect_i2c_configuration_issue,
    detect_i2c_binding_issue,
)
 
 
BASE = Path(
    "data/sample/i2c_timeout/kernel/.config"
)
 
 
def test_detect_i2c_configuration_issue():
    finding = detect_i2c_configuration_issue(BASE)
 
    assert finding is not None
    assert finding.category == "kernel_config"
 
    assert (
        finding.title
        == "DesignWare I2C platform driver is disabled"
    )
 
    assert finding.confidence == 0.85
 
    assert any(
        "CONFIG_I2C_DESIGNWARE_PLATFORM" in evidence
        for evidence in finding.evidence
    )

from src.diagnostics.binding_analyzer import (
    analyze_i2c1_driver_binding,
)
 
 
def detect_i2c_binding_issue(
    driver_file: Path,
    dts_file: Path,
) -> RCAFinding | None:
    """Detect an I2C driver / Device Tree binding problem."""
 
    result = analyze_i2c1_driver_binding(
        driver_file=driver_file,
        dts_file=dts_file,
    )
 
    if result.matched:
        return None
 
    return RCAFinding(
        category="device_tree_binding",
        title="I2C1 Device Tree binding does not match the driver",
        evidence=[
            result.reason,
            (
                "Driver compatible strings: "
                + ", ".join(result.driver_compatible)
            ),
        ],
        recommendations=[
            "Verify the I2C1 compatible property against "
            "the driver's supported Device Tree bindings."
        ],
        confidence=0.90,
    )

from src.diagnostics.binding_analyzer import (
    analyze_i2c1_driver_binding,
)
 
 
def detect_i2c_binding_issue(
    driver_file: Path,
    dts_file: Path,
) -> RCAFinding | None:
    """Detect an I2C driver / Device Tree binding problem."""
 
    result = analyze_i2c1_driver_binding(
        driver_file=driver_file,
        dts_file=dts_file,
    )
 
    if result.matched:
        return None
 
    return RCAFinding(
        category="device_tree_binding",
        title="I2C1 Device Tree binding does not match the driver",
        evidence=[
            result.reason,
            (
                "Driver compatible strings: "
                + ", ".join(result.driver_compatible)
            ),
        ],
        recommendations=[
            "Verify the I2C1 compatible property against "
            "the driver's supported Device Tree bindings."
        ],
        confidence=0.90,
    )

DRIVER = Path(
    "data/sample/i2c_timeout/kernel/"
    "i2c_designware_platform.c"
)
 
DTS = Path(
    "data/sample/i2c_timeout/devicetree/"
    "board.dts"
)
 
 
def test_detect_i2c_binding_issue():
    finding = detect_i2c_binding_issue(
        driver_file=DRIVER,
        dts_file=DTS,
    )
 
    assert finding is not None
    assert finding.category == "device_tree_binding"
 
    assert (
        finding.title
        == "I2C1 Device Tree binding does not match the driver"
    )
 
    assert finding.confidence == 0.90
 
    assert any(
        "does not define a compatible string" in evidence
        for evidence in finding.evidence
    )
 
    assert any(
        "snps,designware-i2c" in evidence
        for evidence in finding.evidence
    )

def test_build_i2c_integrated_rca():
    log_file = Path(
        "data/sample/i2c_timeout/logs/dmesg.txt"
    )

    config_file = Path(
        "data/sample/i2c_timeout/kernel/.config"
    )

    driver_file = Path(
        "data/sample/i2c_timeout/kernel/"
        "i2c_designware_platform.c"
    )

    dts_file = Path(
        "data/sample/i2c_timeout/devicetree/"
        "board.dts"
    )

    rca = build_i2c_integrated_rca(
        log_file=log_file,
        config_file=config_file,
        driver_file=driver_file,
        dts_file=dts_file,
    )

    assert (
        rca.summary
        == "I2C initialization failure detected with "
        "multiple supporting evidence sources."
    )

    assert len(rca.findings) == 3

    categories = {
        finding.category
        for finding in rca.findings
    }

    assert "kernel_log" in categories
    assert "kernel_config" in categories
    assert "device_tree_binding" in categories

