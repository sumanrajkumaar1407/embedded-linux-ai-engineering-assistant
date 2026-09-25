from pathlib import Path
 
from src.diagnostics.log_analyzer import detect_i2c_timeout
 
 
BASE = Path(
    "data/sample/i2c_timeout/logs/dmesg.txt"
)
 
 
def test_detect_i2c_timeout():
    finding = detect_i2c_timeout(BASE)
 
    assert finding is not None
    assert finding.category == "kernel_log"
 
    assert (
        finding.title
        == "I2C controller initialization timed out"
    )
 
    assert finding.confidence == 0.95
 
    assert any(
        "timeout" in evidence.lower()
        for evidence in finding.evidence
    )
 
    assert any(
        "ETIMEDOUT" in evidence
        for evidence in finding.evidence
    )
