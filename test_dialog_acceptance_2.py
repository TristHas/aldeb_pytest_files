# -*- encoding: UTF-8 -*-
""" ALDialog API test (automatic)
"""

__author__ = "thascoet"
__copyright__ = "Copyright September 2015, Aldebaran Robotics"


from functionaltools.cloudfixture_2 import *
from log_handler import log_viewer
from bench_dialog import RemoteCPUWatch

from qi import Session, logging
from functionaltools import ssh_tools
from qi import Session

import time


# Missing fixtures for associating the good profiles
###
### Model Performance
###
def test_compile_with_life(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store('test_compile_with_life')
    cpu.start_display()
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s.service('ALDialog')
    print "======================================="
    print "     Compiling ..."
    print "=======================================\n"
    logs.dump_logs('test_compile_with_life')
    dialog._preloadMain()
    cpu.stop_store()
    cpu.stop_display()
    logs.dump_logs('test_compile_with_life')
    print "======================================="
    print "     Log Results:"
    print " | Load time = {} s".format(logs.get_load_time())
    print " | Main Dialog total compile time = {} s".format(logs.get_bundle_compile_time('welcome'))
    print " | Main Dialog model compile time = {} s".format(logs.get_model_compile_time('welcome'))
    print " | Main Dialog Japanese reco compile time = {} s".format(logs.get_reco_compile_time('welcome', 'Japanese'))
    print " | Main Dialog English reco compile time = {} s".format(logs.get_reco_compile_time('welcome', 'English'))
    print "=======================================\n"

    print "======================================="
    print "     CPU Results:"
    print " | Virtual Memory RSS difference  = {}".format(cpu.get_naoqiservice_VmRSS_diff())
    print " | Virtual Memory Size difference = {}".format(cpu.get_naoqiservice_VmSize_diff())
    print " | Maximum 1 minute load average  = {}".format(cpu.get_cpu_lavg1_max())
    print " | Average IO time                = {}".format( cpu.get_cpu_iotime_mean())
    print " | Total Majflt                   = {}".format(cpu.get_cpu_majflt_sum())
    print " | Average system time            = {}".format(cpu.get_naoqiservice_stime_mean())
    print " | Average user time              = {}".format(cpu.get_naoqiservice_utime_mean())
    print "=======================================\n"


####
####    Precompile behavior
####


####
####    Correct error detection
####


####
####    Content
####

# For all client configuartion:
# No error at topic loading
# Check compilation time. fix a threshold



def non_compile_with_life_2(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    cpu.stop_store()
    cpu.stop_display()
    dialog.stopDialog()
    assert True

def non_compile_with_life_3(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    cpu.stop_store()
    cpu.stop_display()
    dialog.stopDialog()
    assert True


def non_compile_with_life_4(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    cpu.stop_store()
    cpu.stop_display()
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    dialog.stopDialog()

    assert True


def non_compile_with_life_5(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    cpu.stop_store()
    cpu.stop_display()
    dialog.stopDialog()
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    assert True

def non_compile_with_life_6(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    cpu.stop_store()
    cpu.stop_display()
    dialog.stopDialog()
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    assert True

def non_compile_with_life_7(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    cpu.stop_store()
    cpu.stop_display()
    dialog.stopDialog()
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    assert True


def non_compile_with_life_6(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    cpu.stop_store()
    cpu.stop_display()
    dialog.stopDialog()
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    assert True


def non_compile_with_life_7(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    cpu.stop_store()
    cpu.stop_display()
    dialog.stopDialog()
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    assert True


def nontest_compile_with_life_8(set_no_life, force_compilation, restart_naoqi, cpu_server):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    cpu = RemoteCPUWatch(ssh_tools.get_ip())
    cpu.start_store()
    cpu.start_display()
    print cpu.files
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s. service('ALDialog')
    dialog.runDialog()
    print 'Has run dialog'
    cpu.stop_store()
    cpu.stop_display()
    dialog.stopDialog()
    print "======================================="
    print "     Result = " + str(logs.get_compile_result())
    print "======================================="
    assert True
