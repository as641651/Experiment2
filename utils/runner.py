import os
import subprocess
import pandas as pd
import shutil


class Runner:
    def __init__(self, name, script_path, args):
        """
        This class handles the code generation and execution of the variant codes.
        The generated event data can be obtained as a pandas dataframe.

        Requirements:

        It is assumed that there exists a script file that generates variant codes
        for a given opoerand sizes. The operand sizes are input as command line args
            e.g. run of script file: python generate.py 10 10 10 10 12

        After running the script file, inside the folder "experiments", which is in
        the same directory as the script file, an "argument folder" is generated,
        which contains the case_table, event_meta_table (i.e, the event table without actual run times)
        ,and a runner script as shown in the expample below:
            e.g. experiment/10_10_10_10_12/
                    case_table.csv
                    event_meta_table.csv
                    runner.jl

        'runner.jl' is the script that runs the experiments and generates a log file 'run_times.txt' (which is the
        event table with actual run times) in the "arguments folder"


        INPUT:

        name: Experiment name
        script_path: Path to the script file that generates variants
        args: operand sizes (or arguments to the script file)

        USECASE:
        If the behavior of the script is as said in the requirements, this class can
        call the scipt file and collects the eventlogs as a pandas dataframe, and
        if needed, can also clean the generated folders.

        """
        self.name = name
        self.script_path = script_path
        self.script_dir = os.path.dirname(self.script_path)
        self.args = args
        self.call = ["python", self.script_path] + self.args
        self.exp_dir = os.path.join(self.script_dir,
                                    "experiments",
                                    "_".join(self.args))

    def generate_run_experiments(self, bRun=True, bGenerate=True):
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

        if bGenerate:
            completed_proccess = subprocess.run(self.call)
            if completed_proccess.returncode == 0:
                if bRun:
                    # Generate and run
                    return self.run_experiments()
                else:
                    return 2  # only Generate
            else:
                return -1
        elif bRun:
            # Run without generating
            if os.path.exists(self.exp_dir):
                return self.run_experiments()
        return -1

    def run_experiments(self):
        """
        executes the runner file, which generates run_times.txt
        """
        runner_path = os.path.join(self.exp_dir, "runner.jl")

        if os.path.exists(runner_path):
            print("Running Experiments")
            completed_proccess = subprocess.run(["julia", runner_path])
            if completed_proccess.returncode == 0:
                print("Experiments completed")
                return 1  # Ran experiment
        return -1

    def get_case_table(self):
        """get case table"""
        if os.path.exists(self.exp_dir):
            return self.read_log(os.path.join(self.exp_dir, "case_table.csv"))
        return -1

    def get_event_meta_table(self):
        """get event table without actual execution times."""
        if os.path.exists(self.exp_dir):
            return self.read_log(os.path.join(self.exp_dir, "event_meta_table.csv"))
        return -1

    def get_event_runtime_table(self):
        """get event table with actual execution times."""
        if os.path.exists(self.exp_dir):
            return self.read_log(os.path.join(self.exp_dir, "run_times.txt"))
        return -1

    def get_all_tables(self, meta=True):
        """get all tables"""
        case_table = self.get_case_table()
        event_meta_table = None
        if meta:
            event_meta_table = self.get_event_meta_table()
        event_runtime_table = self.get_event_runtime_table()
        return (case_table, event_meta_table, event_runtime_table)

    def read_log(self, log_path):
        if os.path.exists(log_path):
            df = pd.read_csv(log_path, sep=';')
            return df
        return -1

    def isGenerated(self):
        if os.path.exists(self.exp_dir):
            return True
        return False

    def isRun(self):
        if os.path.exists(os.path.join(self.exp_dir, "run_times.txt")):
            return True
        return False

    def clean(self):
        """remove arguments folder"""
        if os.path.exists(self.exp_dir):
            shutil.rmtree(self.exp_dir)
        else:
            return -1

