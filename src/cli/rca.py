from pathlib import Path
 
from src.rca.integrated import build_i2c_integrated_rca
from src.rca.integrated_report import (
    format_integrated_rca_report,
)
 
 
BASE = Path("data/sample/i2c_timeout")
 
 
def main() -> None:
    """Run the integrated RCA for the sample I2C failure."""
 
    log_file = BASE / "logs" / "dmesg.txt"
    config_file = BASE / "kernel" / ".config"
    driver_file = (
        BASE / "kernel" / "i2c_designware_platform.c"
    )
    dts_file = BASE / "devicetree" / "board.dts"
 
    rca = build_i2c_integrated_rca(
        log_file=log_file,
        config_file=config_file,
        driver_file=driver_file,
        dts_file=dts_file,
    )
 
    print(format_integrated_rca_report(rca))
 
 
if __name__ == "__main__":
    main()
