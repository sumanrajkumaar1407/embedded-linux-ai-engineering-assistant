from pathlib import Path
 
from src.rca.report import format_rca_report
from src.rca.rule_engine import analyze_i2c_timeout
 
 
BASE = Path("data/sample/i2c_timeout")
 
 
def main() -> None:
    log_file = BASE / "logs" / "dmesg.txt"
    config_file = BASE / "kernel" / ".config"
    dts_file=BASE / "devicetree" / "board.dts"
 
    result = analyze_i2c_timeout(
        log_file=log_file,
        config_file=config_file,
        dts_file=dts_file,
    )
 
    print(format_rca_report(result))
 
 
if __name__ == "__main__":
    main()
