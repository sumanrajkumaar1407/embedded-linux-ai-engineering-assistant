/*
* Simulated DesignWare I2C platform driver
* Used for the Embedded Linux AI RCA test scenario.
*/
 
#include <linux/platform_device.h>
#include <linux/of.h>
#include <linux/clk.h>
 
static int dw_i2c_probe(struct platform_device *pdev)
{
    struct device *dev = &pdev->dev;
    struct clk *clk;
 
    clk = devm_clk_get(dev, NULL);
 
    if (IS_ERR(clk)) {
        dev_err(dev, "failed to acquire I2C clock\n");
        return PTR_ERR(clk);
    }
 
    dev_info(dev, "I2C controller clock acquired\n");
 
    /*
     * Controller initialization would happen here.
     */
 
    return 0;
}
 
static const struct of_device_id dw_i2c_of_match[] = {
    {
        .compatible = "snps,designware-i2c",
    },
    { }
};
 
static struct platform_driver dw_i2c_driver = {
    .probe = dw_i2c_probe,
    .driver = {
        .name = "designware-i2c",
        .of_match_table = dw_i2c_of_match,
    },
};
 
module_platform_driver(dw_i2c_driver);
 
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Simulated DesignWare I2C platform driver");

