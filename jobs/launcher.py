from flask_script import Command
import sys, argparse, traceback, importlib

"""
job统一入口文件
"""

class RunJob(Command):

    capture_all_args=True
    def run(self, *args, **kwargs):
        # print(sys.argv)
        args = sys.argv[2:]
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument("-m", "--name", dest="name", metavar="name", help="指定job名", required=True)
        parser.add_argument("-a", "--act", dest="act", metavar="act", help="job动作", required=False)
        parser.add_argument("-p", "--params", dest="params", nargs="*", metavar="params", help="业务参数", required=False)
        params = parser.parse_known_args(args)
        # print(params)
        params_dict = params[0].__dict__
        if "name" not in params_dict or not params_dict["name"]:
            return self.tips()
        # print(params_dict)

        try:
            """
            from jobs.tasks.test import JobTask
            """
            module_name = params_dict["name"].replace("/",".")
            import_str = f"jobs.tasks.{module_name}"
            target = importlib.import_module(import_str)
            exit(target.JobTask().run(params_dict))
        except Exception:
            traceback.print_exc()
        return

    def tips(self):
        tip_msg = """
        请正确的调度job
        manager.py runjob -m Test   注释：(jobs/tasks/Test.py)
        manager.py runjob -m test/index   注释：(jobs/tasks/test/index.py)
        """
        print(tip_msg)
        return

