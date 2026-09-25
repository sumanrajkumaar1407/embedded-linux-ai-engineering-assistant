from src.core.models import (
    BugReport,
    Evidence,
    EvidenceType,
    Severity,
)
 
 
def test_bug_report_creation():
    evidence = Evidence(
        evidence_type=EvidenceType.LOG,
        source="dmesg",
        content="i2c_designware 12340000.i2c: controller timed out",
    )
 
    bug = BugReport(
        title="I2C controller timeout",
        description="Temperature sensor is not detected",
        severity=Severity.ERROR,
        subsystem="I2C",
        module="i2c_designware",
        evidence=[evidence],
    )
 
    assert bug.title == "I2C controller timeout"
    assert bug.subsystem == "I2C"
    assert bug.module == "i2c_designware"
    assert len(bug.evidence) == 1
