## start bot
* start
  - action_time_greeting

## greetings
* greet
  - action_time_greeting
  
## thanking
* thanks
  - utter_welcome
  
## request default happy path 1
* request_recommend
  - restaurant_form
  - form{"name": "restaurant_form"}
  - form{"name": null}
  - utter_ask_pref
* deny OR affirm
  - slot{"pref": []}
  - utter_finish
  - action_try_recommend
  - action_slot_reset
  
## request default happy path 2
* request_recommend
  - restaurant_form
  - form{"name": "restaurant_form"}
  - form{"name": null}
  - utter_ask_pref
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - utter_finish
  - action_try_recommend
  - action_slot_reset
  
## request adv happy path 1
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - action_collect_temp
  - restaurant_form
  - form{"name": "restaurant_form"}
  - form{"name": null}
  - utter_ask_pref
* deny OR affirm
  - slot{"pref": []}
  - utter_finish
  - action_try_recommend
  - action_slot_reset
  
## request adv happy path 2
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - action_collect_temp
  - restaurant_form
  - form{"name": "restaurant_form"}
  - form{"name": null}
  - utter_ask_pref
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - utter_finish
  - action_try_recommend
  - action_slot_reset
  
## request default unhappy path
* request_recommend
  - restaurant_form
  - form{"name": "restaurant_form"}
* chitchat
  - utter_dont_know
  - restaurant_form
  - form{"name": null}
  - utter_ask_pref
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - utter_finish
  - action_try_recommend
  - action_slot_reset
  
## request default very unhappy path
* request_recommend
  - restaurant_form
  - form{"name": "restaurant_form"}
* chitchat
  - utter_dont_know
  - restaurant_form
* chitchat
  - utter_dont_know
  - restaurant_form
  - form{"name": null}
  - utter_ask_pref
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - utter_finish
  - action_try_recommend
  - action_slot_reset

## request default cancelled path
* greet
  - action_time_greeting
* request_recommend
  - restaurant_form
  - form{"name": "restaurant_form"}
* cancel
  - utter_ask_confirmation
* affirm
  - form{"name": null}
  - action_slot_reset
  - utter_cancelled
  
## request adv cancelled path
* greet
  - action_time_greeting
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - action_collect_temp
  - restaurant_form
  - form{"name": "restaurant_form"}
* cancel
  - utter_ask_confirmation
* affirm
  - form{"name": null}
  - action_slot_reset
  - utter_cancelled
  
## request default uncancelled path
* request_recommend
  - restaurant_form
  - form{"name": "restaurant_form"}
* cancel
  - utter_ask_confirmation
* deny
  - restaurant_form
  - form{"name": null}
  - utter_ask_pref
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - utter_finish
  - action_try_recommend
  - action_slot_reset
 
## request adv uncancelled path
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - action_collect_temp
  - restaurant_form
  - form{"name": "restaurant_form"}
* cancel
  - utter_ask_confirmation
* deny
  - restaurant_form
  - form{"name": null}
  - utter_ask_pref
* request_recommend{"pref":"bakso"}
  - slot{"pref": ["bakso"]}
  - utter_finish
  - action_try_recommend
  - action_slot_reset

## check
* check
  - utter_slot_check