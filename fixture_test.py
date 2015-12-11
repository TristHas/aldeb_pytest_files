#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functionaltools.cloudfixture_2 import *
from bench_dialog import RemoteCPUWatch
from qi import Session, logging
from functionaltools import ssh_tools
import time


NESTLE_BAYTRAIL_REFLEX_TIME = 10
NESTLE_BAYTRAIL_WELCOME_TIME = 3000
NESTLE_BAYTRAIL_REFLEX_TIME_NO_LIFE = 10
NESTLE_BAYTRAIL_WELCOME_TIME_NO_LIFE = 3000

SHOP_BAYTRAIL_REFLEX_TIME = 10
SHOP_BAYTRAIL_WELCOME_TIME = 3000
SHOP_BAYTRAIL_REFLEX_TIME_NO_LIFE = 10
SHOP_BAYTRAIL_WELCOME_TIME_NO_LIFE = 3000

set_precompile_dummy_profile = set_profile_Nestle   # Temporary. We just need a profile with relevant content to test precompile.
                                                    # Further discussion with David for potentially interesting content?


###
###     PART I: Loading and compilation
###


####    Compile Performance
# Watch time with logger
# Watch memory and cpu Load
# Configure so that minimum services are running on the robot


####    Correct precompile use
###     Client configuration content Validation

def test_compile_with_life(set_profile_Shopfor24, force_compilation, dialog, autonomous_life):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_compile()
    with RemoteCPUWatch(ssh_tools.get_ip()) as cpu:
        cpu.start_store()
        autonomous_life.setState("solitary")
        cpu.start_store()
        while logs.get_compile_result() is None:
            time.sleep(3)

    print "======================================="
    print "     Result = " + str(logs.get_precompile_result())
    print "======================================="

    #assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    #assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_001_001(set_profile_Shopfor20, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = autonomous_life.setState("solitary")
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < SHOP_ATOM_REFLEX_TIME
    assert logs["welcome 1"] < SHOP_ATOM_WELCOME_TIME

def test_toreplace_VALID_DIA_001_002(set_profile_Shopfor20, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < SHOP_ATOM_REFLEX_TIME
    assert logs["welcome 1"] < SHOP_ATOM_WELCOME_TIME

def test_toreplace_VALID_DIA_002_001(set_profile_Shopfor24, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = autonomous_life.setState("solitary")
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < SHOP_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < SHOP_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_002(set_profile_Shopfor24, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < SHOP_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < SHOP_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_003(set_profile_Nestle, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = autonomous_life.setState("solitary")
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_004(set_profile_Nestle, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_005(set_profile_Benesse, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME


def test_toreplace_VALID_DIA_002_006(set_profile_Benesse, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_007(set_profile_Mizuho, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_008(set_profile_Mizuho, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_009(set_profile_SMBC, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_010(set_profile_SMBC, force_compilation, dialog, autonomous_life):
    logs = connect_message(log_message_compile_time)
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_011(set_profile_B2C, force_compilation, dialog, autonomous_life):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_precompile()
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)
    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME

def test_toreplace_VALID_DIA_002_012(set_profile_B2C, force_compilation, dialog, autonomous_life):
    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_precompile()
    y = dialog._runMain()
    while not (logs["reflex 1"] and logs["welcome 1"]):
        time.sleep(3)

    assert logs["reflex 1"] < NESTLE_BAYTRAIL_REFLEX_TIME
    assert logs["welcome 1"] < NESTLE_BAYTRAIL_WELCOME_TIME


def non_test_VALID_DIA_003_001(dialog_compile, restart_naoqi_no_life):                # Missing associate dummy profile fixture
    s = Session()
    s.connect(ssh_tools.get_ip())
    autonomous_life = s.service("ALAutonomousLife")
    dialog = s.service("ALDialog")

    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_precompile()

    autonomous_life.setState("solitary")
    while logs.get_precompile_result() is None:
        time.sleep(3)
        #print "sleep"

    print "======================================="
    print "     Result = " + str(logs.get_precompile_result())
    print "======================================="


def NON_VALID_test_VALID_DIA_003_002(dialog_compile, reboot_no_life):
    s = Session()
    s.connect(ssh_tools.get_ip())
    autonomous_life = s.service("ALAutonomousLife")
    dialog = s.service("ALDialog")

    logs = log_viewer(ssh_tools.get_ip())
    logs.watch_precompile()

    autonomous_life.setState("solitary")
    while logs.get_precompile_result() is None:
        time.sleep(3)

    print "======================================="
    print "     Result = " + str(logs.get_precompile_result())
    print "======================================="
