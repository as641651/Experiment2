import os
import subprocess
import pandas as pd
import shutil


class Runner:
    def __init__(self, name, expression_dir, args, threads=4, backend=None):
        """
        This class handles the code generation and execution of the variant codes.
        The generated event data can be obtained as a pandas dataframe.

        Requirements:

        It is assumed that there exists a script file that generates variant codes
        for a given oopoerand sizes. The operand sizes are input as command line args
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
        self.expression_dir = expression_dir
        self.threads = threads

        self.script_path = os.path.join(self.expression_dir, "generate-variants-linnea.py")
        self.args = args
        self.args_dir = os.path.join(self.expression_dir,
                                     "experiments",
                                     "_".join(self.args))

        self.backend = backend

    def generate_experiments(self):
        """
        generates experiments for a given set of valid arguments
        that can be given as input to the script file.
            e.g. in,  python generate.py 10 10 10 10 12
            ['10','10','10','10','12'] would be the argument list.

        Output: Return code == 0 implies successful completion
        """

        if not self.backend:
            call = ["python", self.script_path] + self.args + ["--threads={}".format(self.threads)]
            completed_proccess = subprocess.run(call)
            ret = completed_proccess.returncode
        else:
            ret = self.backend.generate_experiments(self.expression_dir, self.args, self.threads)

        return ret

    def run_experiments(self):
        """
        executes the runner file, which generates run_times.txt
        """
        runner_path = os.path.join(self.args_dir, "runner.jl")
        if not self.backend:
            if os.path.exists(self.args_dir):
                print("Running Experiments locally")
                completed_proccess = subprocess.run(["julia", runner_path])
                if completed_proccess.returncode == 0:
                    print("Experiments completed locally")
                    return 0  # Ran experiment
        else:
            ret = self.backend.run_julia_script(runner_path)
            if ret == 0:
                print("Running experiments in the backend.")
                return 0

        return -1

    def clean(self):
        """remove arguments folder"""
        if os.path.exists(self.args_dir):
            shutil.rmtree(self.args_dir)
        else:
            return -1

