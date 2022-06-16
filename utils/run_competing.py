from filter_variants import FilterVariants
from generate_linnea_experiment_code import generate_runner_competing_code
import os
import subprocess
from project_utils import get_trace_durations


class RunCompeting:
    """Runs all the variants once and selects a set of competing variants.
    Each of the competing variant is measured "rep" times, and the tables are
    prepa`red for analysis."""

    def __init__(self, runner):
        """
        Input: Runner
        """
        self.runner = runner
        self.filter_variants = None
        self.competing_variants = None
        self.event_table_competing = None
        self.durations_competing = None

    def generate_run(self, bRun=True, bGenerate=False):
        """
        executes the Runner. Intializes FilterVariants object.
        """
        ret = self.runner.generate_run_experiments(bRun=bRun, bGenerate=bGenerate)
        case_table, _, event_table = self.runner.get_all_tables(meta=False)
        self.filter_variants = FilterVariants(case_table, event_table)
        return ret

    def set_best_flop_duration_as_competing(self, tolerance=0.0):
        """
        Filters for variants that have the minimum flop and also those variants
        with more flops but duration within a certain tolerance level from the variant
        with minimum duration.
        """
        if not self.filter_variants:
            return "Please generate a run."

        competing_ct, _ = self.filter_variants.filter_best_flops_duration()
        self.competing_variants = list(competing_ct['case:concept:name'])
        return competing_ct

    def measure_competing_variants(self, reps):
        """
        generates a runner code for comopeting variants. Measures the competing variants.
        """
        if not self.competing_variants:
            return "Please set competing variants."

        ret = generate_runner_competing_code(self.competing_variants,
                                             reps,
                                             self.runner.exp_dir)

        runner_path = os.path.join(self.runner.exp_dir, "runner_competing.jl")

        if os.path.exists(runner_path):
            print("Running Experiments")
            completed_proccess = subprocess.run(["julia", runner_path])
            if completed_proccess.returncode == 0:
                print("Experiments completed")
                return 1  # Ran experiment
        return -1

    def prepare_event_data(self):
        """get event table for the measured variants."""
        log_path = os.path.join(self.runner.exp_dir, "run_times_competing.txt")
        if os.path.exists(log_path):
            self.event_table_competing = self.runner.read_log(log_path)
            self.duration_competing = get_trace_durations(self.event_table_competing)
            return 1
        return "please measure competing variants."

    def get_variant_duration(self, variant):
        """Compute duration for each measurement of the competing variants."""
        if not variant in self.competing_variants:
            return "variant not found in competing variants."

        return self.duration_competing[
            self.duration_competing['case:concept:name'].str.contains(variant)]




