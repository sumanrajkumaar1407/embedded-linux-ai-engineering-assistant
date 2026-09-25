from dataclasses import dataclass
 
 
@dataclass
class KernelConfig:
    name: str
    value: str
    enabled: bool
    source: str = ""
 
 
def parse_kernel_config(config_file: str) -> list[KernelConfig]:
    """
    Parse a Linux kernel .config file.
 
    Supported forms:
 
        CONFIG_I2C=y
        CONFIG_I2C=m
        CONFIG_I2C=n
        # CONFIG_I2C_DESIGNWARE_PLATFORM is not set
    """
 
    configs: list[KernelConfig] = []
 
    with open(config_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
 
            if not line:
                continue
 
            # Example:
            # CONFIG_I2C=y
            if line.startswith("CONFIG_") and "=" in line:
                name, value = line.split("=", 1)
 
                configs.append(
                    KernelConfig(
                        name=name,
                        value=value,
                        enabled=value in {"y", "m"},
                        source=config_file,
                    )
                )
 
            # Example:
            # # CONFIG_I2C_DESIGNWARE_PLATFORM is not set
            elif line.startswith("# CONFIG_") and line.endswith(
                "is not set"
            ):
                name = line.split()[1]
 
                configs.append(
                    KernelConfig(
                        name=name,
                        value="n",
                        enabled=False,
                        source=config_file,
                    )
                )
 
    return configs
