from domain.eeg_app_aggregate.factory_eeg import EEGFactory
from domain.eeg_app_aggregate.repository_eeg import EEGRepo
from domain.eeg_app_aggregate.root_entity_eeg import EEG
from domain.eeg_app_aggregate.service_eeg import EEGService
from domain.eeg_app_aggregate.value_object_eeg_data_info import EEGDataInfo

class EEGAggregate(EEG, EEGDataInfo, EEGFactory, EEGRepo, EEGService):
    pass