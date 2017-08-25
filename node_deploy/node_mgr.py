# from transitions.extensions import LockedHierarchicalGraphMachine as Machine
from transitions import Machine
from django.db.models.signals import post_init
from django.dispatch import receiver
from transitions.extensions import GraphMachine
from IPython.display import Image, display, display_png
from node_checker import NodeChecker
from deploy_tool import DeployTool
from node_logger import NodeLogger
from threading import Timer
import time
# from transitions.extensions.states import add_state_features, Error, Timeout, Tags

class NodeMgr():
    @staticmethod
    def create_node(parm):
        checker = NodeChecker()
        logger = NodeLogger()
        deploy_tool = DeployTool()
        print("create_node")
        return HostNode(checker, logger, deploy_tool)

# @add_state_features(Error, Timeout, Tags)
# class CustomStateMachine(Machine):
#     pass

class HostNode():

    def __init__(self, name):
        self.node_status = False
        self.deploy_status = False
        self.config_status = False
        states = [
            'new',
            'deploy_ready',
            'deploy_done',
            'pre_check_fail',
            'deploy_fail',
            'post_check_fail',
            'success',
            'fail'
        ]
        transitions = [
            {'trigger': 'pre_check', 'source': 'new', 'dest': 'deploy_ready', 'conditions': 'is_node_ok',
             'prepare': 'run_pre_check', 'after':'node_deploy'},
            {'trigger': 'pre_check', 'source': 'new', 'dest': 'pre_check_fail',
             'prepare': 'run_pre_check', 'unless':['is_node_ok'], 'after':'retry1'},
            {'trigger': 'retry1', 'source': 'pre_check_fail', 'dest': 'deploy_ready', 'conditions': 'is_retry1_ok',
             'prepare': 'run_pre_check', 'after':'node_deploy'},
            {'trigger': 'retry1', 'source': 'pre_check_fail', 'dest': 'fail', 'unless': ['is_retry1_ok'],
             'prepare': 'run_pre_check'},
            {'trigger': 'node_deploy', 'source': 'deploy_ready', 'dest': 'deploy_done', 'prepare': 'run_deploy_node',
             'conditions': 'is_deploy_ok', 'after':'post_check'},
            {'trigger': 'node_deploy', 'source': 'deploy_ready', 'dest': 'deploy_fail', 'prepare': 'run_deploy_node',
             'unless': ['is_deploy_ok'], 'after':'retry2'},
            {'trigger': 'retry2', 'source': 'deploy_fail', 'dest': 'deploy_done', 'conditions': 'is_retry2_ok',
             'prepare': 'run_deploy_node'},
            {'trigger': 'retry2', 'source': 'deploy_fail', 'dest': 'fail', 'unless': ['is_retry2_ok'],
             'prepare': 'run_deploy_node', 'after':'run_fail_handler'},
            {'trigger': 'post_check', 'source': 'deploy_done', 'dest': 'success', 'prepare': 'run_post_check',
             'conditions': 'is_config_ok'},
            {'trigger': 'post_check', 'source': 'deploy_done', 'dest': 'fail', 'unless': ['is_config_ok']},
        ]

        # Initialize the state machine
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='new', queued=True,
                                          finalize_event='finalize', send_event=True)

        # CustomStateMachine.__init__(self, states=states, transitions=transitions, initial='new')
        # self.machine.add_transition('touch', ['liquid', 'gas', 'plasma'], '=', after='change_shape')

    def on_enter_deploy_ready(self, ev_data):
        print(ev_data)
        print("We've just entered state deploy_ready!, sleep 1s")

    def on_enter_fail(self, ev_data):
        print("on_enter_fail")

    def on_enter_success(self, ev_data):
        print("on_enter_fail")

    def raise_error(self, event): raise ValueError("Oh no")

    def finalize(self, ev_data):
        print("finalize")

    def check_fail(self, ev_data):
        print("check_fail")

    def is_node_ok(self, ev_data):
        print(self.node_status)
        return self.node_status

    def is_deploy_ok(self, ev_data):
        print(self.deploy_status)
        return self.deploy_status

    def is_config_ok(self, ev_data):
        print("is_config_valid")
        return self.config_status

    def run_pre_check(self, ev_data):
        print("run_pre_check")
        self.node_status = True

    def run_deploy_node(self, ev_data):
        print("node_deploy")
        self.deploy_status = True

    def run_post_check(self, ev_data):
        print("run_post_check")
        self.config_status = True

    def run_fail_handler(self, ev_data):
        print("run_fail_handler")


    def timer_func(self):
        print self.machine.state
        self.machine.cancel()
if __name__ == '__main__':
    thread{}
    batman = HostNode("Batman")
    print(batman.state)
    batman.start_deploy(123)
    batman.to_deploy_done()
    }
    batman.state
    print(batman.state)
    # batman.node_deploy()
    # print(batman.state)
    timer(timer_func)

    # time.sleep(2)
    # print(batman.state)
    # time.sleep(2)