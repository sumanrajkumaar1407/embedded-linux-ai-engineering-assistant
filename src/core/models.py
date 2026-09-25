from dataclasses import dataclass, field
from enum import Enum
from typing import Any
 
 
class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
 
 
class EvidenceType(str, Enum):
    LOG = "log"
    KERNEL_CONFIG = "kernel_config"
    DEVICE_TREE = "device_tree"
    SOURCE_CODE = "source_code"
    CRASH_TRACE = "crash_trace"
    GIT_HISTORY = "git_history"
    HARDWARE = "hardware"
 
 
@dataclass
class Evidence:
    """
    Represents a piece of evidence used during diagnostic analysis.
    """
 
    evidence_type: EvidenceType
    source: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
 
 
@dataclass
class BugReport:
    """
    Represents an Embedded Linux bug reported by an engineer or system.
    """
 
    title: str
    description: str
    severity: Severity = Severity.ERROR
    subsystem: str | None = None
    module: str | None = None
    evidence: list[Evidence] = field(default_factory=list)
 
 
@dataclass
class RCAResult:
    """
    Represents the result of root-cause analysis.
    """
 
    summary: str
    hypotheses: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    confidence: float | None = None

