import datetime

from flask import Flask
from src.models.MonsterType import MonsterType
from src.service.SummonersWarCoScraper import SummonersWarCoScraper


app = Flask(__name__)


@app.route('/')
def root():
    return "Please use /monsterName/type"


@app.route('/<monster_name>/<type>')
def get_monster_description(monster_name: str, type: str):
    parser = SummonersWarCoScraper(monster_name, type)
    return parser.get_description()

    #metrics = {
    #    "globalNote": parser.getGlobalNote,
    #    "dungeonNote": parser.getDungeonNote,
    #    "arenaOffenceNote": parser.getArenaOffenceNote,
    #    "arenaDefenseNote": parser.getArenaDefenseNote,
#
    #    "globalUserNote": parser.getUserGlobalNote,
    #    "dungeonUserNote": parser.getUserDungeonNote,
    #    "arenaOffenceUserNote": parser.getUserArenaOffenceNote,
    #    "arenaDefenseUserNote": parser.getUserArenaDefenseNote,
#
    #    "type": parser.getMonsterType,
    #    "runesReco" : parser.getRuneRecomendations,
    #    "awakenName" : parser.getAwakenName,
    #    "badges": parser.getBadges
    #}
#
    #metriclisttocompute = metric.split(",")
    #resultascsv = ""
    #for metrictocompute in metriclisttocompute:
    #    try:
    #        resultascsv += metrics[metrictocompute]() + ","
    #    except:
    #        resultascsv += ","
    #resultascsv = resultascsv[:-1]
#
    #self.response.write(resultascsv)
#

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)