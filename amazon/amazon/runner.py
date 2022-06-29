from scrapy.cmdline import execute

try:

    execute(
        [
            'scrapy',
            'crawl',
            'amazon_laptop'
        ]
    )


except SystemExit:
    pass 