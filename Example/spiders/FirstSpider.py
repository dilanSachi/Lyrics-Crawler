# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import scrapy

class FirstSpider(scrapy.Spider):
    name = "FirstSpider"
    
    def start_requests(self):
        urls = ['http://stats.espncricinfo.com/ci/engine/records/averages/batting.html?class=1;current=2;id=8;type=team',
                'http://stats.espncricinfo.com/ci/engine/records/averages/batting.html?class=2;current=2;id=8;type=team'
        ]
        
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
            
    def parse(self,response):
        page = response.url.split("?")[-1]
        filename = 'stats-%s.html' % page
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        