import random
import numpy as np
import pandas as pd

class RankVariants:
    def __init__(self, alg_measurements, alg_seq_h0):
        self.measurements = alg_measurements
        self.alg_seq_h0 = alg_seq_h0

        self.comparision_matrix = {}
        self.init_comparision_matrix()

    def init_comparision_matrix(self):
        self.comparision_matrix = {}
        for alg in self.alg_seq_h0:
            self.comparision_matrix[alg] = {}
            for alg2 in self.alg_seq_h0:
                self.comparision_matrix[alg][alg2] = -1

    def get_measurements(self, alg):
        return self.measurements[alg]

    def remove_outliers(self, x):
        x = np.array(x)
        q1, q2 = np.percentile(x,  [25,75])
        iqr = q2-q1
        fence_low = q1 - 1.5*iqr
        fence_high = q2 + 1.5*iqr
        return x[(x>fence_low) & (x <fence_high)]

    def get_quartiles(self, measurements, q_max=75, q_min=25):
        return np.percentile(self.remove_outliers(measurements), [q_max, q_min])

    def compareAlgs(self, alg1, alg2, q_max=75, q_min=25):
        #print(alg1, alg2)
        if self.comparision_matrix[alg1][alg2] != -1:
            return self.comparision_matrix[alg1][alg2]

        t_alg1 = self.get_measurements(alg1)
        t_alg2 = self.get_measurements(alg2)

        q1_max, q1_min = self.get_quartiles(t_alg1, q_max, q_min)
        q2_max, q2_min = self.get_quartiles(t_alg2, q_max, q_min)
        # print(alg1, q1_max, q1_min)
        # print(alg2, q2_max, q2_min)

        ret = 1  # alg1 ~ alg2
        if q1_max < q2_min:
            ret = 0  # alg1 is faster than alg2
        elif q2_max < q1_min:
            ret = 2  # alg2 is faster than alg1

        self.comparision_matrix[alg1][alg2] = ret
        if ret == 0:
            self.comparision_matrix[alg2][alg1] = 2
        elif ret == 2:
            self.comparision_matrix[alg2][alg1] = 0
        else:
            self.comparision_matrix[alg2][alg1] = ret

        #print(ret)
        #print("\n")
        return ret

    def sortAlgs(self, q_max=75, q_min=25):
        self.init_comparision_matrix()

        p = len(self.alg_seq_h0)

        r = np.array([i for i in range(p)])
        s = np.array([i for i in range(p)])

        algs = {}
        for i in range(p):
            algs[s[i]] = self.alg_seq_h0[i]

        for i in range(p):
            for j in range(0, p - i - 1):

                # ret = self.compareAlgs(algs[s[j]], algs[s[j+1]], threshold, M, K)
                ret = self.compareAlgs(algs[s[j]], algs[s[j + 1]], q_max, q_min)

                # if alg j+1 is faster than alg j
                if ret == 2:
                    # swap index
                    s[j], s[j + 1] = s[j + 1], s[j]

                    # update rank
                    if r[j + 1] == r[j]:
                        if j == 0:
                            r[j + 1:] = r[j + 1:] + 1
                        elif r[j - 1] != r[j]:
                            r[j + 1:] = r[j + 1:] + 1

                    else:
                        if j != 0 and r[j - 1] != r[j]:
                            r[j + 1:] = r[j + 1:] - 1

                # alg j+1 is as good as alg j
                if ret == 1:
                    # update rank
                    if r[j + 1] != r[j]:
                        r[j + 1:] = r[j + 1:] - 1

        columns = ['case:concept:name', 'case:rank:q{}-q{}'.format(int(q_max),int(q_min))]

        return pd.DataFrame([(algs[s[i]], r[i]) for i in range(p)], columns=columns)


    def calculate_ranks(self):
        q_maxs = [95, 90, 85, 80, 75, 70, 65, 55]
        q_mins = [5, 10, 15, 20, 25, 30, 35, 45]
        ranks = []
        for q_max, q_min in zip(q_maxs, q_mins):
            ranks.append(self.sortAlgs(q_max, q_min).set_index('case:concept:name'))

        return pd.concat(ranks, axis=1)

    def calculate_roc(self):

        df_ranks = self.calculate_ranks()
        max_rank = df_ranks.max().max()
        if max_rank == 0:
            max_rank = 1
        x = df_ranks.apply(lambda x: x * (1. / len(df_ranks.columns))).sum(axis=1) / (max_rank)
        df_roc = pd.DataFrame(x)
        df_roc = df_roc.reset_index()
        df_roc = df_roc.rename(columns={0: 'case:roc'})

        df_roc.sort_values(by=['case:roc'], inplace=True)
        return df_ranks, df_roc

    def calculate_mean_rank(self):

        df_ranks = self.calculate_ranks()

        x = df_ranks.sum(axis=1) / float(len(df_ranks.columns))
        df_mean = pd.DataFrame(x)
        df_mean = df_mean.reset_index()
        df_mean = df_mean.rename(columns={0: 'case:mean-rank'})

        df_mean.sort_values(by=['case:mean-rank'], inplace=True)
        return df_ranks, df_mean
