from infrastructure.base_class_models import Repository
from domain.eeg_app_aggregate.value_object_eeg_data_info import EEGDataInfo
from infrastructure.connection_to_nosql_db import database_api
from bson.objectid import ObjectId
import uuid

# def fetch_eegdata_by_id(profile_id):
#         try:
#             return database_api.find_one({"profile.profile_id": uuid.UUID(str(profile_id))})['profile'][0]['eeg_data']
#         except:
#             return "Profile not found"

class EEGRepo(Repository):
    def save_eeg_to_db(self, eeg_values, profile_id):
        profile_index_count = 0
        try:
            for profile in database_api.find_one({"profile.profile_id": profile_id})['profile']:
                if profile['profile_id'] == profile_id:
                    print(profile)
                    print("Profile found")
                    string_for_profile_location = "profile." + str(profile_index_count) + ".eeg_data"
                    database_api.update_one({"profile.profile_id": profile_id}, {"$push": {string_for_profile_location: eeg_values}})
                    return profile
                else:
                    profile_index_count += 1
        except:        
            return print("Profile not found")

    def fetch_eeg_by_id(profile_id):
        profile_index_count = 0
        try:
            for profile in database_api.find_one({"profile.profile_id": profile_id}, {"_id": 0})['profile']:
                if profile['profile_id'] == profile_id:
                    print("Profile found")
                    print("Checking if there is eeg data...")
                    # return database_api.find_one({"profile.profile_id": uuid.UUID(str(profile_id))})['profile'][profile_index_count]['eeg_data']
                    return {"profilename": database_api.find_one({"profile.profile_id": profile_id})['profile'][profile_index_count]['profileinfo']['name'], "values" : database_api.find_one({"profile.profile_id": profile_id})['profile'][profile_index_count]['eeg_data']}
                else:
                    profile_index_count += 1
        except:
            return "Profile or eegdata not found"

    def fetch_all_eeg():
        # profile_index_count = 0
        data = list(database_api.find({}))
        import datetime
        from dateutil import parser
        import pandas as pd
        all_df = pd.DataFrame()
        for i in data:
            # print(i['_id'])
            # print(i['profile'])
            for x in i['profile']:
                # print("-------")
                # print(x['eeg_data'])
                try:
                    count=0
                    for y in x['eeg_data']:
                        count+=1
                        initial_datetime = parser.parse(y['creation_date'])
                        added_seconds = datetime.timedelta(0, len(y['eeg_data_info']['eeg_data_values']['Delta']))
                        final_datetime = initial_datetime + added_seconds
                        df = pd.DataFrame(y['eeg_data_info']['eeg_data_values'])
                        df['Session'] = 'Session ' + str(count)
                        df['Profile_id'] = x['profile_id']
                        df['Profile Name'] = x['profileinfo']['name']
                        df['Session Start and End Time'] = y['creation_date'] + " - " + final_datetime.strftime("%m/%d/%Y, %H:%M:%S")
                        df['Customer_id'] = i['customer_id']
                        df['Customer Name'] = i['customer_info']['first_name'] + " " + i['customer_info']['last_name']
                        # print(df.head(2))
                        all_df = pd.concat([all_df, df], axis=0, ignore_index=True)
                except:
                    print("No eeg_data here")
        all_df = all_df[['Customer_id', 'Customer Name', 'Profile_id', 'Profile Name', 'Session', 'Session Start and End Time', 'Delta', 'Theta', 'Low Alpha', 'High Alpha', 'Low Beta', 'High Beta', 'Low Gamma', 'Middle Gamma', 'Cognitive Load', 'Flow', 'Focus', 'Stress']]
        # print(all_df.columns)
        # print(all_df.tail(3))
        return all_df.to_dict('records')
    
    def get_customer_id_by_profile_id(profile_id):
        return database_api.find_one({"profile.profile_id": profile_id})['customer_id']
    
    def get_profile_name_by_profile_id(profile_id):
        return [i['profileinfo']['name'] for i in database_api.find_one({"profile.profile_id": profile_id}, {'_id':0 , "profile.profile_id": 1, 'profile.profileinfo.name':1 })['profile'] if i['profile_id'] == profile_id][0]

    def fetch_eeg_by_subscription_id_for_b2b_app(self, subscription_id):
        print("TODO;...")
        return None

    def erase_all_eeg(self):
        print("TODO;...")
        return None


eegRepositoryInstance = EEGRepo()