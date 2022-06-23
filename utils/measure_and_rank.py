import pandas as pd
from case_duration_manager import CaseDurationsManager
from rank_variants import RankVariants
import numpy as np

def measure_and_rank(runner_competing, data_collector, alg_seq_h0, rep_steps=3, eps=0.001):
    num_measurements = 0
    run_id = 0
    cm = CaseDurationsManager()

    data = []
    for i, j in enumerate(alg_seq_h0):
        data.append([j, i])
    mean_rank_h0 = pd.DataFrame(data, columns=['case:concept:name', 'case:mean-rank'])
    mean_rank_log = []
    mean_rank_log.append(mean_rank_h0.set_index('case:concept:name'))

    norm = 1
    while norm > eps:

        ret = runner_competing.measure_competing_variants(run_id=run_id, reps=rep_steps)

        if ret != 0:
            return ret

        measurements = data_collector.get_runtimes_competing_table(run_id)
        cm.add_case_durations(measurements)

        rank_variants = RankVariants(cm.get_alg_measurements(), alg_seq_h0)
        _, mean_rank_h1 = rank_variants.calculate_mean_rank()

        print(mean_rank_h1)

        df = mean_rank_h1.merge(mean_rank_h0, on=['case:concept:name'])
        x = df.iloc[:, -1].values
        y = df.iloc[:, -2].values
        norm = np.linalg.norm(x - y)
        print("norm: {}".format(norm))

        mean_rank_h0 = mean_rank_h1.copy()
        mean_rank_log.append(mean_rank_h0.set_index('case:concept:name'))

        alg_seq_h0 = list(mean_rank_h0['case:concept:name'])

        run_id = run_id + 1

    num_measurements = (run_id) * rep_steps
    print("Number of measurements: {}".format(num_measurements))

    return rank_variants, cm, pd.concat(mean_rank_log, axis=1)
