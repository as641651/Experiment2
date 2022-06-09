import pandas as pd

class FilterVariants:
    """Calculates duration of each case from the event table
    and appends to case table in column 'case:duration'

    This class provides functions that returns filtered case and event tables;
    filtering based on min flops, min duration, worst flops or both min flops and duration

    """

    def __init__(self, case_table, event_table):
        """
        INPUT: Case table and event table.
        Init appends 'case:duration' to the case table"""

        self.event_table = event_table
        case_durations = self.get_trace_durations()
        self.case_table = case_durations.merge(case_table, on="case:concept:name")

    def get_trace_durations(self):
        """calculates duration of each case from event table"""
        dfs = self.event_table.drop_duplicates('case:concept:name', keep='first')[
            ['case:concept:name', 'timestamp:start']]
        dfe = self.event_table.drop_duplicates('case:concept:name', keep='last')[['case:concept:name', 'timestamp:end']]
        dfm = dfs.merge(dfe, on='case:concept:name')
        dfm['case:duration'] = dfm.apply(lambda row: row['timestamp:end'] - row['timestamp:start'], axis=1)
        dfm = dfm.rename(columns={
            'timestamp:start': 'case:timestamp:start',
            'timestamp:end': 'case:timestamp:end',
        })
        return dfm

    def filter_best_flops(self):
        """returns case and event table corresponding to min flop instances"""
        best_flops_case = self.case_table[self.case_table['case:flops'] == self.case_table['case:flops'].min()]
        filter_algs = best_flops_case['case:concept:name'].values
        best_flops_events = self.event_table.loc[self.event_table['case:concept:name'].isin(filter_algs)]
        return (best_flops_case, best_flops_events)

    def filter_worst_flops(self):
        """returns case and event table corresponding to max flop instances"""
        worst_flops_case = self.case_table[self.case_table['case:flops'] == self.case_table['case:flops'].max()]
        filter_algs = worst_flops_case['case:concept:name'].values
        worst_flops_events = self.event_table.loc[self.event_table['case:concept:name'].isin(filter_algs)]
        return (worst_flops_case, worst_flops_events)

    def filter_best_duration(self):
        """returns case and event table corresponding to min duration instances"""
        best_duration_case = self.case_table[self.case_table['case:duration'] == self.case_table['case:duration'].min()]
        filter_algs = best_duration_case['case:concept:name'].values
        best_duration_events = self.event_table.loc[self.event_table['case:concept:name'].isin(filter_algs)]
        return (best_duration_case, best_duration_events)

    def filter_best_flops_duration(self):
        """returns case and event table corresponding to min flop and min duration instances
        This function appends 'case:rel-flops' (relative flops: flop-min_flop) and
        'case:rel-duration' (relative duration: duration - min_duration) to the returned case table.

        if case:rel-flops = case:rel-duration = 0, then minimum flops implies minimum duration.

        """

        best_flops_case = self.case_table[self.case_table['case:flops'] == self.case_table['case:flops'].min()]
        best_duration_case = self.case_table[self.case_table['case:duration'] == self.case_table['case:duration'].min()]
        df = pd.concat([best_flops_case, best_duration_case]).drop_duplicates('case:concept:name')

        min_flop = best_flops_case['case:flops'].values[0]
        df['case:rel-flops'] = df.apply(lambda row: row['case:flops'] - min_flop, axis=1)

        min_duration = best_duration_case['case:duration'].values[0]
        df['case:rel-duration'] = df.apply(lambda row: row['case:duration'] - min_duration, axis=1)

        filter_algs = df['case:concept:name'].values
        df_events = self.event_table.loc[self.event_table['case:concept:name'].isin(filter_algs)]

        return (df, df_events)

    def clear_tables(self):
        self.case_table = None
        self.event_table = None

