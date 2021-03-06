# Web scraping in Python

## Using Scrapy ##

 1. Install Scrapy by entering `pip install scrapy` in your Terminal.

 2. Navigate to the directory where you would like to create your Scrapy project.

 3. Enter `scrapy startproject myproject`. This will create a project with the following directory structure:

    ```
    myproject/
        scrapy.cfg
        myproject/
            __init__.py
            items.py
            pipelines.py
            settings.py
            spiders/
                __init__.py
    ```
    
 4. Navigate to the directory that contains the project's spiders by entering `cd myproject/myproject/spiders`.

 5. Create a new spider by entering `touch myspider.py`, then open it in your default Python code editor by entering `open myspider.py`.

 6. Enter the following code:

    ```python
    import scrapy
    from myproject.items import MyItem

    class MySpider(scrapy.Spider):
        name = 'myspider'
        allowed_domains = ['bwog.com']
        start_urls = ['http://bwog.com']

        def parse(self, response):
            for section in response.xpath('//div[@class="blog-section"]'):
                link = section.xpath('.//a/@href').extract_first()
                yield scrapy.Request(link, callback=self.parse_entry)
            next = response.xpath('//div[@class="comnt-btn"]//@href').extract_first()
            yield scrapy.Request(next, callback=self.parse)

        def parse_entry(self, response):
            for comment in response.xpath('//div[contains(@class, " comment-body")]'):
                item = MyItem()
                
                item['author'] = comment.xpath('./div[@class="comment-author vcard"]/cite/text()').extract_first()
                
                metadata = comment.xpath('./div[@class="comment-meta datetime"]')
                item['up'] = int(metadata.xpath('./span[@data-voting-direction="up"]/span/text()').extract_first())
                item['down'] = int(metadata.xpath('./span[@data-voting-direction="down"]/span/text()').extract_first())
                item['datetime'] = metadata.xpath('./a/text()').extract_first().strip()
                
                paragraphs = comment.xpath('./div[contains(@class, "reg-comment-body")]/p/text()').extract()
                item['content'] = '\n'.join(paragraphs)
                
                yield item
    ```

 7. Edit the project items file in your default Python code editor by entering `open ../items.py`.

 8. Enter the following code:

    ```python
    import scrapy

    class MyItem(scrapy.Item):
        author = scrapy.Field()
        up = scrapy.Field()
        down = scrapy.Field()
        datetime = scrapy.Field()
        content = scrapy.Field()
    ```

 9. Navigate to the top directory of your project by entering `cd ../..`.

 10. Run the spider you created and store its output in a `comments.json` file by entering `scrapy crawl myspider -o comments.json`. View the stored comments by entering `open comments.json`.