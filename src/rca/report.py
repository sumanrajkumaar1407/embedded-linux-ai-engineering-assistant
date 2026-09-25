from src.core.models import RCAResult
 
 
def format_rca_report(result: RCAResult) -> str:
    """Convert an RCA result into a human-readable report."""
 
    lines = [
        "=" * 60,
        "EMBEDDED LINUX RCA REPORT",
        "=" * 60,
        "",
        f"Summary:",
        f"  {result.summary}",
        "",
        "Hypotheses:",
    ]
 
    for index, hypothesis in enumerate(result.hypotheses, start=1):
        lines.append(f"  {index}. {hypothesis}")
 
    lines.extend(
        [
            "",
            "Evidence:",
        ]
    )
 
    for evidence in result.evidence:
        lines.append(
            f"  [{evidence.evidence_type.value}] "
            f"{evidence.content}"
        )
 
    lines.extend(
        [
            "",
            "Recommendations:",
        ]
    )
 
    for recommendation in result.recommendations:
        lines.append(f"  - {recommendation}")
 
    if result.confidence is not None:
        lines.extend(
            [
                "",
                f"Confidence: {result.confidence:.0%}",
            ]
        )
 
    lines.append("=" * 60)
 
    return "\n".join(lines)


