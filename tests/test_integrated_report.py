from src.rca.integrated import RCAFinding, IntegratedRCA
from src.rca.integrated_report import (
    format_integrated_rca_report,
)
 
 
def test_format_integrated_rca_report():
    rca = IntegratedRCA(
        summary="I2C initialization failure detected.",
        findings=[
            RCAFinding(
                category="kernel_log",
                title="I2C controller initialization timed out",
                evidence=[
                    "I2C driver probe failed with error -110 (ETIMEDOUT)."
                ],
                recommendations=[
                    "Check I2C controller configuration."
                ],
                confidence=0.95,
            )
        ],
    )
 
    report = format_integrated_rca_report(rca)
 
    assert "EMBEDDED LINUX INTEGRATED RCA REPORT" in report
    assert "I2C initialization failure detected." in report
    assert "I2C controller initialization timed out" in report
    assert "ETIMEDOUT" in report
    assert "95%" in report
    assert "Check I2C controller configuration." in report
