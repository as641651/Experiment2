from project_utils import get_trace_durations

class FilterOnKPIs:
    def __init__(self, case_table, measurements):
        case_durations = get_trace_durations(measurements)

        df = case_durations.merge(case_table, on="case:concept:name")
        min_flop = df['case:flops'].min()
        min_duration = df['case:duration'].min()

        df['case:rel-flops'] = df.apply(lambda row: (row['case:flops'] - min_flop) / min_flop, axis=1)
        df['case:rel-duration'] = df.apply(lambda row: (row['case:duration'] - min_duration) / min_duration, axis=1)

        self.case_table = df

    def filter_on_flops_and_rel_duration(self, rel_duration_limit=None):

        if not rel_duration_limit:
            rel_duration_limit = self.case_table[self.case_table['case:rel-flops'] == 0]['case:rel-duration'].max()
            if rel_duration_limit > 1.2:
                rel_duration_limit = 1.2

        return self.case_table[(self.case_table['case:rel-flops'] == 0) |
                               (self.case_table['case:rel-duration'] < rel_duration_limit)]

    def filter_on_best_flops(self):
        return self.case_table[self.case_table['case:rel-flops'] == 0]

    def filter_on_rel_duration(self, rel_duration_limit):
        return self.case_table[self.case_table['case:rel-duration'] < rel_duration_limit]

    def get_alg_seq_sorted_on_duration(self, case_table):
        return list(case_table.sort_values(by=['case:duration'])['case:concept:name'])


