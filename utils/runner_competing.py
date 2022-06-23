import os
import subprocess


class RunnerCompeting:
    def __init__(self, competing_variants, args_dir, threads=4, backend=None):
        self.competing_variants = competing_variants
        self.args_dir = args_dir
        self.threads = threads
        self.backend = backend

    def measure_competing_variants(self, run_id, reps):
        cmd_args = "--algs {algs} --rep {rep} --threads {threads} --id {run_id}".format(
            algs=" ".join(self.competing_variants),
            rep=reps,
            threads=self.threads,
            run_id=run_id)

        script_file = "generate-measurements-script.py"
        runner_file = os.path.join(self.args_dir, "runner_competing_{}.jl".format(run_id))

        if self.backend:
            ret = self.backend.run_python_script(script_file, cmd_args, self.args_dir)
            if ret != 0:
                return 3

            ret = self.backend.run_julia_script(runner_file)
            if ret == 0:
                print("Running experiments in the backend.")
                return 0

            return ret
        else:
            call = ["python", os.path.join(self.args_dir, script_file)] + cmd_args.split()
            completed_proccess = subprocess.run(call)
            ret = completed_proccess.returncode
            if ret == 0:
                print("Running experiments locally.")
                call = ["julia", runner_file]
                completed_proccess = subprocess.run(call)
                ret = completed_proccess.returncode
                if ret == 0:
                    print("Experiments completed locally")

            return ret

        return -1

    def compute_ranks(self, rep_steps=3, eps=0.001):
        cmd_args = "--rep_steps {rep_steps} --eps {eps} --threads {threads} --algs {algs}".format(rep_steps=rep_steps,
                                                                                                  eps=eps,
                                                                                                  threads=self.threads,
                                                                                                  algs=" ".join(
                                                                                                      self.competing_variants))
        script_file = "compute-ranks.py"

        if self.backend:
            ret = self.backend.run_python_script(script_file, cmd_args, self.args_dir, submit=True)
            if ret != 0:
                return 3
            print("Submitted experiment to backend.")
            return ret
        else:
            call = ["python", os.path.join(self.args_dir, script_file)] + cmd_args.split()
            completed_proccess = subprocess.run(call)
            ret = completed_proccess.returncode
            return ret




