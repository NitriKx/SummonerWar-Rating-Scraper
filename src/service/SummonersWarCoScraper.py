import requests
import json
from bs4 import BeautifulSoup as Soup
from src.models.MonsterType import MonsterType

class SummonersWarCoScraper:

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    def __init__(self, monster_name: str, type: MonsterType):
        self.parser = self.__create_parser(monster_name=monster_name, type=type)

    def get_description(self):
        return {
            "awakenName": self.__get_awaken_name(),
            "overview": self.__get_overview(),
            "reviews": {
                "overall": self.__get_overall_reviews(),
                "type": self.__get_per_purpose_reviews(),
                "pros": self.__get_pros(),
                "cons": self.__get_cons()
            },
            "runes": self.__get_runes_recommendations()
        }

    def __get_awaken_name(self):
        page_main_title = self.parser.select("h1.jeg_post_title")[0].text
        awaken_name = page_main_title.split("(")[1].split(")")[0]
        return self.__clean_text(awaken_name)

    def __get_overview(self):
        overview_items = self.parser.select("section.elementor-section-content-middle .elementor-widget-wrap")[-1].select(".elementor-widget")
        grade = self.__clean_text(overview_items[1].find('span').text).count('★')
        type = self.__clean_text(overview_items[2].find('span').text)
        recommended_usages = self.__clean_text(overview_items[3].text).replace('Badges ', '').split(', ')
        get_from = self.__clean_text(overview_items[4].text).replace('Get From ', '').split(', ')
        good_for = self.__clean_text(overview_items[6].text).replace('Good For ', '')
        skill_up_info = self.__clean_text(overview_items[7].text).replace('Skill Up Info ', '')
        return {
            "grade": grade,
            "type": type,
            "recommendedUsages": recommended_usages, 
            "getFrom": get_from, 
            "goodFor": good_for,
            'skillUpInfo': skill_up_info
        }

    def __get_overall_reviews(self):
        official_review = float(self.parser.select("section.mon-rating-submit-widget .elementor-text-editor.elementor-clearfix")[0].text.split('  ')[0])
        user_review = float(self.parser.select("section.mon-rating-submit-widget .elementor-text-editor.elementor-clearfix")[1].text.split(' ')[0])
        return {
            "official": official_review,
            "user": user_review
        }

    def __get_per_purpose_reviews(self):
        result = {}
        reviews = self.parser.select(".review-list li")
        for review in reviews: 
            title = self.__clean_text(review.text.split(' - ')[0])
            note = self.__clean_text(review.text.split(' - ')[1].split('/')[0])
            if note:
                result[title] = float(note)
        return result

    def __get_runes_recommendations(self):
        # Case 1 - Rune recommendation has stuff in a table
        #          https://summonerswar.co/monster/light-inugami-belladeon/
        recommendation_table = self.parser.select('h2:contains("Rune Recommendations") ~table')
        if len(recommendation_table) > 0:
            recommendation_cells = self.parser.select('h2:contains("Rune Recommendations") ~table td')
            early_types = self.__clean_text(recommendation_cells[1].text).replace('(', '').replace(')', '').split(' / ')
            early_stats = self.__clean_text(recommendation_cells[2].text).replace('(', '').replace(')', '').split(' / ')
            late_types = self.__clean_text(recommendation_cells[4].text).split(' / ')
            late_stats = self.__clean_text(recommendation_cells[5].text).split(' / ')
        # Case 2 - Rune recommendation has everything in one column (no detail for early)
        #          https://summonerswar.co/monster/dark-imp-champion-loque/
        else:
            recommendation_text_blocks = self.parser.select('h2:contains("Rune Recommendations") ~p')
            types = []
            stats = []

            for recommendation_text_block in recommendation_text_blocks:
                recommendation = recommendation_text_block.text.split(' – ')[1]
                types.append(recommendation.split('(')[0].replace('/', ' + '))
                stats.append(recommendation.split('(')[1].replace(')', '').split('/'))

            early_types = types
            early_stats = stats
            late_types = types
            late_stats = stats

        return {
            "early": [
                "types": early_types,
                "stats": early_stats
            ],
            "late": [
                "types": late_types,
                "stats": late_stats
            ]
        }

    def __get_pros(self):
        return self.parser.select(".review-pros p")[1].text.replace('– ', '').split('\n')

    def __get_cons(self):
        return self.parser.select(".review-cons p")[1].text.replace('– ', '').split('\n')

    def __create_parser(self, monster_name: str, type: MonsterType):
        formatted_monster_name = monster_name.strip().replace(' ', '-').lower()
        formatted_type = type.lower()
        r = requests.get(f"http://summonerswar.co/monster/{formatted_type}-{formatted_monster_name}", headers=self.hdr)
        return Soup(r.text, "lxml")

    def __clean_double(self, number):
        return '"' + number.replace(".", ",").replace("\n", "") + '"'

    def __clean_text(self, text):
        return text.strip().replace('\n', '').replace('\t', '')