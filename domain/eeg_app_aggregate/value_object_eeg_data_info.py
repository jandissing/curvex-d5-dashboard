from dataclasses import dataclass
from infrastructure.base_class_models import ValueObject
from infrastructure.useful_functions import actual_time_in_string

@dataclass(frozen=True)
class EEGDataInfo(ValueObject):
    creation_date = actual_time_in_string()
    eeg_data_values: dict
    