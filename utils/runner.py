import os
import subprocess
import pandas as pd
import shutil


class Runner:
    """
    This class handles the code generation and execution of the variant codes.
    The generated event data can be obtained as a pandas dataframe.

    Requirements:

    It is assumed that there exists a script file that generates variant codes.
    The script file can take command line arguments;
        e.g. run of script file: python generate.py 10 10 10 10 12

    After running the script file, inside the folder "experiments", which is in
    the same directory as the script file, an "argument folder" is generated,
    which contains the files shown in the expample below:
        e.g. experiment/10_10_10_10_12/
                case_table.csv
                event_meta_table.csv
                runner.jl

    'runner.jl' is the script that runs the experiments and generates a log file 'run_times.txt' in the
    "arguments folder"
    """
    def __init__(self, name, script_path, num_args):
        """
        INPUT:

        name: Experiment name
        script_path: Path to the script file that generates variants

        USECASE:
        If the behavior of the script is as said in the requirements, this class can
        call the scipt file and collects the eventlogs as a pandas dataframe, and
        if needed, can also clean the generated folders.
        """

        self.name = name
        self.script_path = script_path
        self.script_dir = os.path.dirname(self.script_path)
        self.call = ["python", self.script_path]
        self.num_args = num_args

    def get_exp_dir(self, args_list):
        return os.path.join(self.script_dir,
                            "experiments",
                            "_".join(args_list))

    def generate_run_experiments(self, args_list, bRun=True, bGenerate=True):
        """
        generates and run experiments for a given set of valid arguments
        that can be given as input to the script file.
            e.g. in,  python generate.py 10 10 10 10 12
            ['10','10','10','10','12'] would be the argument list.


        optional args:
            bGenerate: Runs the script file if set to True. The "argument folder"
                is re-generated.

            bRun: if set to False, it is assumed that the "argument folder"
            has been already generated.

        """
        exp_dir = self.get_exp_dir(args_list)

        if bGenerate:
            completed_proccess = subprocess.run(self.call + args_list)
            if completed_proccess.returncode == 0:
                if bRun:
                    # Generate and run
                    return self.run_experiments(exp_dir)
                else:
                    return 2  # only Generate
            else:
                return -1
        elif bRun:
            # Run without generating
            if os.path.exists(exp_dir):
                return self.run_experiments(exp_dir)
        return -1

    def run_experiments(self, exp_dir):
        """
        executes the runner file, which generates run_times.txt
        """
        runner_path = os.path.join(exp_dir, "runner.jl")

        if os.path.exists(runner_path):
            print("Running Experiments")
            completed_proccess = subprocess.run(["julia", runner_path])
            if completed_proccess.returncode == 0:
                print("Experiments completed")
                return 1  # Ran experiment
        return -1

    def get_case_table(self, exp_dir):
        """get case table"""
        if os.path.exists(exp_dir):
            return self.read_log(os.path.join(exp_dir, "case_table.csv"))
        return -1

    def get_event_meta_table(self, exp_dir):
        """get event table without actual execution times."""
        if os.path.exists(exp_dir):
            return self.read_log(os.path.join(exp_dir, "event_meta_table.csv"))
        return -1

    def get_event_runtime_table(self, exp_dir):
        """get event table with actual execution times."""
        if os.path.exists(exp_dir):
            return self.read_log(os.path.join(exp_dir, "run_times.txt"))
        return -1

    def get_all_tables(self, exp_dir, meta=True):
        """get all tables"""
        case_table = self.get_case_table(exp_dir)
        event_meta_table = None
        if meta:
            event_meta_table = self.get_event_meta_table(exp_dir)
        event_runtime_table = self.get_event_runtime_table(exp_dir)
        return (case_table, event_meta_table, event_runtime_table)

    def read_log(self, log_path):
        if os.path.exists(log_path):
            df = pd.read_csv(log_path, sep=';')
            return df
        return -1

    def isGenerated(self, args_list):
        exp_dir = self.get_exp_dir(args_list)
        if os.path.exists(exp_dir):
            return True
        return False

    def isRun(self, args_list):
        exp_dir = self.get_exp_dir(args_list)
        if os.path.exists(os.path.join(exp_dir, "run_times.txt")):
            return True
        return False

    def clean(self, args_list):
        """remove arguments folder"""
        exp_dir = self.get_exp_dir(args_list)
        if os.path.exists(exp_dir):
            shutil.rmtree(exp_dir)
        else:
            return -1

