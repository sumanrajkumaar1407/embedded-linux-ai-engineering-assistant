from src.kernel.config_parser import parse_kernel_config
 
 
BASE = "data/sample/i2c_timeout/kernel/.config"
 
 
def test_parse_kernel_config():
    configs = parse_kernel_config(BASE)
 
    config_map = {config.name: config for config in configs}
 
    assert config_map["CONFIG_I2C"].value == "y"
    assert config_map["CONFIG_I2C"].enabled is True
 
    assert config_map["CONFIG_I2C_DESIGNWARE_CORE"].value == "y"
    assert config_map["CONFIG_I2C_DESIGNWARE_CORE"].enabled is True
 
    assert config_map["CONFIG_I2C_DESIGNWARE_PLATFORM"].value == "n"
    assert config_map["CONFIG_I2C_DESIGNWARE_PLATFORM"].enabled is False
