import requests
from bs4 import BeautifulSoup#これはクラスの上に書く必要がありました。
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from secret import Secret

class Web_Data_Get:
    BusiCfB = '#listcf_normal01 > table > tr:nth-of-type(2) > td:nth-of-type(4)'#前期営業CF:前期今期ともにプラスのもの(Business CF　Before)
    BusiCfN = '#listcf_normal01 > table > tr:nth-of-type(2) > td:nth-of-type(5)'#今期営業CF
    InveCfB = '#listcf_normal01 > table > tr:nth-of-type(3) > td:nth-of-type(4)'#前期投資CF:投資はマイナスで良い。これがマイナスになってないと会社も拡大しない。(investment)
    InveCfN = '#listcf_normal01 > table > tr:nth-of-type(3) > td:nth-of-type(5)'#今期投資CF
    SaleBb = '#listpl_normal01 > table > tr:nth-of-type(2) > td:nth-of-type(3)'#決算前々期売上高
    SaleB = '#listpl_normal01 > table > tr:nth-of-type(2) > td:nth-of-type(4)'#決算前期売上高
    SaleN = '#listpl_normal01 > table > tr:nth-of-type(2) > td:nth-of-type(5)'#決算売上高(Sale)
    Cash = '#listbs_normal01 > table > tr:nth-of-type(2) > td:nth-of-type(5)'#現金同等物
    seleList_all = [BusiCfB,BusiCfN,InveCfB,InveCfN,SaleBb,SaleB,SaleN,Cash]

    FounY = '#summary01_tab > div > div.tabbox > div:nth-of-type(2) > table > tr:nth-of-type(2) > td'#設立年月日(foundation year)
    ListY = '#summary01_tab > div > div.tabbox > div:nth-of-type(2) > table > tr:nth-of-type(3) > td'#上場年月日(listing year)
    AveAge = '#summary01_tab > div > div.tabbox > div.listsummary > table > tr:nth-of-type(4) > td:nth-of-type(5)'#平均年齢(average age)
    AveInc = '#summary01_tab > div > div.tabbox > div.listsummary > table > tr:nth-of-type(6) > td:nth-of-type(5)'#平均年収(average income)
    seleList_summary = [FounY,ListY,AveAge,AveInc]

    GainB = '#str-main > table.tbl-data-09 > tbody > tr:nth-of-type(1) > td:nth-of-type(4)'#前期営業利益
    GainN = '#str-main > table.tbl-data-09 > tbody > tr:nth-of-type(2) > td:nth-of-type(4)'#今期営業利益
    GainF = '#str-main > table.tbl-data-09 > tbody > tr:nth-of-type(3) > td:nth-of-type(4)'#営業利益会社予想
    SaleF = '#str-main > table.tbl-data-09 > tbody > tr:nth-of-type(3) > td:nth-of-type(2)'#売上高会社予想
    RakuList = [GainB,GainN,GainF,SaleF]

    def __init__(self,SC):
        self.SC = str(SC)

    def all_get(self):#allページからの抽出
        DataList = []
        U = 'http://www.ullet.com/01.html#all'
        MyU = U.replace('01',self.SC)
        r = requests.get(MyU)
        soup = BeautifulSoup(r.content,'lxml')

        for sele in self.seleList_all:
            sele = sele.replace('01',self.SC)
            DL = soup.select(sele)

            try:
                D = DL[0].text
            except IndexError:
                DataList.append('NaN')
            else:
                DataList.append(D)
        return DataList

    def summary_get(self):#summaryページからの抽出
        SummaryList = []
        U = 'http://www.ullet.com/01.html#summary'
        MyU = U.replace('01',self.SC)
        r = requests.get(MyU)
        soup = BeautifulSoup(r.content,'lxml')

        for sele in self.seleList_summary:
            sele = sele.replace('01',self.SC)
            SL = soup.select(sele)

            try:
                S = SL[0].text
            except IndexError:
                SummaryList.append('NaN')
            else:
                SummaryList.append(S)
        return SummaryList

    def all_get2(self):#allページのリスト内包表記Vr.
        U = 'http://www.ullet.com/01.html#all'
        MyU = U.replace('01',self.SC)
        r = requests.get(MyU)
        soup = BeautifulSoup(r.content,'lxml')
        DL = [soup.select(sele.replace('01',self.SC)) for sele in self.seleList_all]
        DataList = [self.try_exce(D) for D in DL]#たぶん入れ子にして一行にできるけど、読みにくいので二行で。それでも充分簡素化した。
        return DataList

    def try_exce(self,DL):#try文は関数じゃないから、内包表記に入れられません。このように関数にして渡す。
        try:
            D = DL[0].text
        except IndexError:
            return 'NaN'
        else:
            return D

    def raku_url_get(self):#楽天。ログインしてアドレス抽出。
        ID , PASS = Secret().Id_Pass()
        MyUrl =('https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html')#('https://www.rakuten-sec.co.jp/')

        driver = webdriver.Chrome()
        driver.get(MyUrl)

        driver.find_element_by_id('form-login-id').send_keys(ID)
        driver.find_element_by_id('form-login-pass').send_keys(PASS)
        driver.find_element_by_id('login-btn').click()

        driver.find_element_by_id('gmenu_domestic_stock').find_element_by_tag_name('a').click()

        driver.find_element_by_id('dscrCdNm2').send_keys('1301')
        driver.find_elements_by_class_name('btn-box')[0].find_elements_by_tag_name('img')[0].click()

        driver.find_elements_by_class_name('nav-tab-01-jp')[0].find_elements_by_tag_name('li')[5].find_elements_by_tag_name('a')[0].click()

        soup = BeautifulSoup(driver.page_source,'html.parser')#'lxml')
        #iframe = soup.find('iframe',id = 'J010101-008-1')
        iframe = soup.select('#J010101-008-1')[0]
        Url = iframe['src']
        return Url
        driver.quit()

    def raku_data(self,DataUrl):#楽天からの抽出
        rkList = []
        DataUrl = DataUrl.replace('01',self.SC)

        HtmlData = requests.get(DataUrl)
        soup2 = BeautifulSoup(HtmlData.content,'lxml')
        for C in self.RakuList:
            CC = soup2.select(C)

            try:
                CC = CC[0].text
            except IndexError:
                rkList.append('NaN')
            else:
                rkList.append(CC)
        return rkList
        driverNeo.quit()
