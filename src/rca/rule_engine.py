from pathlib import Path
 
from src.core.models import (
    Evidence,
    EvidenceType,
    RCAResult,
)
 
 
def analyze_i2c_timeout(
    log_file: Path,
    config_file: Path,
    dts_file: Path,
) -> RCAResult:
    """Analyze an I2C timeout using deterministic rules."""
 
    log_content = log_file.read_text()
    config_content = config_file.read_text()
    dts_content = dts_file.read_text()
 
    evidence = []
    hypotheses = []
    recommendations = []
 
    # ---------------------------------------------------------
    # Rule 1: Detect I2C timeout
    # ---------------------------------------------------------
    if "probe failed with error -110" in log_content:
        evidence.append(
            Evidence(
                evidence_type=EvidenceType.LOG,
                source=str(log_file),
                content=(
                    "I2C driver probe failed with error -110 "
                    "(ETIMEDOUT)."
                ),
            )
        )
 
        hypotheses.append(
            "The I2C controller failed to initialize "
            "within the expected timeout."
        )
 
    # ---------------------------------------------------------
    # Rule 2: Check DesignWare platform driver
    # ---------------------------------------------------------
    if "# CONFIG_I2C_DESIGNWARE_PLATFORM is not set" in config_content:
        evidence.append(
            Evidence(
                evidence_type=EvidenceType.KERNEL_CONFIG,
                source=str(config_file),
                content=(
                    "CONFIG_I2C_DESIGNWARE_PLATFORM "
                    "is not enabled."
                ),
            )
        )
 
        hypotheses.append(
            "The DesignWare I2C platform driver is disabled "
            "in the kernel configuration."
        )
 
        recommendations.append(
            "Verify whether CONFIG_I2C_DESIGNWARE_PLATFORM "
            "should be enabled."
        )
 
    # ---------------------------------------------------------
    # Rule 3: Check Device Tree I2C controller
    # ---------------------------------------------------------
    if "&i2c1" in dts_content and 'status = "okay";' in dts_content:
        evidence.append(
            Evidence(
                evidence_type=EvidenceType.DEVICE_TREE,
                source=str(dts_file),
                content=(
                    "I2C1 is present and enabled in the "
                    "Device Tree."
                ),
            )
        )
 
    # ---------------------------------------------------------
    # Rule 4: Check temperature sensor node
    # ---------------------------------------------------------
    if "temp_sensor@48" in dts_content:
        evidence.append(
            Evidence(
                evidence_type=EvidenceType.DEVICE_TREE,
                source=str(dts_file),
                content=(
                    "Temperature sensor node exists at "
                    "I2C address 0x48."
                ),
            )
        )
 
    # ---------------------------------------------------------
    # Rule 5: Check controller compatible string
    # ---------------------------------------------------------
    if "snps,designware-i2c" not in dts_content:
        evidence.append(
            Evidence(
                evidence_type=EvidenceType.DEVICE_TREE,
                source=str(dts_file),
                content=(
                    "DesignWare I2C compatible string "
                    "was not found in the Device Tree."
                ),
            )
        )
 
        hypotheses.append(
            "The Device Tree compatible string may not correctly"
            "identify the DesignWare I2C controller."
        )
 
        recommendations.append(
            "Verify the I2C controller compatible string "
            "against the SoC binding documentation."
        )
 
    if not evidence:
        return RCAResult(
            summary="No known I2C timeout pattern detected.",
        )
 
    return RCAResult(
        summary="Potential I2C initialization/configuration issue detected.",
        hypotheses=hypotheses,
        evidence=evidence,
        recommendations=recommendations,
        confidence=0.70,
    )

