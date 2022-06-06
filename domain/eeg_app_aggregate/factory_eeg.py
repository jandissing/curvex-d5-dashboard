from infrastructure.base_class_models import Factory
from domain.eeg_app_aggregate.root_entity_eeg import EEG

class EEGFactory(Factory):
    def __init__(self, ):
        self.aggregate_root = EEG

    def create_eeg(self, eeg_values):
        return self.aggregate_root(eeg_values)


eegFactoryInstance = EEGFactory()