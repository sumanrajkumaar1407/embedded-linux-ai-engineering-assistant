from src.rca.integrated import IntegratedRCA
 
 
def format_integrated_rca_report(
    rca: IntegratedRCA,
) -> str:
    """Format an integrated RCA as a human-readable report."""
 
    lines = [
        "=" * 60,
        "EMBEDDED LINUX INTEGRATED RCA REPORT",
        "=" * 60,
        "",
        "Summary:",
        f"  {rca.summary}",
        "",
        "Findings:",
    ]
 
    for index, finding in enumerate(
        rca.findings,
        start=1,
    ):
        lines.extend(
            [
                "",
                f"[{index}] {finding.category}",
                f"    {finding.title}",
                "",
                "    Evidence:",
            ]
        )
 
        for evidence in finding.evidence:
            lines.append(f"      - {evidence}")
 
        if finding.recommendations:
            lines.append("")
            lines.append("    Recommendations:")
 
            for recommendation in finding.recommendations:
                lines.append(
                    f"      - {recommendation}"
                )
 
        lines.append(
            f"    Confidence: {finding.confidence:.0%}"
        )
 
    lines.extend(
        [
            "",
            "=" * 60,
        ]
    )
 
    return "\n".join(lines)

