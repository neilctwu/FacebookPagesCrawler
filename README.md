# Facebook粉絲頁爬蟲

####透過Python的Request包, 進行樹狀爬行的粉絲頁爬蟲

 
##使用
```
Gocrawl = crawler()
Godata = data_warehouse()

##設定初始爬行網址
Godata.relate_urls.append ('https://www.facebook.com/yellow9395/')
##設定爬行數量
Gocrawl.itter_count=50 #Set counts of crawling

Gocrawl.crawl_urllists(Godata)
```

##結果
```
Godata.page_urls = **List of 粉絲頁網址**
Godata.pages_names= **List of 粉絲頁名稱**
Godata.pages_likes= **List of 粉絲頁Like數**
Godata.pages_follows= **List of 粉絲頁追蹤數**
## 同一粉絲頁結果記載於同一list index, 
## e.g. X粉絲頁infos={
##   		'網址':Godata.page_urls[n],
##   		'名稱':'X粉絲頁', #('X粉絲頁'==Godata.pages_names[n])
##   		'Like數':Godata.page_likes[n],
##			'追蹤數':Godata.pages_follows[n]
##			}
```
