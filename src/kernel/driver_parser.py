from dataclasses import dataclass, field
 
 
@dataclass
class DriverInfo:
    name: str
    source: str
    probe_function: str | None = None
    compatible_strings: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
 
 
def create_driver_info(
    name: str,
    source: str,
) -> DriverInfo:
    """Create an empty driver description."""
 
    return DriverInfo(
        name=name,
        source=source,
    )

from pathlib import Path
import re
 
 
def parse_probe_function(driver_file: Path) -> str | None:
    """Extract the probe function name from a platform driver."""
 
    content = driver_file.read_text(encoding="utf-8")
 
    match = re.search(
        r"static\s+int\s+(\w+_probe)\s*\(",
        content,
    )
 
    if match:
        return match.group(1)
 
    return None

def parse_compatible_strings(driver_file: Path) -> list[str]:
    """Extract Device Tree compatible strings from a driver."""

    content = driver_file.read_text(encoding="utf-8")

    matches = re.findall(
        r'\.compatible\s*=\s*"([^"]+)"',
        content,
    )

    return matches

def parse_driver_dependencies(driver_file: Path) -> list[str]:
    """Detect common framework dependencies used by a driver."""

    content = driver_file.read_text(encoding="utf-8")

    dependencies = []

    if "devm_clk_get" in content or "clk_get" in content:
        dependencies.append("Clock framework")

    if "platform_driver" in content:
        dependencies.append("Platform driver framework")

    if "of_device_id" in content or "of_match_table" in content:
        dependencies.append("Device Tree")

    return dependencies

def analyze_driver(
    driver_file: Path,
    driver_name: str,
) -> DriverInfo:
    """Analyze a kernel driver source file."""

    return DriverInfo(
        name=driver_name,
        source=str(driver_file),
        probe_function=parse_probe_function(driver_file),
        compatible_strings=parse_compatible_strings(driver_file),
        dependencies=parse_driver_dependencies(driver_file),
    )
