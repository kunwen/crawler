#! /usr/bin/env Python 
# -*- coding: UTF-8 -*-


import re
import urlparse
import traceback

from logger import logger

#这是国家级域名后缀字符串，如果有新增加，请按照“后缀-说明"的格式添加
country_domain_names = """ad-Andorra安道尔
ae-United Arab Emirates阿联酋
af-Afghanistan阿富汗
ag-Antigua and Barbuda安提瓜和巴布达
ai-Anguilla安圭拉
al-Albania阿尔巴尼亚
am-Armenia亚美尼亚
an-Netherlands Antilles荷兰属地
ao-Angola安哥拉
aq-Antarctica南极洲
ar-Argentina阿根廷
as-American Samoa东萨摩亚
at-Austria奥地利
au-Australia澳大利亚
aw-Aruba阿鲁巴
az-Azerbaijan阿塞拜疆
ba-Bosnia Herzegovina波黑
bb-Barbados巴巴多斯
bd-Bangladesh孟加拉
be-Belgium比利时
bf-Burkina Faso布基纳法索
bg-Bulgaria保加利亚
bh-Bahrain巴林
bi-Burundi布隆迪
bj-Benin贝宁
bm-Bermuda百慕大
bn-Brunei Darussalam文莱
bo-Bolivia玻利维亚
br-Brazil巴西
bs-Bahamas巴哈马
bt-Bhutan不丹
bv-Bouvet Island布韦岛
bw-Botswana伯兹瓦纳
by-Belarus白俄罗斯
bz-Belize伯利兹
ca-Canada加拿大
cc-Cocos Islands科科斯群岛
cf-Central African Republic中非
cg-Congo刚果
ch-Switzerland瑞士
ci-Ivory Coast象牙海岸
ck-Cook Islands库克群岛
cl-Chile智利
cm-Cameroon喀麦隆
cn-China中国
co-Colombia哥伦比亚
cq-Equatorial Guinea赤道几内亚
cr-Costa Rica哥斯达黎加
cu-Cuba古巴
cv-Cape Verde佛得角
cx-Christmas Island圣诞岛(英属)
cy-Cyprus塞浦路斯
cz-Czech Republic捷克
de-Germany德国
dj-Djibouti吉布提
dk-Denmark丹麦
dm-Dominica多米尼加联邦
do-Dominican Republic多米尼加
dz-Algeria阿尔及利亚
ec-Ecuador厄瓜多尔
ee-Estonia爱沙尼亚
eg-Egypt埃及
eh-Western Sahara西萨摩亚
es-Spain西班牙
et-Ethiopia埃塞俄比亚
ev-El Salvador萨尔瓦多
fi-Finland芬兰
fj-Fiji斐济
fk-Falkland Islands福克兰群岛
fm-Micronesia密克罗尼西亚
fo-Faroe Islands法罗群岛
fr-France法国
ga-Gabon加蓬
gb-Great Britain (UK)大不列颠联合王国
gd-Grenada格林纳达
ge-Georgia格鲁吉亚
gf-French Guiana法属圭亚那
gh-Ghana加纳
gi-Gibraltar直布罗陀
gl-Greenland格陵兰群岛
gm-Gambia冈比亚
gn-Guinea几内亚
gp-Guadeloupe瓜德罗普岛(法属)
gr-Greece希腊
gt-Guatemala危地马拉
gu-Guam关岛
gw-Guinea-Bissau几内亚比绍
gy-Guyana圭亚那
hk-Hong Kong香港
hm-Heard 赫德与麦克唐纳群岛
hn-Honduras洪都拉斯
hr-Croatia克罗地亚
ht-Haiti海地
hu-Hungary匈牙利
id-Indonesia印度尼西亚
ie-Ireland爱尔兰
il-Israel以色列
in-India印度
io-British Indian Ocean Territory英属印度洋领地
iq-Iraq伊拉克
ir-Iran伊朗
is-Iceland冰岛
it-Italy意大利
jm-Jamaica牙买加
jo-Jordan约旦
jp-Japan日本
ke-Kenya肯尼亚
kg-Kyrgyz Stan吉尔吉斯斯坦
kh-Cambodia柬埔塞
ki-Kiribati基里巴斯
km-Comoros科摩罗
kn-St. Kitts 圣基茨和尼维斯
kp-Korea-North朝鲜
kr-Korea-South韩国
kw-Kuwait科威特
ky-Cayman Islands开曼群岛(英属)
kz-Kazakhstan哈萨克斯坦
la-Lao People's Republic老挝
lb-Lebanon黎巴嫩
lc-St. Lucia圣露西亚岛
li-Liechtenstein列支敦士登
lk-Sri Lanka斯里兰卡
lr-Liberia利比里亚
ls-Lesotho莱索托
lt-Lithuania立陶宛
lu-Luxembourg卢森堡
lv-Latvia拉脱维亚
ly-Libya利比亚
ma-Morocco摩洛哥
mc-Monaco摩纳哥
md-Moldova摩尔多瓦
mg-Madagascar马达加斯加
mh-Marshall Islands马绍尔群岛
ml-Mali马里
mm-Myanmar缅甸
mn-Mongolia蒙古
mo-Macao澳门
mp-Northern Mariana Islands北马里亚纳群岛
mq-Martinique马提尼克岛(法属)
mr-Mauritania毛里塔尼亚
ms-Montserrat蒙塞拉特岛
mt-Malta马尔他
mv-Maldives马尔代夫
mw-Malawi马拉维
mx-Mexico墨西哥
my-Malaysia马来西亚
mz-Mozambique莫桑比克
na-Namibia纳米比亚
nc-New Caledonia新喀里多尼亚
ne-Niger尼日尔
nf-Norfolk Island诺福克岛
ng-Nigeria尼日利亚
ni-Nicaragua尼加拉瓜
nl-Netherlands荷兰
no-Norway挪威
np-Nepal尼泊尔
nr-Nauru瑙鲁
nt-Neutral Zone中立区
nu-Niue纽埃
nz-New Zealand新西兰
om-Oman阿曼
pa-Panama巴拿马
pe-Peru秘鲁
pf-French Polynesia法属玻利尼西亚
pg-Papua New Guinea巴布亚新几内亚
ph-Philippines菲律宾
pk-Pakistan巴基斯坦
pl-Poland波兰
pm-St. Pierre 圣皮埃尔和密克隆群岛
pn-Pitcairn Island皮特克恩岛
pr-Puerto Rico波多黎各
pt-Portugal葡萄牙
pw-Palau帕劳
py-Paraguay巴拉圭
qa-Qatar卡塔尔
re-Reunion Island留尼汪岛(法属)
ro-Romania罗马尼亚
ru-Russian Federation俄罗斯
rw-Rwanda卢旺达
sa-Saudi Arabia沙特阿拉伯
sb-Solomon Islands所罗门群岛
sc-Seychelles塞舌尔
sd-Sudan苏旦
se-Sweden瑞典
sg-Singapore新加坡
sh-St. Helena海伦娜
si-Slovenia斯洛文尼亚
sj-Svalbard 斯瓦尔巴特和扬马延岛
sk-Slovakia斯洛伐克
sl-Sierra Leone塞拉利昂
sm-San Marino圣马力诺
sn-Senegal塞内加尔
so-Somalia索马里
sr-Suriname苏里南
st-Sao Tome 圣多美和普林西比
su-USSR苏联
sy-Syrian Arab Republic叙利亚
sz-Swaziland斯威士兰
tc-Turks 特克斯和凯科斯群岛
td-Chad乍得
tf-French Southern Territories法属南半球领地
tg-Togo多哥
th-Thailand泰国
tj-Tajikistan塔吉克斯坦
tk-Tokelau托克劳群岛
tm-Turkmenistan土库曼斯坦
tn-Tunisia突尼斯
to-Tonga汤加
tp-East Timor东帝汶
tr-Turkey土耳其
tt-Trinidad 特立尼达和多巴哥
tv-Tuvalu图瓦鲁
tw-Taiwan台湾
tz-Tanzania坦桑尼亚
ua-Ukrainian SSR 乌克兰
ug-Uganda乌干达
uk-United Kingdom英国
us-United States美国
uy-Uruguay乌拉圭
va-Vatican City State梵地冈
vc-St.Vincent 圣文森特和格林纳丁斯
ve-Venezuela委内瑞拉
vg-Virgin Islands维京群岛
vn-Vietnam越南
vu-Vanuatu瓦努阿图
wf-Wallis 瓦利斯和富图钠群岛
ws-Samoa西萨摩亚
ye-Yemen也门
yu-Yugoslavia南斯拉夫
za-South Africa南非
zm-Zambia赞比亚
zr-Zaire扎伊尔
zw-Zimbabwe津巴布韦"""

#这是国际级域名后缀字符串，如果有新增加，请按照“后缀-说明"的格式添加
international_domain_names = """.com-商业机构,任何人都可以注册
.edu-教育机构
.gov-政府部门
.int-国际组织
.mil-美国军事部门
.net-网络组织,例如因特网服务商和维修商,现在任何人都可以注册
.org-非盈利组织,任何人都可以注册
.biz-商业
.co-日本商业
.ac-日本商业
.naver-日本商业
.me-日本商业
.ne-日本商业
.mobi-日本商业
.info-网络信息服务组织
.pro-用于会计、律师和医生
.name-用于个人
.museum-用于博物馆
.coop-用于商业合作团体
.aero-用于航空工业
.xxx-用于成人、色情网站
.idv-用于个人"""

class SLD(object):
    """
            该方法的准确与否取决于顶级域名后缀库的完善性，目前只添加了国际级域名后缀和国家级域名后缀
    """
    def __init__(self):
        #url格式校验的正则表达式
        self.url_regex = r"^(http://|https://){0,1}[A-Za-z0-9][A-Za-z0-9\-\.]+[A-Za-z0-9]\.[A-Za-z]{2,}[\43-\176]*$"
        #顶级域名后缀字典
        self.top_domain_suffix = self.get_top_domain_suffix()


    def get_top_domain_suffix(self):
        "获取顶级域名后缀"
        "将国家域名后缀、国际域名后缀以及两者的结合生成一个字典，{'.com.cn':None, '.cn':None}这种格式，这种格式可以提高查询速度"
        k_1 = map(lambda s:".%s"%s.split("-")[0], country_domain_names.split("\n"))
        k_2 = map(lambda s:s.split("-")[0], international_domain_names.split("\n"))
        mem_dict = {}.fromkeys(["%s%s"%(k2,k1) for k2 in k_2 for k1 in k_1])
        mem_dict.update({}.fromkeys(k_1))
        mem_dict.update({}.fromkeys(k_2))
        return mem_dict

    def get_host(self, url):
        "获取url的host"
        host = ""
        if re.match(self.url_regex, url):
            if url.startswith("http"):
                host_port = urlparse.urlparse(url)[1]
                host = host_port.split(":")[0]
            elif "/" in url:
                host = url[:url.find("/")].split(":")[0]
            else:
                host = url
        else:
            logger.warning( "[%s] not a url" %url)
            pass
        return host
           
    def get_l_s_r(self, c, h):
        "返回字符串h中字符c的位置l,c右边的部分s,左边的部分r"
        l = h.rindex(c)
        s = h[l:]
        r = h[:l]
        return l,s,r
    

    #传入参数url，返回一级域名，返回空表示url不规范    

    def get_second_level_domain(self, url):

        try:
            second_level_domain = ""
            host = self.get_host(url)
            dot_num = host.count(".")
            #根据host中的点"."去判断host中顶级域名的结构
            if dot_num >= 2:
                dot_1,suffix_1,remainder_1 = self.get_l_s_r(".", host)
                dot_2,suffix_2,remainder_2 = self.get_l_s_r(".", remainder_1)
                #对国家与国际结合的域名后缀进行判断
                if self.top_domain_suffix.has_key(suffix_2):
                    dot_3 = remainder_2.rindex(".")
                    second_level_domain = host[dot_3+1:]
                #对国家或国际域名后缀进行判断
                elif self.top_domain_suffix.has_key(suffix_1):
                    second_level_domain = host[dot_2+1:]
                else:
                    logger.warning( "['%s'] get top domain error!" %host)
                    pass
               
            else:
                dot_1,suffix_1,remainder_1 = self.get_l_s_r(".", host)
                #只能是国家或国际域名后缀，进行判断
                if self.top_domain_suffix.has_key(suffix_1):
                    second_level_domain = host
                else:
                    logger.warning( "['%s'] get top domain error!" %host)
                    pass
            return second_level_domain
        
        except Exception, err:
            logger.warning('获取一级域名时报错的原因：%s' % err)
            pass
            # traceback.print_exc()
   

#这下面是测试代码
if __name__ == '__main__':
    a = SLD()
    for u in ["https://www.sina.com.cn:80/news/1/index.html", "https://www.jd.com.cn:80", "https://www.sina.com/","www.baidu.com.cn/news/1/index.html", "news.aodun.com.cn/1/a.html", "aodun.com", "d.adf.jf.cn", "adf.adfkj","a.news.aodun.com.cn:80/1/a.html", "med-music.com.ua"]:
        print a.get_second_level_domain(u)
