from scrapy.cmdline import execute

try:

    execute(
        [
            'scrapy',
            'crawl',
            'megadental_2'
        ]
    )


except SystemExit:
    pass 