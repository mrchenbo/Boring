import re
import requests


"""
获取基金最近的年化率
"""
def obtain_rate_of_fund(fcode):
    response = requests.get('http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + str(fcode))
    content = str(response.text.encode('utf8'))
    b = re.search(r'(\d+\.\d+?)%', content)
    return float(b.group(1)) / 100


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


FUND_CODE = '000198'
out_price = 280 #黄金卖出价格
charge = 0.001 #黄金卖出手续费
rate = obtain_rate_of_fund(FUND_CODE) #当前货币基金年化率
period = 6 #黄金投资周期（月）

print("基金当前年化率：%f" % rate)
print("当前适合转入金价小于：%f" % suitable_buying_price_of_gold(out_price, charge, rate, period))
