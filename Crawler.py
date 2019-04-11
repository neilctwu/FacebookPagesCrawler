import requests
import time
from bs4 import BeautifulSoup as bs

class crawler:
    def __init__(self):
        self.itter_count=1000
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                        "Accept-Language":"en-US,en;q=0.5"}

    def html_response(self, url):
        response_state=False
        while response_state is False:
            try:
                response = requests.get(url, headers=self.headers)
                response.encoding = 'utf-8'
                response_state = True
                print('Success crawl {}'.format(url))
            except Exception as e:
                print('Fail with Exception:{}'.format(e))
                time.sleep(3)
            else:
                fanpage_parsed = fanpage_parser(response)
                fanpage_infos = fanpage_parsed.parse_pageinfos()
        return fanpage_infos

    def crawl_urllists(self,data_warehouse):
        n=0
        while n<self.itter_count:
            infos = self.html_response(data_warehouse.relate_urls[n])
            data_warehouse.add_data(infos)
            n += 1



class data_warehouse:
    def __init__(self):
        self.relate_names=[]
        self.relate_urls=[]
        self.page_urls=[]
        self.pages_names=[]
        self.pages_likes=[]
        self.pages_follows=[]

    def add_data(self,infos):
        self.relate_urls += self.remove_duplicate(self.relate_urls, infos['relate_url'])
        self.relate_names += self.remove_duplicate(self.relate_urls, infos['relate_name'])
        self.page_urls += [infos['page_url']]
        self.pages_names += [infos['page_name']]
        self.pages_likes += [infos['page_like']]
        self.pages_follows += [infos['page_follow']]

    @staticmethod
    def remove_duplicate(main,sub):
        [sub.remove(x) for x in main if x in sub]
        return sub



class html_parser:
    def __init__(self, response):
        self._response = response
        self._response.encoding = "utf-8"
        self._parser = bs(self._response.text, "html.parser")



class fanpage_parser(html_parser):
    def __init__(self, response):
        super().__init__(response)

    def parse_pageinfos(self):
        url_list, page_name = self._get_relatedpage()
        fanpage_info={
            'page_name':self._get_name(),
            'page_url':self._get_url(),
            'page_like':self._get_like(),
            'page_follow':self._get_follow(),
            'relate_url':url_list,
            'relate_name':page_name
        }
        return fanpage_info

    def _get_name(self):
        text_name = self._parser.select_one('title#pageTitle').text
        page_name = text_name.split(' - Home | Facebook')[0]
        return page_name

    def _get_url(self):
        return self._response.url

    def _get_like(self):
        soup = self._parser.select("div._4bl9")
        text_like = [meat for meat in soup if 'people like this' in meat.text][0].text
        num_like = int(text_like.split(' people like this')[0].replace(',',''))
        return num_like

    def _get_follow(self):
        soup = self._parser.select("div._4bl9")
        text_follow = [meat for meat in soup if 'people follow this' in meat.text][0].text
        num_follow = int(text_follow.split(' people follow this')[0].replace(',',''))
        return num_follow

    def _get_relatedpage(self):
        soup = self._parser.select("a._4-lu.ellipsis")
        link_infos = [[meat.get('href'), meat.text] for meat in soup]
        url_list = []
        page_name = []
        for x,y in link_infos:
            if x not in url_list:
                url_list.append(x)
                page_name.append(y)
        return url_list,page_name



###

Gocrawl = crawler()
Godata = data_warehouse()

Godata.relate_urls.append('https://www.facebook.com/yellow9395/') #Set initial
Gocrawl.itter_count=50 #Set counts of crawling
Gocrawl.crawl_urllists(Godata)
