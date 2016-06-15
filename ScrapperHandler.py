import webapp2
from SummonersWarScraper import SummonersWarScraper

class ScrapperHandler(webapp2.RequestHandler):

    def get(self):
        monsterName = self.request.get("monsterName")
        metric = self.request.get("metric")
        parser = SummonersWarScraper(monsterName)

        metrics = {
            "globalNote": parser.getGlobalNote,
            "dungeonNote": parser.getDungeonNote,
            "arenaOffenceNote": parser.getArenaOffenceNote,
            "arenaDefenseNote": parser.getArenaDefenseNote,

            "globalUserNote": parser.getUserGlobalNote,
            "dungeonUserNote": parser.getUserDungeonNote,
            "arenaOffenceUserNote": parser.getUserArenaOffenceNote,
            "arenaDefenseUserNote": parser.getUserArenaDefenseNote,

            "type": parser.getMonsterType,
            "runesReco" : parser.getRuneRecomendations,
            "awakenName" : parser.getAwakenName,
            "badges": parser.getBadges
        }

        metriclisttocompute = metric.split(",")
        resultascsv = ""
        for metrictocompute in metriclisttocompute:
            try:
                resultascsv += metrics[metrictocompute]() + ","
            except:
                resultascsv += ","
        resultascsv = resultascsv[:-1]

        self.response.write(resultascsv)

app = webapp2.WSGIApplication([
    ('/scrape', ScrapperHandler)
], debug=True)
