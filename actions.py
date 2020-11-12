# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused, FollowupAction
import geocoder
from datetime import datetime
from random import random
from rasa_sdk.forms import FormAction
from typing import Dict, Text, Any, List, Union, Optional
import re, math
from collections import Counter
import numpy as np
import pandas as pd
import operator
import json
import pprint


#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# restart bot
class ActionChatRestarted(Action):

    def name(self):
        return "action_chat_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]


# reset slot
class ActionSlotReset(Action):
    def name(self):
        return 'action_slot_reset'

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


class ActionTimeGreeting(Action):
    def name(self):
        return 'action_time_greeting'

    def run(self, dispatcher, tracker, domain):
        time = tracker.get_slot('time')
        if not time:
            now = datetime.now()
            now_hour = now.strftime("%H")
            if 4 <= int(now_hour) < 10:
                time = "pagi"
            elif 10 <= int(now_hour) < 15:
                time = "siang"
            elif 15 <= int(now_hour) < 19:
                time = "sore"
            else:
                time = "malam"

        k = random()
        if k < 0.25:
            response = """Selamat {}, aku adalah Rec-Food, aku bisa kasih kamu rekomendasi tempat makan.\nUntuk mulai rekomendasi bisa coba tulis seperti 'tolong cari tempat makan' atau 'laper nih cariin tempat makan dong'. Kamu juga bisa langsung sebutin apa yang kamu mau seperti 'laper nih mau cari sate' atau 'cariin tempat makan jepang dong'""".format(time)
        elif 0.25 <= k < 0.5:
            response = """Halo, selamat {}, aku adalah Rec-Food, aku bisa kasih kamu rekomendasi tempat makan.\nUntuk mulai rekomendasi bisa coba tulis seperti 'tolong cari tempat makan' atau 'laper nih cariin tempat makan dong'. Kamu juga bisa langsung sebutin apa yang kamu mau seperti 'laper nih mau cari sate' atau 'cariin tempat makan jepang dong'""".format(time)
        elif 0.5 <= k < 0.75:
            response = """{}, aku adalah Rec-Food, aku bisa kasih kamu rekomendasi tempat makan.\nUntuk mulai rekomendasi bisa coba tulis seperti 'tolong cari tempat makan' atau 'laper nih cariin tempat makan dong'. Kamu juga bisa langsung sebutin apa yang kamu mau seperti 'laper nih mau cari sate' atau 'cariin tempat makan jepang dong'""".format(time.capitalize())
        else:
            response = """{} kak, aku adalah Rec-Food, aku bisa kasih kamu rekomendasi tempat makan.\nUntuk mulai rekomendasi bisa coba tulis seperti 'tolong cari tempat makan' atau 'laper nih cariin tempat makan dong'. Kamu juga bisa langsung sebutin apa yang kamu mau seperti 'laper nih mau cari sate' atau 'cariin tempat makan jepang dong'""".format(time.capitalize())
        dispatcher.utter_message(response)
        return [SlotSet("time", time)]


class ActionCollectTemp(Action):
    def name(self):
        return 'action_collect_temp'

    def run(self, dispatcher, tracker, domain):
        set_slot = []
        pref = tracker.get_slot('pref')
        preferences = ' '.join(pref)

        if 'italia' not in preferences and ('pasta' in preferences or 'pizza' in preferences):
            preferences = preferences + ' italia'

        if 'jepang' not in preferences and ('sushi' in preferences or 'shabu' in preferences or 'ramen' in preferences or
                                            'takoyaki' in preferences):
            preferences = preferences + ' jepang'

        if 'amerika' not in preferences and 'burger' in preferences:
            preferences = preferences + ' amerika'

        if 'warteg' in preferences:
            preferences = preferences + ' jawa sunda'

        if 'somay' in preferences or 'martabak' in preferences:
            set_slot.append(SlotSet("resto", "jajanan"))

        if 'lokal' not in preferences and ('ayam' in preferences or 'bebek' in preferences or 'geprek' in preferences or
                                           'sate' in preferences or 'bakmi' in preferences or 'bakso' in preferences or
                                           'jawa' in preferences or 'sunda' in preferences or 'ntt' in preferences or
                                           'padang' in preferences or 'martabak' in preferences or
                                           'jakarta' in preferences or 'batak' in preferences or 'soto' in preferences or
                                           'sumatra' in preferences or 'sulawesi' in preferences or 'somay' in preferences or
                                           'batagor' in preferences):
            preferences = preferences + ' lokal'

        if 'lokal' in preferences:
            set_slot.append(SlotSet("region", "lokal"))

        if 'cafe' in preferences:
            set_slot.append(SlotSet("resto", "cafe"))

        if 'jajanan' in preferences:
            set_slot.append(SlotSet("resto", "jajanan"))

        if ('thai' in preferences or 'vietnam' in preferences or 'jepang' in preferences or 'korea' in preferences or
            'chinese' in preferences) and ('amerika' in preferences or 'belanda' in preferences or
                                           'italia' in preferences or 'eropa' in preferences):
            set_slot.append(SlotSet("region", "western asia"))

        elif 'thai' in preferences or 'vietnam' in preferences or 'jepang' in preferences or 'korea' in preferences or \
                'chinese' in preferences:
            set_slot.append(SlotSet("cuisines", "asia"))

        elif 'amerika' in preferences or 'belanda' in preferences or 'italia' in preferences or 'eropa' in preferences:
            set_slot.append(SlotSet("cuisines", "western"))

        if 'thai' in preferences or 'vietnam' in preferences or 'jepang' in preferences or 'korea' in preferences or \
                'chinese' in preferences or 'amerika' in preferences or 'belanda' in preferences or 'italia' in \
                preferences or 'eropa' in preferences:
            set_slot.append(SlotSet("region", "internasional"))

        set_slot.append(SlotSet("temp_pref", preferences))

        return set_slot


class RestaurantForm(FormAction):
    def name(self):
        return 'restaurant_form'

    @staticmethod
    def required_slots(tracker: Tracker):
        """A list of required slots that the form has to fill"""
        # if tracker.get_slot('pref') and ('sushi' in tracker.get_slot('pref') or 'shabu' in tracker.get_slot('pref')):
        #     SlotSet("region", "internasional")
        #     SlotSet("cuisines", "asia")
        if tracker.get_slot('region') and ('internasional' in tracker.get_slot('region')):
            return ["area", "region", "cuisines", "resto", "wifi", "seat", "budget"]
        else:
            return ["area", "region", "resto", "wifi", "seat", "budget"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "budget": [
                self.from_entity(entity="budget", intent="inform_budget"),
                self.from_intent(intent="deny", value="None")
            ],
            "seat": self.from_entity(entity="seat", intent="inform_seat")
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        # dispatcher.utter_message(template="utter_finish")
        return []

class ActionTryRecommend(Action):
    def name(self):
        return 'action_try_recommend'

    @staticmethod
    def cosine_similarity_of(text1, text2):
        # get words first
        first = re.compile(r"[\w']+").findall(text1)
        second = re.compile(r"[\w']+").findall(text2)

        # get dictionary with each word and count.
        vector1 = Counter(first)
        vector2 = Counter(second)

        # convert vectors to set to find common words as intersection
        common = set(vector1.keys()).intersection(set(vector2.keys()))

        dot_product = 0.0

        for i in common:
            # get amount of each common word for both vectors and multiply them then add them together.
            dot_product += vector1[i] * vector2[i]

        squared_sum_vector1 = 0.0
        squared_sum_vector2 = 0.0

        # get squared sum values of word counts from each vector.
        for i in vector1.keys():
            squared_sum_vector1 += vector1[i] ** 2

        for i in vector2.keys():
            squared_sum_vector2 += vector2[i] ** 2

        # calculate magnitude with squared sums.
        magnitude = math.sqrt(squared_sum_vector1) * math.sqrt(squared_sum_vector2)

        if not magnitude:
            return 0.0
        else:
            return float(dot_product) / magnitude

    def get_recommendations(self, keywords, budget, area):
        df = pd.read_csv('resto.csv')
        score_dict = {}

        for index, row in df.iterrows():
            score_dict[index] = self.cosine_similarity_of(row['desc'], keywords)

        # sort cities by score and index.
        sorted_scores = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)

        counter = 0

        # create an empty results data frame.
        result_df = pd.DataFrame(columns=('name', 'address', 'rating', 'price', 'description', 'url', 'score'))

        # get highest scored 5 cities.
        if area == "None":
            for i in sorted_scores:
                # print index dan score resto.
                # print(i[0], i[1])
                if int(df.iloc[i[0]]['category_price']) < float(budget) and i[1] >= 0.7:
                    result_df = result_df.append(
                        {'name': df.iloc[i[0]]['name'], 'address': df.iloc[i[0]]['address'], 'rating': df.iloc[i[0]]['rating'],
                         'price': df.iloc[i[0]]['category_price'], 'description': df.iloc[i[0]]['desc'],
                         'url': df.iloc[i[0]]['url'], 'score': i[1]}, ignore_index=True)
                    # counter += 1

                if i[1] < 0.7:
                    break
        else:
            for i in sorted_scores:
                # print index dan score resto.
                # print(i[0], i[1])
                if int(df.iloc[i[0]]['category_price']) < float(budget) and df.iloc[i[0]]['location'] == area and i[1] >= 0.7:
                    result_df = result_df.append(
                        {'name': df.iloc[i[0]]['name'], 'address': df.iloc[i[0]]['address'], 'rating': df.iloc[i[0]]['rating'],
                         'price': df.iloc[i[0]]['category_price'], 'description': df.iloc[i[0]]['desc'],
                         'url': df.iloc[i[0]]['url'], 'score': i[1]}, ignore_index=True)
                    # counter += 1

                if i[1] < 0.7:
                    break

        result_df = result_df.sort_values(by=['score', 'rating'], ascending=False)
        # convert DF to json.
        json_result = json.dumps(result_df.to_dict('records'))
        return json_result

    def get_top(self, json_string):
        lst = json.loads(json_string)
        res = []
        lst_len = len(lst)
        n_max = 10
        i = 0
        while i < lst_len and i < n_max:
            res.append((lst[i]['name'], lst[i]['address'], lst[i]['rating'], lst[i]['price'], lst[i]['url'],
                        lst[i]['description']))
            i += 1

        return res

    def run(self, dispatcher, tracker, domain):
        # try:
        # if 'df' not in globals():

        keywords = ''
        region = tracker.get_slot('region')
        keywords = keywords + ' ' + region

        resto = tracker.get_slot('resto')
        keywords = keywords + ' ' + resto

        cuisines = tracker.get_slot('cuisines')
        if cuisines:
            keywords = keywords + ' ' + cuisines

        wifi = tracker.get_slot('wifi')
        keywords = keywords + ' ' + wifi

        pref = tracker.get_slot('pref')
        temp_pref = tracker.get_slot('temp_pref')
        preferences = ''
        if pref:
            preferences = ' '.join(pref)
        if temp_pref:
            preferences = preferences + ' ' + temp_pref

        if 'kopi' not in preferences and resto == 'cafe':
            preferences = preferences + ' kopi'

        if 'cemilan' not in preferences and resto == 'bakery':
            preferences = preferences + ' cemilan'

        if 'fast food' not in preferences and 'burger' in preferences:
            preferences = preferences + ' fast food'

        if 'cemilan' not in preferences and 'martabak' in preferences:
            preferences = preferences + ' cemilan'

        if 'buffet' not in preferences and 'shabu' in preferences:
            preferences = preferences + ' buffet'

        if 'alkohol' not in preferences and resto == 'bar':
            preferences = preferences + ' alkohol'

        if resto != 'bar' and 'alkohol' in preferences:
            preferences = preferences + ' bar'

        if 'italia' not in preferences and ('pasta' in preferences or 'pizza' in preferences):
            preferences = preferences + ' italia'

        if 'jepang' not in preferences and ('sushi' in preferences or 'shabu' in preferences or 'ramen' in preferences or
                                            'takoyaki' in preferences):
            preferences = preferences + ' jepang'

        if 'amerika' not in preferences and 'burger' in preferences:
            preferences = preferences + ' amerika'

        if 'jawa' not in preferences and ('geprek' in preferences or 'warteg' in preferences):
            preferences = preferences + ' jawa'

        if 'sunda' not in preferences and 'warteg' in preferences:
            preferences = preferences + ' sunda'

        if 'lokal' not in keywords and ('ayam' in preferences or 'bebek' in preferences or 'geprek' in preferences or
                                        'sate' in preferences or 'bakmi' in preferences or 'bakso' in preferences or
                                        'jawa' in preferences or 'sunda' in preferences or 'ntt' in preferences or
                                        'padang' in preferences or 'martabak' in preferences or
                                        'jakarta' in preferences or 'batak' in preferences or 'soto' in preferences or
                                        'sumatra' in preferences or 'sulawesi' in preferences or 'somay' in preferences or
                                        'batagor' in preferences or 'warkop' in preferences):
            preferences = preferences + ' lokal'

        if 'asia' not in keywords and ('thai' in preferences or 'vietnam' in preferences or 'jepang' in preferences or
                                       'korea' in preferences or 'chinese' in preferences):
            preferences = preferences + ' asia'

        if 'western' not in keywords and ('amerika' in preferences or 'belanda' in preferences or 'italia' in preferences or
                                          'eropa' in preferences):
            preferences = preferences + ' western'

        if 'internasional' not in keywords and ('western' in preferences or 'asia' in preferences):
            preferences = preferences + ' internasional'

        keywords = keywords + ' ' + preferences + ' '
        keywords = re.sub(r'nya\s', ' ', keywords)
        keywords = list(set(keywords.split()))
        keywords = ' '.join(keywords)

        budget = tracker.get_slot('budget')
        if budget == "None":
            budget = "100000000"
        budget = re.sub(r'[^0-9]', '', budget)
        budget = re.sub(r'.k', '000', budget)
        budget = re.sub(r'.rb', '000', budget)
        budget = re.sub(r'.ribu', '000', budget)

        seat = tracker.get_slot('seat')
        if re.search(r"[a-z]", seat):
            seat = "1"
        mean_budget = int(budget)/int(seat)

        area = tracker.get_slot('area')

        result_key = self.get_recommendations(keywords, mean_budget, area)
        top_list = self.get_top(result_key)

        dispatcher.utter_message("keywords : " + keywords)
        if len(top_list) == 0:
            dispatcher.utter_message("Maaf kak, kita ga nemu restoran yang kakak mau :(")

        else:
            # user_choice = [region, resto, cuisines]
            # if pref:
            #     user_choice.extend(pref)
            # if temp_pref:
            #     user_choice.extend(temp_pref.split())
            # user_choice = list(set(user_choice))
            user_choice = keywords.split()

            for i in range(len(top_list)):
                if 'babi' in top_list[i][5]:
                    response = "(" + str(i+1) + ")\nNama : " + top_list[i][0] + "\nAlamat : " + top_list[i][1] + "\nRating : " + str(top_list[i][2]) + "\nHarga : " + str(top_list[i][3]) + "\nLink : " + top_list[i][4] + "\nMENGANDUNG BABI!"
                else:
                    response = "(" + str(i+1) + ")\nNama : " + top_list[i][0] + "\nAlamat : " + top_list[i][1] + "\nRating : " + str(top_list[i][2]) + "\nHarga : " + str(top_list[i][3]) + "\nLink : " + top_list[i][4]
                response = response + "\nKarena kamu ingin mencari makanan/tempat makan dengan kriteria"
                desc = top_list[i][5].split()
                for j in range(len(user_choice)):
                    if user_choice[j] in desc:
                        response = response + ', ' + user_choice[j]
                dispatcher.utter_message(response)

        # except:
        #     response = """Pencarian Gagal"""
        #     dispatcher.utter_message(response)

# class ActionSolveProblem(Action):
#     def name(self):
#         return 'action_solve_problem'
#     def run(self, dispatcher, tracker, domain):
#         problem = tracker.get_slot('deleted')
#         if problem == 'area':
#             return [SlotSet("area", "None")]
#         else:
#             return [SlotSet("budget", "500000")]
#
# class ActionGetLoc(Action):
#     # FAIL (malah server location)
#     def name(self):
#         return 'action_get_loc'
#
#     def run(self, dispatcher, tracker, domain):
#         try:
#             g = geocoder.ip('me')
#             loc = g.address
#
#             response = """Kamu berada di {}""".format(loc)
#             dispatcher.utter_message(response)
#         except:
#             response = """Location not found"""
#             dispatcher.utter_message(response)
