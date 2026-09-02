import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YelpcrawlerSpider(CrawlSpider):
    name = "yelpcrawler"
    allowed_domains = ["yelp.com"]
    start_urls = ["https://www.yelp.com/search?find_desc=Gyms&find_loc=Berlin%2C+Germany"]

    rules = (Rule(LinkExtractor(allow=r"desc=Gyms.*start="), follow=True),
             Rule(LinkExtractor(allow=r"biz/.*osq=Gyms", deny='hrid'), callback="parse_item", follow=True),
             )

    def parse_item(self, response):
        name = response.css("h1.y-css-eildv6::text").get()
        url = response.url
        a_tag = response.xpath('//p[text()="Business website"]/following-sibling::p[1]/a')
        url_on_web = a_tag.css('::text').get()

        if url_on_web:
            if url_on_web[-1] == '…':
                website_link = a_tag.attrib['href']
            else:
                website_link = url_on_web
        else:
            website_link = 'No info'
        phone = response.xpath('//p[text()="Phone number"]/following-sibling::p[1]/text()').get()
        if not phone:
            phone = 'No info'
        address = response.xpath('//a[text()="Get Directions"]/../following-sibling::p[1]/text()').get()
        if not address:
            address = 'No info'
        yield  {
            'name': name,
            'website_link': website_link,
            'phone': phone,
            'address': address,
            'url': url
        }