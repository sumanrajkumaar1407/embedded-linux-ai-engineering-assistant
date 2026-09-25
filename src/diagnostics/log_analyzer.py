from pathlib import Path
 
from src.rca.integrated import RCAFinding
 
 
def detect_i2c_timeout(log_file: Path) -> RCAFinding | None:
    """Detect an I2C controller timeout from kernel logs."""
 
    content = log_file.read_text(encoding="utf-8")
 
    timeout_detected = (
        "controller timed out" in content
        or "timeout waiting for bus ready" in content
        or "probe failed with error -110" in content
    )
 
    if not timeout_detected:
        return None
 
    evidence = []
 
    if "controller timed out" in content:
        evidence.append(
            "I2C controller reported a timeout."
        )
 
    if "timeout waiting for bus ready" in content:
        evidence.append(
            "I2C controller timed out waiting for bus ready."
        )
 
    if "probe failed with error -110" in content:
        evidence.append(
            "I2C driver probe failed with error -110 (ETIMEDOUT)."
        )
 
    return RCAFinding(
        category="kernel_log",
        title="I2C controller initialization timed out",
        evidence=evidence,
        recommendations=[
            "Check I2C controller configuration, clock/reset "
            "configuration, Device Tree binding, and bus state."
        ],
        confidence=0.95,
    )
 
