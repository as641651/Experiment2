from datetime import datetime
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer

def convert_timestamp_todtime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')

def convert_timestamp_format(df):
    df['timestamp:start'] = df['timestamp:start'].apply(convert_timestamp_todtime)
    df['timestamp:end'] = df['timestamp:end'].apply(convert_timestamp_todtime)
    df = dataframe_utils.convert_timestamp_columns_in_df(df)


class DiscoverPN:
    """Creates an xes eventlog from the dataframes: case_table and event table
    The eventlog is used to discover process models"""

    def __init__(self, event_table, case_table=None):
        """INPUT: dataframes: case_table and event_table
            Upon initialization, the case and event tables are merged
            and converted to an xes event log format. The dataframes are not stored.
        """
        log = event_table.copy()
        convert_timestamp_format(log)
        log = log.sort_values('timestamp:start')
        if case_table:
            log = log.merge(case_table, on='case:concept:name')

        self.event_log = log_converter.apply(log)
        log = None

    def inductive_miner(self, activity='concept:name', filtered_log=None):
        """apply inductive mining on the filtered log.
        if no filtered_log is passed, self.event_log is used.

        Input (optional): event log
        Output: petrinet, initial marking, final marking"""

        log = self.event_log
        if filtered_log:
            log = filtered_log
        parameters = {
            inductive_miner.Variants.IM_CLEAN.value.Parameters.ACTIVITY_KEY: activity
        }
        return inductive_miner.apply(log, parameters=parameters)

    def visualize_pn(self, net, im, fm):
        """visualize petrinet
        Input: net, inital and final marking
        Returns nothing."""
        gviz = pn_visualizer.apply(net, im, fm)
        pn_visualizer.view(gviz)

