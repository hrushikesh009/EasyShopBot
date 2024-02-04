from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
import requests
import firebase_admin
from firebase_admin import db, credentials, firestore

cred_obj = credentials.Certificate('SmartEcommerceFirebasekey.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': 'https://smartecom-60f57-default-rtdb.firebaseio.com/'})
ref = db.reference('/')
ref_firestore = firestore.client()
user_id = "A3E652YQA5UQAY"

def retrieve_data(category):
    for i in range(3):
        cat = f'Sub_Category/{i}'
        result = ref.child('Products').order_by_child(cat).equal_to(category).limit_to_first(5).get()
        if result:
            return list(result.values())

def retrieve_data_from_recommender_api(userid):
    recommended_products = requests.get(f"https://5000-amber-pig-upxd6yew.ws-us04.gitpod.io/{userid}")
    return recommended_products.json()['Recommended_Products'][:5]

class ActionRecommender(Action):

    def name(self) -> Text:
        return "action_recommend_products"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        users = ref_firestore.collection('User').where('user_id', '==', user_id).stream()

        if len([user.id for user in users]) > 0:
            recommend_products = retrieve_data_from_recommender_api(user_id)
            recommend_products_list = []

            for product in recommend_products:
                refer = f'Products/{product}'
                result = ref.child(refer).get()
                recommend_products_list.append(result)

            for i, product in enumerate(recommend_products_list):
                dispatcher.utter_message(
                    text=f"Product Title: {product['title']}",
                    image=product['image'][0]
                )
            dispatcher.utter_message(text="If you liked the products type 1..5 according to the product you want! ;)")
        else:
            dispatcher.utter_message(text="You seem like a new user. Here are our top 5 products! ;)")
            popular_products = ['B000VRMV1I', 'B000U6H08O', 'B000PGJ3IE', 'B000P4M1F8', 'B000EHTY0Q']
            recommend_products_list = []

            for product in popular_products:
                refer = f'Products/{product}'
                result = ref.child(refer).get()
                recommend_products_list.append(result)

            for i, product in enumerate(recommend_products_list):
                dispatcher.utter_message(
                    text=f"Product Title: {product['title']}",
                    image=product['image'][0]
                )
            dispatcher.utter_message(text="If you liked the products type 1..5 according to the product you want! ;)")

        return [SlotSet("products_list", recommend_products_list)]

class ActionSearchProvider(Action):

    def name(self) -> Text:
        return "action_search_products"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        category = tracker.get_slot("category_type")
        products = retrieve_data(category)

        if products:
            for i, product in enumerate(products):
                dispatcher.utter_message(
                    text=f"Product Title: {product['title']}",
                    image=product['image'][0]
                )
            dispatcher.utter_message(text="If you liked the products type 1..5 according to the product you want! ;)")
        else:
            dispatcher.utter_message(text="Sorry, we couldn't find products related to your category! :(")

        return [SlotSet("products_list", products)]

class ActionLookupAddress(Action):

    def name(self) -> Text:
        return "action_address_lookup"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        users = ref_firestore.collection('User').where('user_id', '==', user_id).stream()

        if len([user.id for user in users]) > 0:
            address_list = ref_firestore.collection(u'User').document(user_id).collection(u'address').limit(2).stream()
            address = [addr.to_dict() for addr in address_list]

            if address:
                options = [{'title': addr['address'], 'payload': '/address_found'} for addr in address]
                dispatcher.utter_message(
                    text="Here is your latest address we found. Please pick one!",
                    buttons=options
                )
                return [SlotSet("address", address[0]['address'])]

        dispatcher.utter_message(text="We couldn't find an address. Can you please help us with the address here!")
        return []

class ActionAddAddress(Action):

    def name(self) -> Text:
        return "action_add_address"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        current_address = tracker.latest_message['text']
        ref_firestore.collection(u'User').document(user_id).set({u'user_id': user_id})
        ref_firestore.collection(u'User').document(user_id).collection(u'address').document().set({u'address': current_address})
        dispatcher.utter_message(text="Your address has been added successfully!")
        return [SlotSet("address", current_address)]

class ActionPlaceOrder(Action):

    def name(self) -> Text:
        return "action_order_placed"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        address_selected = tracker.get_slot("address")
        payment_selected = tracker.get_slot("payment_type")
        option_selected = tracker.get_slot('option_select')
        products_list = tracker.get_slot('products_list')
        dict_data = {
            'ProdID': products_list[int(option_selected) - 1]['ProdID'],
            'payment_type': payment_selected,
            'brand': products_list[int(option_selected) - 1]['brand'],
            'address': address_selected,
            'image': products_list[int(option_selected) - 1]['image'],
            'price': products_list[int(option_selected) - 1]['price'],
            'rating': products_list[int(option_selected) - 1]['rating'],
            'title': products_list[int(option_selected) - 1]['title']
        }
        ref_firestore.collection(u'User').document(user_id).set({u'user_id': user_id})
        ref_firestore.collection(u'User').document(user_id).collection(u'cart').document().set(dict_data)
        dispatcher.utter_message(text="Your order has been placed! Thank you :)")
        return []
