import pandas as pd
from project_utils import get_trace_durations

class CaseDurationsManager:
    def __init__(self, case_table=None):
        self.case_table = case_table
        self.case_durations = None

    def add_case_durations(self, measurements):
        self.case_durations = pd.concat([self.case_durations, get_trace_durations(measurements)], ignore_index=True)

    def get_alg_measurements(self):
        alg_list = [alg.split('_')[0] for alg in list(self.case_durations['case:concept:name'])]
        alg_list = list(set(alg_list))

        alg_measurements = {}
        for alg in alg_list:
            t_alg = self.case_durations[self.case_durations.apply(
                lambda x: x['case:concept:name'].split('_')[0] == alg, axis=1)]
            alg_measurements[alg] = list(t_alg['case:duration'])
        return alg_measurements

    def clear_case_durations(self):
        self.case_durations = None