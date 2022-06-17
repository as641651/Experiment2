import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter


class RankVariants:
    def __init__(self, measurements, alg_list):
        self.measurements = {}
        self.alg_list = alg_list
        # self.alg_list.sort()
        for alg in alg_list:
            t_alg = measurements[measurements.apply(
                lambda x: x['case:concept:name'].split('_')[0] == alg, axis=1)]
            self.measurements[alg] = list(t_alg['case:duration'])

        self.comparision_matrix = {}
        self.init_comparision_matrix()

    def init_comparision_matrix(self):
        self.comparision_matrix = {}
        for alg in self.alg_list:
            self.comparision_matrix[alg] = {}
            for alg2 in self.alg_list:
                self.comparision_matrix[alg][alg2] = -1

    def get_measurements(self, alg):
        return self.measurements[alg]

    def get_quartiles(self, measurements, q_max=75, q_min=25):
        return np.percentile(measurements, [q_max, q_min])

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

        p = len(self.alg_list)

        r = np.array([i for i in range(p)])
        s = np.array([i for i in range(p)])

        algs = {}
        for i in range(p):
            algs[s[i]] = self.alg_list[i]

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

        columns = ['case:concept:name', 'case:rank']

        return pd.DataFrame([(algs[s[i]], r[i]) for i in range(p)], columns=columns)

    def calculate_ranks_old(self):
        q_max = 99
        q_min = 0
        ranks = []
        for q in np.linspace(q_min, q_max, 10):
            ranks.append(self.sortAlgs(q, q_min).set_index('case:concept:name'))

        return pd.concat(ranks, axis=1)

    def calculate_ranks(self):
        q_maxs = [95, 90, 85, 80, 75, 70, 65]
        q_mins = [5, 10, 15, 20, 25, 30, 35]
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

    def show_measurement_histograms(self, alg_list=None, bins=10, hspace=0.5):
        if not alg_list:
            alg_list = self.alg_list
        alg_list.sort()

        n = len(alg_list)
        fig = plt.figure(figsize=(7, 3 * n))
        gs = gridspec.GridSpec(n, 1, height_ratios=[1] * n)

        ax = [None] * n
        for i in range(n):
            if i != 0:
                ax[i] = plt.subplot(gs[i], sharex=ax[0])
            else:
                ax[i] = plt.subplot(gs[i])
            ax[i].set_title(alg_list[i])
            ax[i].hist(self.measurements[alg_list[i]], bins=bins)
            ax[i].xaxis.set_major_formatter(FormatStrFormatter('%.e'))

        plt.subplots_adjust(hspace=hspace)
        plt.show()

    def show_measurements_boxplots(self, alg_list=None, outliers=False):
        if not alg_list:
            alg_list = self.alg_list
        # alg_list.sort()

        x = []
        y = []
        for alg in alg_list:
            x.append(self.measurements[alg])
            y.append(alg)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111)

        # # Creating axes instance
        bp = ax.boxplot(x, patch_artist=True,
                        notch=False, vert=0, showfliers=outliers,
                        positions=range(len(y)))

        x_lim = ax.get_xlim()

        try:
            sp = ax.plot(x, y, 'b.', alpha=0.9)
            ax.set_xlim(x_lim)
        except:
            pass

        colors = ['#E1E8E8'] * len(y)

        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        # changing color and linewidth of
        # whiskers
        for whisker in bp['whiskers']:
            whisker.set(color='#8B008B',
                        linewidth=1.5,
                        linestyle=":")

        # changing color and linewidth of
        # caps
        for cap in bp['caps']:
            cap.set(color='#8B008B',
                    linewidth=2)

        # changing color and linewidth of
        # medians
        for median in bp['medians']:
            median.set(color='red',
                       linewidth=2)

        # y-axis labels
        ax.set_yticklabels(y)

        # Removing top axes and right axes
        # ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        plt.show()






