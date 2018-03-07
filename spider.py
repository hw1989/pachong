#-*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import sys
import re
from urllib import urlencode
from twisted.enterprise import adbapi
import urllib
import urllib2
import os
import os.path
class ImageSpider(scrapy.spiders.Spider):
    name="imgspider"
    #108.179.235.108
    allowed_domains=['rai-playroom.net',]
    start_urls=["http://www.rai-playroom.net/js/galleries_list.js"]
    path="e:\\yaGimg\\"
    def parse(self,respose):
        matStr=r"insert[\s]*\([\s]*\"[\s]*([a-zA-Z0-9\s]*)\""
        html=respose.body
        patternParams=re.compile(matStr,re.M|re.I)
        findObjParams =patternParams.findall(html)
        for tag in findObjParams:
            scriptUrl="http://www.rai-playroom.net/gallery/"+tag+"/script.js"
            self.mkdir(self.path+tag+"\\")
            yield scrapy.FormRequest(
                url=scriptUrl,
                meta={"tag":tag},
                callback=self.scriptInfo
            )
        print findObjParams

    def scriptInfo(self,response):
        if response.status != 200:
            return
        html=response.body
        tag=response.meta['tag']
        pageStr=r"galleryPage[\s]*=[\s]*([\d]*)[\s]*;"
        formatStr=r"galleryText[\s]*=[\s]*\[(.*)[\s]*\][\s]*;"
        pattern1=re.compile(pageStr,re.M|re.I)
        pattern2=re.compile(formatStr,re.M|re.I)
        findObj1 =pattern1.findall(html)
        findObj2 =pattern2.findall(html)
        pageCount=0
        print "----------------------"
        if findObj1:
            # print pattern1
            pageCount=int(findObj1[0].strip())
        if findObj2:
            print "----------------------"
            print findObj2
        for pageNum in [1,pageCount+1]:
            index=str(pageNum)
            if pageCount<10:
                index="0"+index
            file_path=os.path.join(self.path+tag+"\\",index+".jpg")#拼接这个图片的路径，我是放在F盘的pics文件夹下
            url="http://www.rai-playroom.net/gallery/"+tag+"/"+index+".jpg"
            try:
                res=urllib2.urlopen(url)
                if str(res.status)!='200':
                    continue
                else:
                    with open(file_path,'wb') as f:
                        f.write(res.read())
            except Exception  as ex:
                print url
            # urllib.urlretrieve(url,file_path)#接收文件路径和需要保存的路径，会自动去文件路径下载并保存到我们指定的本地路径
        print "............................"
    def errorBack(self, failure):
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    def mkdir(self,path):
        # 去除首位空格
        path=path.strip()
        # 去除尾部 \ 符号
        path=path.rstrip("\\")
 
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
 
        # 判断结果
        if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
            os.makedirs(path) 
 
            print path+' 创建成功'
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print path+' 目录已存在'
            return False