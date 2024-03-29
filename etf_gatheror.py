import json
import re

import requests
from lxml import etree


def etf_gatheror(etf_codes):
    base_web_url = "http://fund.eastmoney.com/{}.html"
    base_json_url = "http://fundgz.1234567.com.cn/js/{}.js"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "cookie": "HAList=a-sz-300518-%u76DB%u8BAF%u8FBE; em_hq_fls=js; qgqp_b_id=7514820c1e95d8dabb9959ed6472fd31; _adsame_fullscreen_18503=1; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=08-04 19:09:50@#$%u6C47%u6DFB%u5BCC%u79FB%u52A8%u4E92%u8054%u80A1%u7968@%23%24000697; ASP.NET_SessionId=qasotufrbtg4enx2xpohj4g3; st_si=86989931877644; st_pvi=61302411299081; st_sp=2019-08-29%2008%3A37%3A57; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=1; st_psi=20210804190950792-112200305282-2090016094; st_asi=delete",
    }
    unit_net_worth_xpath = "//div[@class='dataOfFund']/dl[@class='dataItem01']/dd[@class='dataNums']/span[1]/text()"
    net_worth_date_xpath = "//div[@class='dataOfFund']/dl[@class='dataItem01']/dt/p/text()"
    etf_name_xpath = "//div[@class='fundDetail-tit']/div/text()"
    etf_code_xpath = "//div[@class='fundDetail-tit']/div/span[@class='ui-num']//text()"
    fund_size_and_date_xpath = "//div[@class='infoOfFund']//tr[1]/td[2]/text()"

    result = [["代码", "名称", "净值估算", "估算时间", "单位净值", "净值日期", "规模", "规模日期"]]
    for etf_code in etf_codes:
        etf_code = etf_code.strip()
        r = requests.get(base_web_url.format(etf_code), headers=headers)
        html = etree.HTML(r.content)  # type:ignore
        etf_name = html.xpath(etf_name_xpath)[0]
        etf_code_display = f"'{html.xpath(etf_code_xpath)[0]}'"
        unit_net_worth = html.xpath(unit_net_worth_xpath)[0]
        net_worth_date = (html.xpath(net_worth_date_xpath)[0]).replace(")", "")
        fund_size_and_date = html.xpath(fund_size_and_date_xpath)[0]
        fund_size_and_date = re.findall(r"([\d\.]+)亿?元（([\d\-]+)）", fund_size_and_date)
        fund_size = fund_size_and_date[0][0]
        fund_size_date = fund_size_and_date[0][1]

        r = requests.get(base_json_url.format(etf_code), headers=headers)
        json_result = re.findall(r"jsonpgz\((.*?)\);", r.content.decode("utf-8"))
        json_data = json.loads(json_result[0])
        net_worth_estimation = json_data["gsz"]
        estimated_time = json_data["gztime"]

        # etf_code_display      代码
        # etf_name              名称
        # net_worth_estimation  净值估算
        # estimated_time        估算时间
        # unit_net_worth        单位净值
        # net_worth_date        净值日期
        # fund_size             规模
        # fund_size_date        规模日期
        result.append(
            [etf_code_display, etf_name, net_worth_estimation, estimated_time, unit_net_worth, net_worth_date, fund_size, fund_size_date]
        )
    return result


if __name__ == "__main__":
    etf_codes = ["000697", "001725", "001685", "000925", "000696", "001490", "005802", "001726"]
    for i in etf_gatheror(etf_codes):
        print(i)
