from datetime import datetime
import numpy as np


def actual_time_in_string():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")



# def random_eeg_fake_data(a, b):
#     time        = np.arange(0, 10, 0.1)
#     amplitude   = np.sin(time)
#     dict = {"time" : time.tolist(), "amplitude": amplitude.tolist()}
#     return dict


# def random_eeg_fake_data2(lines):
#     values = [np.random.randint(700, 1200) for line in range(lines)]
#     return {"values" : values}

def random_eeg_processed_fake_data(time_in_seconds):
    waves_list = ['Delta', 'Theta', 'Low Alpha', 'High Alpha', 'Low Beta', 'High Beta',
       'Low Gamma', 'Middle Gamma']
    metrics_list = ['Cognitive Load', 'Flow', 'Focus', 'Stress']
    waves = {wave: [round(np.random.uniform(1, 15),3) for line in range(time_in_seconds)] for wave in waves_list}
    metrics = {'Cognitive Load': [round(np.random.uniform(0, 7),2) for line in range(time_in_seconds)], "Flow": [round(np.random.uniform(0, 11),2) for line in range(time_in_seconds)], "Focus": [round(np.random.uniform(0, 4),2) for line in range(time_in_seconds)], "Stress": [round(np.random.uniform(0, 3),2) for line in range(time_in_seconds)]}
    waves.update(metrics)
    return waves