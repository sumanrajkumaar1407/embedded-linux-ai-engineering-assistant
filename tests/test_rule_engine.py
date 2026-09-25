from pathlib import Path
 
from src.rca.rule_engine import analyze_i2c_timeout
 
 
BASE = Path("data/sample/i2c_timeout")
 
LOG_FILE = BASE / "logs" / "dmesg.txt"
CONFIG_FILE = BASE / "kernel" / ".config"
 
 
def test_i2c_timeout_analysis():
    result = analyze_i2c_timeout(
        log_file=LOG_FILE,
        config_file=CONFIG_FILE,
        dts_file=BASE/"devicetree" / "board.dts",
    )
 
    assert "I2C" in result.summary
    assert len(result.evidence) == 5
 
    assert any(
        "ETIMEDOUT" in evidence.content
        for evidence in result.evidence
    )
 
    assert any(
        "CONFIG_I2C_DESIGNWARE_PLATFORM" in evidence.content
        for evidence in result.evidence
    )

    assert any(
        "I2C1" in evidence.content
        for evidence in result.evidence
    )   

    assert any(
        "0x48" in evidence.content
        for evidence in result.evidence
    )

    assert any(
        "compatible string" in hypothesis
        for hypothesis in result.hypotheses
    )
 
#    assert len(result.recommendations) > 0
