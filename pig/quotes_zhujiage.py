import scrapy


class QuotesZhuJiaGeSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        'FEED_EXPORT_ENCODING' : 'UTF-8'
    }
    start_urls = [
        'http://www.zhujiage.com.cn/article/201801/879976.html'
    ]

    def parse(self, response):
        for quote in response.css('body div#tbody div#left div#content p[style*=text-align]'):
            yield {
                'item': self.strip(quote.xpath('text()').extract_first())
            }

        next_page = response.css('body div#tbody div#left div.Pagenav a:last-child[href$=".html"]::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow('http://www.zhujiage.com.cn/article/201801/' + next_page, self.parse)
    
    def strip(self, item): 
        return item