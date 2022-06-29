# import scrapy


# class EbaySpiderSpider(scrapy.Spider):
#     name = 'ebay_spider'
#     allowed_domains = ['example.com']
#     start_urls = ['http://example.com/']

#     def parse(self, response):
#         pass


from scrapy.crawler import CrawlerProcess
import scrapy
import json
from scrapy.http import FormRequest
from scrapy.http.headers import Headers
from urllib.parse import urlencode
from scrapy import Request
from scrapy.http.cookies import CookieJar
from scrapy.shell import inspect_response
# from urlparse import urlparse, parse_qs
from urllib.parse import urlparse, parse_qs
import math

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class BlogSpider(scrapy.Spider):
    COOKIES_ENABLED = True
    COOKIES_DEBUG = False
    name = 'ebay_spider'
    # start_urls = ['http://www.ebay.com/sch/Cars-Trucks/6001/i.html']
    start_urls = [
        'http://www.ebay.com/sch/Cars-Trucks/6001/i.html?_dcat=6001&_dmpt=US_Cars_Trucks&Model%2520Year=1901%7C1902%7C1903%7C1904%7C1905%7C1906%7C1907%7C1908%7C1909%7C1910%7C1911%7C1912%7C1913%7C1914%7C1915%7C1916%7C1917%7C1918%7C1919%7C1920%7C1921%7C1922%7C1923%7C1924%7C1925%7C1926%7C1927%7C1928%7C1929%7C1930%7C1931%7C1932%7C1933%7C1934%7C1935%7C1936%7C1937%7C1938%7C1939%7C1940%7C1941%7C1942%7C1943%7C1944%7C1945%7C1946%7C1947%7C1948%7C1949%7C1950%7C1951%7C1952%7C1953%7C1954%7C1955%7C1956%7C1957%7C1958%7C1959%7C1960%7C1961%7C1962%7C1963%7C1964%7C1965%7C1966%7C1967%7C1968%7C1969%7C1970%7C1971%7C1972%7C1973%7C1974%7C1975%7C1976%7C1977%7C1978%7C1979%7C1980%7C1981%7C1982%7C1983%7C1984%7C1985%7C1986%7C1987']

    def __init__(self, brand=None, model=None, start_year=None, end_year=None, start_price=None, end_price=None,
                 mileage=None, interior=None, exterior=None, page_number=None, *args, **kwargs):

        f = open("./ebay_params.txt", "w")
        qs = "brand={brand}, model={model}, start_year={start_year}, end_year={end_year}, " \
             "start_price={start_price}, end_price={end_price}, mileage={mileage}, " \
             "interior={interior}, exterior={exterior}, page_number={page_number}" \
            .format(brand=brand, model=model, start_year=start_year, end_year=end_year,
                    start_price=start_price, end_price=end_price, mileage=mileage,
                    interior=interior, exterior=exterior, page_number=page_number)

        self.f = open("./ebay_debugger.txt", "a")
        super(BlogSpider, self).__init__(*args, **kwargs)
        year = ""
        try:
            if start_year and end_year:
                for i in range(int(start_year), int(end_year) + 1, 1):
                    if i == int(end_year):
                        year = year + str(i)
                    else:
                        year = year + str(i) + '%7C'
            elif start_year and not end_year:
                year = start_year
            elif end_year and not start_year:
                year = end_year
            self.f.write('Start.')
            if mileage:
                mileage = mileage.replace(',', '%252C')
                # url= 'http://www.ebay.com/sch/Cars-Trucks/6001/i.html?rt=nc&LH_BIN=1&_dcat=6001&_dmpt=US_Cars_Trucks&makeval='+brand+'&modelval='+model+'&_nkw='+brand+' '+model+'&Model%2520Year='+year+'&rt=nc&_mPrRngCbx=1&_udlo='+start_price+'&_udhi='+end_price+'&Vehicle%2520Mileage=Less%2520than%2520'+mileage+'%2520miles'+'&Exterior%2520Color='+exterior+'&Interior%2520Color='+interior+'&_pgn='+page_number+'&_ipg=50'
            url = 'http://www.ebay.com/sch/Cars-Trucks/6001/i.html?_dcat=6001&_dmpt=US_Cars_Trucks&makeval=' + brand + '&modelval=' + model + '&_nkw=' + brand + ' ' + model + '&Model%2520Year=' + year + '&rt=nc&_mPrRngCbx=1&_udlo=' + start_price + '&_udhi=' + end_price + '&Vehicle%2520Mileage=Less%2520than%2520' + mileage + '%2520miles' + '&Exterior%2520Color=' + exterior + '&Interior%2520Color=' + interior + '&_pgn=' + page_number + '&_ipg=50'

            # url = 'https://www.ebay.com/sch/Cars-Trucks/6001/i.html?_dcat=6001&_dmpt=US_Cars_Trucks&' \
            #       'makeval={make}&_fosrp=1'.format(make=brand)


            # self.start_urls = ['http://www.example.com/categories/%s' % category]
            f.write("%s \n %s" % (qs, url))
            self.start_urls = [url]
        except Exception as e:
            f = open("./ebay_exception1.txt", "w")
            f.write(str(e))

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)

    def errback_httpbin(self, failure):
        f = open("./ebay_httpfail.txt", "w")
        # f.write(repr(failure))
        output = "URL: {url} \n failure: {failure}".format(url=self.start_urls[0], failure=repr(failure))

        if failure.check(HttpError):
            output += 'HttpError occurred'

        elif failure.check(DNSLookupError):
            output += 'DNSLookupError occurred'

        elif failure.check(TimeoutError, TCPTimedOutError):
            output += 'TimeoutError occurred'
        output += "\n statusCode: {status}".format(status=failure.value.response.status )
        f.write(output)

    def parse(self, response):
        try:
            global total_results
            global page_count
            self.f.write('Step 1')
            #	inspect_response(response,self)
            self.f.write(response.body)
            #self.f.write(response.__dict__)
            if response.css('span.listingscnt ::text'):
                self.f.write('Step 2')
                total_results = response.css('span.listingscnt ::text').extract_first()
                total_results = total_results.replace(",", "")
                total_results = total_results.replace("listings", "")
                total_results = total_results.strip()
                pages = float(total_results) / 50
                page_count = math.ceil(pages)
                self.logger.warning(total_results + " resultats")
            elif response.css('span.rcnt ::text'):
                self.f.write('Step 3')
                total_results = response.css('span.rcnt ::text').extract_first()
                total_results = total_results.replace(",", "")
                total_results = total_results.replace("listings", "")
                total_results = total_results.strip()
                pages = float(total_results) / 50
                page_count = math.ceil(pages)
                self.logger.warning(total_results + " resultats")
            elif response.css('h1.srp-controls__count-heading ::text'):
                self.f.write('Step 4')
                total_results = response.css('h1.srp-controls__count-heading ::text').extract_first()
                total_results = total_results.replace(",", "")
                total_results = total_results.replace(" results", "")
                total_results = total_results.strip()
                pages = float(total_results) / 50
                page_count = math.ceil(pages)
                self.logger.warning(total_results + " resultats")

            else:
                self.f.write('Step 5')
                self.logger.warning("absence de span.listingscnt et span.rcnt")
                total_results = ''
                page_count = ''

            for res in response.css('li.sresult.lvresult.clearfix.li'):
                if res.css('ul.lvprices li:nth-child(2).lvformat span ::text'):
                    bids = res.css('ul.lvprices li:nth-child(2).lvformat span ::text').extract_first()
                    bids = bids.split(" ")
                else:
                    bids = []
                if res.css('ul div.tsp'):
                    best = res.css('ul div.tsp + li + li span ::text').extract_first()
                    best = best.strip()
                    if best == "Buy It Now":
                        scrap = True
                else:
                    scrap = False
                if len(bids) > 1:
                    if bids[1] == "bids" or bids[1] == "bid" and scrap == False:
                        pass
                    else:
                        href = res.css('div div a::attr(href)').extract_first()
                        yield scrapy.Request(response.urljoin(href), callback=self.product_details)
                else:
                    href = res.css('div div a::attr(href)').extract_first()
                    yield scrapy.Request(response.urljoin(href), callback=self.product_details)
            next_page = response.css('tr td.pages a.curr + a ::attr(href)').extract_first()
            self.f.write('Step 6')
        except Exception as e:
            f = open("./ebay_exception.txt", "w")
            f.write(str(e))
    # if next_page:
    # yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def product_details(self, response):
        try:
            title = response.css('.it-ttl ::text').extract()
            self.f.write('Step 7')
            title = title[1]
            if title:
                str_title = title.split(" ")
            else:
                str_title = "       "
            brand = str_title[1]
            if len(str_title) > 2:
                model = str_title[2]
            else:
                model = " "
            price = response.css('div#vi-mskumap-none span ::text').extract_first()
            price = price.replace("US $", "")
            price = price.replace(",", "")
            src = []
            if response.css('div#vi_main_img_fs ul.lst.icon li'):
                for res in response.css('ul.lst.icon li'):
                    img = res.css('td.tdThumb div img::attr(src)').extract_first()
                    img = img.replace("64.", "500.")
                    src.append(img)
            else:
                img = response.css('div#mainImgHldr img:nth-child(2)::attr(src)').extract_first()
                src.append(img)

            specs = {}
            for res in response.css('div.itemAttr div table tr'):

                key = res.css('td:nth-child(1) ::text').extract_first()
                if res.css('td:nth-child(2) h2'):
                    value = res.css('td:nth-child(2) h2 ::text').extract_first()
                else:
                    value = res.css('td:nth-child(2) span ::text').extract_first()

                value = res.css('td:nth-child(2) span ::text').extract_first()
                key1 = res.css('td:nth-child(3) ::text').extract_first()
                if res.css('td:nth-child(4) h2'):
                    value1 = res.css('td:nth-child(4) h2 ::text').extract_first()
                else:
                    value1 = res.css('td:nth-child(4) span ::text').extract_first()
                # value1=res.css('td:nth-child(4) span ::text').extract_first()
                if value is not None:
                    value = value.strip()
                if key is not None:
                    key = key.replace(":", "")
                    key = key.strip()

                if value1 is not None:
                    value1 = value1.strip()
                if key1 is not None:
                    key1 = key1.replace(":", "")
                    key1 = key1.strip()
                if key == "Model":
                    if value is None:
                        value = res.css('td:nth-child(2) h2 ::text').extract_first()

                if key is not None:
                    specs[key] = value
                if key1 is not None:
                    specs[key1] = value1
                if key == "Year":
                    year = value
                if key1 == "Year":
                    year = value1
                if key == "Mileage":
                    mileage = value
                if key1 == "Mileage":
                    mileage = value1
            mileage = mileage.replace(",", "")
            mileage = mileage.strip()
            if mileage:
                miles = float(mileage)
                conv_fac = 1.609
                kilometers = miles * conv_fac
            else:
                kilometers = ""
            parameters = parse_qs(urlparse(response.url).query)
            try:
                reference_id = parameters['item']
                reference_id = reference_id[0]
            except Exception as e:
                parames = response.url.split("/")
                ref_param = parames[len(parames) - 1]
                reference_id = ref_param.split('?')
                reference_id = reference_id[0]
            # if not total_resultes:
            #   total_resultes=''
            # yield {"src":src,"href":href,"title":title,"price":price,"year":year.strip(),"brand":brand,"model":model}
            self.f.write("\n %s" %title)
            yield {"src": src, "href": response.url, "specs": specs, "title": title, "price": price, "brand": brand,
                   "model": model, "year": year, "reference_id": reference_id, "mileage": mileage, "kilometers": kilometers,
                   "description": "", "total_results": total_results, "page_count": page_count}
        except Exception as e:
            f = open("./ebay_exception.txt", "w")
            f.write(str(e))


if __name__ == "__main__":
  process = CrawlerProcess()
  process.crawl(BlogSpider)
  process.start()
