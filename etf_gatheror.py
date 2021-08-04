import json
import re

import requests
from lxml import etree


def etf_gatheror(etf_codes):
    base_web_url = "http://fund.eastmoney.com/{}.html"
    base_json_url = "http://fundgz.1234567.com.cn/js/{}.js"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "cookie": "HAList=a-sz-300518-%u76DB%u8BAF%u8FBE; em_hq_fls=js; qgqp_b_id=7514820c1e95d8dabb9959ed6472fd31; _adsame_fullscreen_18503=1; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=08-04 19:09:50@#$%u6C47%u6DFB%u5BCC%u79FB%u52A8%u4E92%u8054%u80A1%u7968@%23%24000697; ASP.NET_SessionId=qasotufrbtg4enx2xpohj4g3; st_si=86989931877644; st_pvi=61302411299081; st_sp=2019-08-29%2008%3A37%3A57; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=1; st_psi=20210804190950792-112200305282-2090016094; st_asi=delete"
    }
    unit_net_worth_xpath = "//div[@class='dataOfFund']/dl[@class='dataItem02']/dd[1]/span[1]/text()"
    net_worth_estimation_xpath = "//div[@class='dataOfFund']/dl[@class='dataItem01']/dd[1]/dl[1]/span[1]/text()"
    etf_name_xpath = "//div[@class='fundDetail-tit']/div/text()"
    etf_code_xpath = "//div[@class='fundDetail-tit']/div/span[@class='ui-num']//text()"

    result = [["代码", "名称", "净值估算", "单位净值"]]
    for etf_code in etf_codes:
        etf_code = etf_code.strip()
        r = requests.get(base_web_url.format(etf_code), headers=headers)
        html = etree.HTML(r.content)
        unit_net_worth = html.xpath(unit_net_worth_xpath)[0]
        etf_name = html.xpath(etf_name_xpath)[0]
        etf_code_display = f"'{html.xpath(etf_code_xpath)[0]}'"

        r = requests.get(base_json_url.format(etf_code), headers=headers)
        json_result = re.findall(r"jsonpgz\((.*?)\);", r.content.decode('utf-8'))
        net_worth_estimation = json.loads(json_result[0])["gsz"]

        result.append([etf_code_display, etf_name, net_worth_estimation, unit_net_worth])
    return result


if __name__ == "__main__":
    etf_codes = ['000697', '001725', '001685', '000925', '000696', '001490', '005802', '001726']
    for i in etf_gatheror(etf_codes):
        print(i)
