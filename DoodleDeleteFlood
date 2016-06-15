from bs4 import BeautifulSoup as Soup
import urllib2

class SummonersWarScraper:

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    def __init__(self, monsterName):
        self.parser = self.createParser(monsterName)

    def createParser(self, monsterName):
        request = urllib2.Request("http://summonerswar.co/" + monsterName, headers=self.hdr)
        content = urllib2.urlopen(request).read()
        return Soup(content, "lxml")

    def reformatDoubleNumbers(self, number):
        return '"' + number.replace(".", ",").replace("\n", "") + '"'

    def reformatText(self, number):
        return '"' + number.replace("\n", "") + '"'


    def getGlobalNote(self):
        return self.reformatDoubleNumbers(self.parser.select(".rating .number")[0].text)

    def getUserGlobalNote(self):
        return self.reformatDoubleNumbers(self.parser.select(".rating .number")[1].text)

    def getDungeonNote(self):
        return self.reformatDoubleNumbers(self.parser.select("#editor_rating_0 .number")[0].text)

    def getUserDungeonNote(self):
        return self.reformatDoubleNumbers(self.parser.select("#user_rating_0 .number")[0].text)

    def getArenaOffenceNote(self):
        return self.reformatDoubleNumbers(self.parser.select("#editor_rating_1 .number")[0].text)

    def getUserArenaOffenceNote(self):
        return self.reformatDoubleNumbers(self.parser.select("#user_rating_1 .number")[0].text)

    def getArenaDefenseNote(self):
        return self.reformatDoubleNumbers(self.parser.select("#editor_rating_2 .number")[0].text)

    def getUserArenaDefenseNote(self):
        return self.reformatDoubleNumbers(self.parser.select("#user_rating_2 .number")[0].text)

    def getOverallValue(self):
        return self.reformatDoubleNumbers(self.parser.select("#editor_rating_6 .number")[0].text)

    def getOverallUserValue(self):
        return self.reformatDoubleNumbers(self.parser.select("#user_rating_6 .number")[0].text)


    def getMonsterType(self):
        detailslabels = self.parser.select(".detail-item .detail-label")
        type = "Unknown"
        for detail in detailslabels:
            if detail.text == "Type":
                type = detail.parent.select(".detail-content")[0].text
                break
        return self.reformatText(type)


    def getRuneRecomendations(self):
        fulldescriptiontitles = self.parser.select("#content-anchor-inner h2 strong")
        runerecommandations = ""
        maxrunenumber = 4
        for descriptiontitle in fulldescriptiontitles:
            if descriptiontitle.text.find("Rune") >= 0:
                currentTag = descriptiontitle.parent.findNext("p")
                iterator = 0
                while currentTag.name == "p":
                    if (iterator != 0):
                        runerecommandations += ","

                    runerecommandations += self.reformatText(currentTag.text)
                    currentTag = currentTag.findNext()
                    iterator += 1

        while iterator < maxrunenumber:
            runerecommandations += ","
            iterator += 1

        return runerecommandations

    def getAwakenName(self):
        pagetitle = self.parser.select("h1.main-title")[0].text
        awakenName = pagetitle.split("(")[1].split(")")[0]
        return self.reformatText(awakenName)

    def getBadges(self):
        return self.reformatText(self.parser.select(".badge-wrapper")[0].get('title'))

def main():
    scraper = SummonersWarScraper("fire-serpent-fao")
    print scraper.getBadges()

if __name__ == "__main__":
    main()