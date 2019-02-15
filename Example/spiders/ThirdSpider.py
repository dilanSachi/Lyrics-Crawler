import scrapy



class ThirdSpider(scrapy.Spider):
    name = "ThirdSpider"
    start_urls = [
        'https://www.lyrics.com//genre/Pop',
    ]

    def parse(self, response):
        for test in response.css('div.sec-lyric'):
            lyric_page_i = "https://www.lyrics.com/" + test.css('p.lyric-meta-title ::attr(href)')[0].get()
            lyric_page_ii = "https://www.lyrics.com/" + test.css('p.lyric-meta-title ::attr(href)')[1].get()

            if lyric_page_i is not None:
                lyric_page_i = response.urljoin(lyric_page_i)
                yield scrapy.Request(lyric_page_i, callback = self.parseLyrics)
            if lyric_page_ii is not None:
                lyric_page_ii = response.urljoin(lyric_page_ii)
                yield scrapy.Request(lyric_page_ii, callback = self.parseLyrics)

        next_index = response.css("div.hidden-xs div.pager ::attr(href)").extract().index(response.css("div.hidden-xs div.pager a.s ::attr(href)")[0].extract()) + 1
        next_page = "https://www.lyrics.com/" + response.css("div.hidden-xs div.pager ::attr(href)")[next_index].get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parseLyrics(self, response):
        song_name = response.css("h1.lyric-title ::text").get()
        artist_name = response.css("h3.lyric-artist a ::text").get()

        file = open("F:\\SE Project\\Scraping\\Example\\Example\\spiders\\Songs\\" + song_name+ "_" + artist_name +".txt", "w")
        lyrics = response.css("pre.lyric-body ::text").extract()
        
        file.write("Song\n")
        file.write(song_name+"\n")
        file.write("Artist\n")
        file.write(artist_name+"\n\n\n")

        for word in lyrics:
            file.write(word)
        file.close()
