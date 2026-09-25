from dataclasses import dataclass, field
 
 
@dataclass
class RCAFinding:
    category: str
    title: str
    evidence: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    confidence: float = 0.0
 
 
@dataclass
class IntegratedRCA:
    summary: str
    findings: list[RCAFinding] = field(default_factory=list)

from pathlib import Path
 
from src.kernel.config_parser import parse_kernel_config
 
 
def detect_i2c_configuration_issue(
    config_file: Path,
) -> RCAFinding | None:
    """Detect a disabled DesignWare I2C platform driver."""
 
    configs = parse_kernel_config(str(config_file))
 
    config_map = {
        config.name: config
        for config in configs
    }
 
    platform_config = config_map.get(
        "CONFIG_I2C_DESIGNWARE_PLATFORM"
    )
 
    if platform_config is None:
        return None
 
    if platform_config.enabled:
        return None
 
    return RCAFinding(
        category="kernel_config",
        title="DesignWare I2C platform driver is disabled",
        evidence=[
            "CONFIG_I2C_DESIGNWARE_PLATFORM is set to 'n'."
        ],
        recommendations=[
            "Verify whether CONFIG_I2C_DESIGNWARE_PLATFORM "
            "should be enabled for this platform."
        ],
        confidence=0.85,
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

def build_i2c_integrated_rca(
    log_file: Path,
    config_file: Path,
    driver_file: Path,
    dts_file: Path,
) -> IntegratedRCA:
    """Build an integrated RCA from logs, Kconfig, driver, and DTS."""
 
    from src.diagnostics.log_analyzer import detect_i2c_timeout
 
    findings: list[RCAFinding] = []
 
    log_finding = detect_i2c_timeout(log_file)
    if log_finding is not None:
        findings.append(log_finding)
 
    config_finding = detect_i2c_configuration_issue(
        config_file
    )
    if config_finding is not None:
        findings.append(config_finding)
 
    binding_finding = detect_i2c_binding_issue(
        driver_file=driver_file,
        dts_file=dts_file,
    )
    if binding_finding is not None:
        findings.append(binding_finding)
 
    if findings:
        summary = (
            "I2C initialization failure detected with "
            "multiple supporting evidence sources."
        )
    else:
        summary = "No known I2C failure pattern detected."
 
    return IntegratedRCA(
        summary=summary,
        findings=findings,
    )
