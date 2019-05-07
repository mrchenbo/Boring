"""
计算当前货币基金是否适宜转入黄金

参数：
sell_price:黄金卖出价格
sell_charge:黄金卖出手续费
fund_rate:当前货币基金年化率
invest_period:黄金投资周期（月）

返回值：
适宜转入的黄金买入价格
"""
def suitable_buying_price_of_gold(sell_price, sell_charge, fund_rate, invest_period):
    return (out_price * (1 - sell_charge)) / (1 + fund_rate * invest_period / 12)

out_price = 280 #黄金卖出价格
charge = 0.001 #黄金卖出手续费
rate = 0.02316 #当前货币基金年化率
period = 6 #黄金投资周期（月）

print(suitable_buying_price_of_gold(out_price, charge, rate, period))