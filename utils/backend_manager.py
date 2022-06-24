from paramiko import SSHClient, AutoAddPolicy
import subprocess
import os


class BackendManager:
    def __init__(self, server, uname, submit_cmd=None):
        self.server = server
        self.uname = uname
        self.submit_cmd = submit_cmd

        self.interactive = True
        if self.submit_cmd:
            self.interactive = False

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.connected = False

    def connect(self):
        self.client.connect(self.server, username=self.uname)
        self.connected = True

    def close(self):
        self.client.close()
        self.connected = False

    def generate_experiments(self, expression_dir, args, threads):
        if self.connected:
            cmd = "source ~/.analyzer; "
            cmd += "cd {}; ".format(expression_dir)
            cmd += "python generate-variants-linnea.py {} --threads={};".format(" ".join(args), threads)

            print(cmd)

            _, stdout, _ = self.client.exec_command(cmd)

            ret = stdout.readlines()
            print(ret)
            if "Generated Variants" in ret[-1]:
                return 0
            else:
                return 1
        else:
            return -1

    def check_if_file_exists(self, file_path):
        if self.connected:
            cmd = "test -f {};".format(file_path)
            _, stdout, _ = self.client.exec_command(cmd)
            ret = stdout.channel.recv_exit_status()
            if stdout.channel.recv_exit_status() == 0:
                return True
            return False
        return -1

    def run_julia_script(self, runner_file):
        if self.connected:
            args_dir, script = os.path.split(runner_file)

            cmd = "source ~/.analyzer; "
            cmd += "cd {}; ".format(args_dir)
            if self.interactive:
                cmd += "julia {};".format(script)
            else:
                cmd += "{} julia {};".format(self.submit_cmd, script)

            _, stdout, _ = self.client.exec_command(cmd)

            print(cmd)

            if stdout.channel.recv_exit_status() == 0:
                return 0
            print("Error: ", stdout.channel.recv_exit_status())
            return 1
        return -1

    def check_slrum_status(self, jobname):
        if self.connected:
            cmd = "squeue --format=\"%.18i %.9P %.30j %.8u %.8T %.10M %.9l %.6D %R\" --me"
            _, stdout, _ = self.client.exec_command(cmd)
            ret = stdout.readlines()
            for j in ret:
                if jobname in j.split():
                    print(j)
                    return 2

            print(ret)
            return 0

    def copy_from_backend(self, backend_path, local_path):
        call = 'scp {uname}@{server}:{backend_path} {local_path}'.format(uname=self.uname,
                                                                         server=self.server,
                                                                         backend_path=backend_path,
                                                                         local_path=local_path)
        print(call)
        try:
            ret = subprocess.check_output(call.split())
            print(ret)
            return 0
        except Exception as e:
            print(e)
            return 1

    def run_python_script(self, script_file, cmd_args, args_dir, submit=False):
        if self.connected:
            cmd = "source ~/.analyzer; "
            cmd += "cd {}; ".format(args_dir)
            if not submit or self.interactive:
                cmd += "python {} {}".format(script_file, cmd_args)
            else:
                cmd += "{} python '{} {}'".format(self.submit_cmd, script_file, cmd_args)
            print(cmd)

            _, stdout, _ = self.client.exec_command(cmd)

            # print(stdout.readlines())
            if stdout.channel.recv_exit_status() == 0:
                return 0
            print("Error: ", stdout.channel.recv_exit_status())
            return 1

        return -1

    def cancel_job(self, job_name):
        pass

    def run_cmd(self, cmd):
        if self.connected:
            print(cmd)
            _, stdout, _ = self.client.exec_command(cmd)

            if stdout.channel.recv_exit_status() == 0:
                return 0
            print("Error: ", stdout.channel.recv_exit_status())
            return 1

        return -1

    def debug_cmd(self, cmd):
        call = 'ssh -l {} {}'.format(self.uname, self.server).split()
        ret = subprocess.check_output(call + [cmd, ])
        print(ret)

