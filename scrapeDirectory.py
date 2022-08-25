import scrapy
import string
from scrapy.http import Request

baselink = 'https://directory.columbia.edu/people/browse/students?filter.initialLetter='
letters = list(string.ascii_uppercase)
start_links = [baselink + letter for letter in letters]
class UNISpider(scrapy.Spider):
    name = 'uni'
    index = 0
    start_urls = [start_links[0]]
    url_index = 0
    def parse(self, response):
        execution = response.xpath("//input[@name='execution']/@value").extract()
        if (len(execution) != 0):
            yield scrapy.FormRequest.from_response(response, formdata={"username":"jmc2437",  "password":"1Wormgeartoeachhisown", "execution": execution[0]}, callback=self.parse_after_login)
        else:
            yield Request(self.start_urls[0], callback=self.parse_after_login, dont_filter = True)
    def parse_after_login(self, response):
        table = response.css('div.table_results').extract()[0]
        items = scrapy.Selector(text = table).xpath("//table/tr")[1:]
        items = [item for item in items if len(item.css("div::text").extract()) != 0 and item.css("div::text").extract()[0] in ["Student, COLUMBIA COLLEGE", "Student, FU FOUNDATN SCHL OF ENGINEERING & APPLIED SCIENCE:UGRAD"]]
        for item in items:
            name = item.css("a::text").get()
            lastname = name.split(',')[0]
            firstname = name.split(',')[1].strip().split(' ')[0]
            department = item.css("div::text").extract()
            address = item.css("td.back1::text").extract()
            result =  {
                "First Name":  firstname,
                "Last Name": lastname,
                "Title": item.css("div::text").extract()[0],
                "Department": "" if len(department) != 2 else department[1],
                "Address": ", ".join(address),
                "Email": item.css("a.mailto::text").get()
            }
            yield result
        nextButton = response.xpath("//a[contains(@title, 'Next Page')]")
        if (len(nextButton.getall()) != 0):
            print("NEXT PAGE")
            self.index += 1
            nextLink = "https://directory.columbia.edu/people/browse/students?page=" + str(self.index)
            yield Request(nextLink, callback=self.parse_after_login, dont_filter = True)
        elif self.url_index != len(start_links) - 1:
            print("NEXT LETTER")
            self.index = 0
            self.url_index += 1
            yield Request(start_links[self.url_index], callback=self.parse_after_login, dont_filter = True)
        else:
            print("DONE")

