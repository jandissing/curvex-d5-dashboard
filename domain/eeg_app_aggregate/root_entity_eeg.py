from infrastructure.base_class_models import Entity
from domain.eeg_app_aggregate.value_object_eeg_data_info import EEGDataInfo
from infrastructure.useful_functions import actual_time_in_string

class EEG(Entity):        
    def __init__(self, eeg_data_values):
        self.creation_date = actual_time_in_string()
        self.eeg_data_id = self.next_id()
        self.eeg_data_info = {}
        self.eeg_data_info.update(EEGDataInfo(eeg_data_values=eeg_data_values).__dict__)