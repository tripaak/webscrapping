from scrapy.cmdline import execute

try:

    execute(
        [
            'scrapy',
            'crawl',
            'henryscheinspider'
        ]
    )


except SystemExit:
    pass 