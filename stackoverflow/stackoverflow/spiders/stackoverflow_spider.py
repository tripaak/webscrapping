import scrapy


class StackOverFlow(scrapy.Spider):
    name = "stackoverflow"

    def start_requests(self):
        start_urls = [
            'https://stackoverflow.com/questions/tagged/python'
        ]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for question in response.css('div.mln24'):
            yield{
                'title' : question.css('div.question-summary div.summary h3 a::text' ).get(),
                'time' : question.css('div.question-summary div.user-action-time span::text' ).get(),
                'user': question.css('div.question-summary div.user-details a::text' ).get(),
                } 
        
        #code for next page

        next_page = response.url + response.css('[class="s-pagination--item js-pagination-item"]')[5].css('a::attr(href)').get()[24:]

        #check if there are no next page 
        if response.css('[class="s-pagination--item js-pagination-item"]')[5].css('a::attr(href)').get() is not None:
            # next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        