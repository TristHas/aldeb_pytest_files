#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- encoding: UTF-8 -*-
"""
Audio fixtures
"""



__author__ = "thascoet"
__copyright__ = "Copyright September 2015, Aldebaran Robotics"

from functionaltools.ssh_tools import is_file_in, send_file, delete, runcommand
from functionaltools.audio_tools import get_audio_source_id, get_audio_sink_id
import pytest
from functionaltools.ssh_tools import get_ip, is_file_in, send_file, delete, runcommand
from functionaltools.audio_tools import trigger_robot_call_to_regulator, change_regulator_mockup_config
from functionaltools import operator
import time
import os.path
import glob
import re
import sys
from qi import Session

try :
    from qualifcloudsdk import cloud
except ImportError:
    print "qualifcloudsdk importation error"

UID_thascoet = '3936'
REBOOT_TIME = 60 * 5
FLASH_TIME = 60 * 10


TEST_ACCEPTANCE_TOPIC_PUSH_MODE = (
                                "topic: ~test_acceptance_push()\n"
                                "language: jpj　\n"
                                "proposal: おはよう \n "
                                "proposal:  おはようございます\n "
                                )


TEST_ACCEPTANCE_TOPIC_2_JPJ = (
                "topic: ~test_acceptance_2()\n"
                "language: jpj　\n"

                "concept:(alcohols) [ ビール '[赤い 白い] ワイン ' ] \n "

                # UAT_DIA_QCH_001
                "u: (おはよう) おはようございます\n"


                "u:(飲みものは何) ^enumerate(~alcohols) があるんですけど　大好きなのは　^enumerate(~alcohols, 2) です\n "

                "u:(ワインがほしい) はい、赤いか白いワインがほしいですか ? \n"
                "   u1:(ちょっとまって) はいゆくりしてね ^stayInScope \n"
                "   u1:(赤い) 赤い? ほんまに? \n"
                "       u2:(はい) 分かりました \n"
                "       u2:(いいえ) はい \n"
                "   u1:(白い) 白い? ほんまに?\n"
                "       u2:(はい) 分かりました \n "
                "       u2:(いいえ) はい \n "

                "u:(変数のテストしよう) $variable='オケ' \n "
                "u:($variable=='オケ') 変数はオケーです \n "
                "   u1:($variable) \n "
                "   [ \n "
                "   はいそうです $variable=='ok' ^stayInScope $variable = 'not ok'\n "
                "   いいえ違う $variable<>'ok' ^stayInScope $variable = 1 \n "
                "   ] \n "
                "   u1:(ジーロよりは?) \n "
                "   [ "
                "   $variable <= 0　した   \n "
                "   $variable > 0 うえ \n "
                "   ] \n "

                "$tmp = $Dialog/Month \n "
                "u:(今何月のテスト) \n "
                "^first[ \n "
                "はい　今月は　$Dialog/Month $tmp <> $Dialog/Month \n "
                "いいえ　しっぱい$tmp == $Dialog/Month \n "
                "] \n "

                "u:(アップは起動して) オケ　$Dialog/StartApp=　'家族登録' \n"

                "u:(ハーロ)[ハーロ　おはよう　おはようございます]"

                "u:^private(プライベートインプット) できる \n "

                "u:(優先は) 二番のトピック \n "

                "u:^recover(リーコーば) 失敗です \n"  # syntax for recover seems wrong: "recover:"

                "u:(リーコーば) 成功です \n"

                "u:^recover(またリーコーば) 成功です \n"

                "u:^fallback(またリーコーば) 失敗です \n"

                "u:(deactivate tag) ^deactivate(testtag) \n "   # to be translated

                "u:(reactivate tag) ^activate(testtag) \n "     # to be translated

                "u:(タグは) タグのに話す %testtag \n"

                "u:(ごちゅうテスト) ^goto(proposaltag) \n "

                "proposal: ごちゅうテスト %proposaltag \n "

                "u:(ルールごちゅう) ^goto(outputtag) \n "

                "u:(anything): ルールごちゅう %outputtag ^ \n "

                "u:(話して　!ください)　はい　話す"




                "u:(remember me _*)    \n"

                )


TEST_ACCEPTANCE_TOPIC_3_JPJ = (
                    "topic: ~test_acceptance_2()\n"
                    "language: jpj\n"
                    "u:^recover(Do recover sections have priority?) No they don't \n"
                    "u:(優先は) さん番のトピック  \n "
                )


TEST_ACCEPTANCE_TOPIC_4_ENG = (

                )

TEST_ACCEPTANCE_TOPIC_4_CHN = (

                )

TEST_ACCEPTANCE_TOPIC_4_ITA = (

                )

TEST_ACCEPTANCE_TOPIC_4_ITA = (

                )



TEST_ACCEPTANCE_TOPIC_JPJ = (
                "topic: ~test_acceptance()\n"
                "language: jpj\n"

                "concept:(kanji_different_pronunciations) [今月 今 日本 会社]\n"
                "concept:(hiragana) [だめ とても いらっしゃいませ まいにち]\n"
                "concept:(katakana_alcohols) [ビール ワイン ウイスキー ウォッカ]\n"

                "dynamic: colors_dynamic\n"

                "proposal: テストをしましょう\n"
                "proposal: テストがとても好きです\n"


                "u: (1) 2\n"
                " u1: (3) 4\n"
                "    u2: (5) 6\n"
                "    u2: (終わりましょう) OK\n"

                "u: (おはよう) おはよう ございます\n"
                "u: (私は [フランス人 日本人] です) どうぞよろしく\n"
                "u: (アルデバランの 社員 です) [そうですか。 わかりました。]\n"
                "u: (こんにちは {ペッパー}) こんにちは マスター\n"
                "u: (お酒が好きです) じゃ、 ~katakana_alcohols を 飲みましょう\n"

                "u: (温度) $Device/SubDeviceList/HeadPitch/Temperature/Sensor/Value\n"
                "u: (e: FrontTactilTouched) あああああ\n"

                "u: (~hiragana) 平仮名 コンセプト です\n"
                "u: (~kanji_different_pronunciations) 漢字 コンセプト です\n"
                "u: (~katakana_alcohols) カタカナ コンセプト です\n"
                "u: (~colors_dynamic) ダイナミック コンセプト\n"
                "u: (漢字) ~kanji_different_pronunciations\n"
                "u: (平仮名) ~hiragana\n"
                "u: (カタカナ) ~katakana_alcohols\n"
                "u: (ダイナミック) ~colors_dynamic\n"

                "u: (_[ポーランド フランス 日本]は 綺麗な 国 です。) $1 へ 行きましょう！\n"
                "u: (_~katakana_alcohols を飲みたい) $1 を 飲みましょう！\n"
                "u: (_~colors_dynamic シャツ を 買います)  新しい シャツは $1 です\n"

                "u: (ランダム) ^rand[おはよう こんにちは こんばんは おやすみなさい]\n"
                )


            ########################################################
            ###                 Cloud settings                   ###
            ########################################################

def clean_up(robotId, nuage):
    """
    This function disassociates a robot from all its groups and profiles
    Parameters: nuage = Cloud object on the "ppd-cloud.aldebaran-robotics.com" domain
                robotId = robot id in the cloud
    Return value: profile objects that remain associated with the robot after clean up
                  It can be used to check error cases of the clean up
    """
    r = nuage.get_fleet_api_robots_groups(rid = robotId)
    result = r.json()
    robotGroups = result['groups']
    for group in robotGroups:
        nuage.delete_fleet_api_groups_robots(gid = group['id'], rid = robotId)

    r = nuage.get_ade_api_robots_channels(rid = robotId)
    result = r.json()
    robotChanels = result['channels']
    for chanel in robotChanels:
        nuage.delete_ade_api_robots_channels(rid = robotId, cid = chanel['id'])

    r = nuage.get_ade_api_robots_profiles(rid = robotId)
    result = r.json()
    profiles = result['profiles']

    return profiles

@pytest.fixture(scope="function")
def check_cloud_env():
    ses = Session()
    ses.connect(ssh_tools.get_ip())
    system = ses.service("ALSystem")
    if float(sy.version()) > 2.4:
        alcloud = ses.service("_ALCloud")
    else
        alcloud = ses.service("ALCloud")
    if alcloud.getEnvironment() != "ppd":
        alcloud.setEnvironment("ppd")
        print "Your robot cloud configuration needs to be changed to a preproduction environment."
        print "Please wait for naoqi to restart..."
        ssh_tools.nao_restart(life=False)
        print "Your configuration has been successfully changed"
        return True
    else:
        return False

def associate_group(memory, request, store, groupNames):
    """
    Associate groups to a robot and updates it
    Finalizer: cleanup and updates
    Parameters: memory: Proxy on the ALMemory module of the robot
                request: request object
                store: Proxy on the ALStore module of the robot
                groupNames: Names of the groups to be associated to the robot
    """
    fullHeadId = memory.getData("RobotConfig/Head/FullHeadId")

    nuage = cloud.Cloud(domain="ppd-cloud.aldebaran-robotics.com", protocol="https")
    nuage.set_credentials(oauth=True)

    r = nuage.get_core_api_robots()
    result = r.json()
    robots = result['robots']
    myRobot = None
    for robot in robots:
        if robot['productid'] == fullHeadId:
            myRobot = robot
            break
    if not myRobot:
        sys.exit("ERROR : can't find robot rid on the cloud.")
    else:
        robotId = myRobot['id']


    print("\n=============================")
    print("Cleaning Up")
    print("=============================")

    profiles = clean_up(robotId, nuage)
    if profiles:
        print "WARNING: Profiles remaining on robot configuration:"
        print profiles


    r = nuage.get_fleet_api_groups()
    result = r.json()
    groupIds = []
    for groupName in groupNames:
        print("=============================")
        print( " ".join(["Associating", groupName ," Group"]) )
        print("=============================")

        groupId = None
        for item in result["groups"]:
            if item["name"] == groupName:
                groupId = item["id"]
                break
        if groupId:
            nuage.post_fleet_api_groups_robots(rid = robotId, gid = groupId)
        else:
            print "ERROR: Group not found"

    print("=============================")
    print(" Robot Updating")
    print("=============================")
    store.update()

    def ending():
        print("=============================")
        print(" ENDING: Cleaning up")
        print("=============================")
        clean_up(robotId, nuage)

        print("=============================")
        print(" ENDING: Robot Updating")
        print("=============================")
        store.update()
    request.addfinalizer(ending)

@pytest.fixture
def set_profile_Nestle(check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    NESTLE_GROUPS = ["dialog_compile_Nestle_Test"]
    associate_group(memory, request, store, NESTLE_GROUPS)

@pytest.fixture
def set_profile_Mizuho(check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    MIZUHO_GROUPS = ["dialog_compile_Mizuho_Test"]
    associate_group(memory, request, store, MIZUHO_GROUPS)

@pytest.fixture
def set_profile_SMBC(check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    SMBC_GROUPS = ["dialog_compile_SMBC_Nikko_Test"]
    associate_group(memory, request, store, SMBC_GROUPS)

@pytest.fixture
def set_profile_Benesse(check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    BENESSE_GROUPS = ["dialog_compile_Benesse_Test"]
    associate_group(memory, request, store, BENESSE_GROUPS)

@pytest.fixture
def set_profile_Shopfor24(check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    SHOP_GROUPS = ["dialog_compile_LeCommon", "dialog_compile_LeShop_for2.4"]
    associate_group(memory, request, store, SHOP_GROUPS)

@pytest.fixture
def set_profile_Shopfor20(check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    SHOP_GROUPS = [u"dialog_compile_ダンスなしモード_本番", u"dialog_compile_コモングループ"]
    associate_group(memory, request, store, SHOP_GROUPS)


@pytest.fixture
def set_profile_B2C(check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_B2C_Config to the robot
    """
    B2C_GROUPS = ["dialog_compile_B2C_Config"]  # To be filled with appropriate Name
    associate_group(memory, request, store, B2C_GROUPS)



@pytest.fixture
def reset_dialog_acceptance_jpj(dialog, tts, asr, request, autonomous_life, operator):
    try:  # new method from starting from 2.4.0.42
        dialog.pause(False)
    except RuntimeError:
        pass
    dialog.stopDialog()
    if autonomous_life.getState() != "disabled":
        operator.notif("\nDialog API tests should not be executed with ALAutonomousLife. Disabling ALAutonomousLife...")
        autonomous_life.setState("disabled")
    for subscriber in dialog.getSubscribersInfo():
        dialog.unsubscribe(subscriber[0])
    for topic in dialog.getAllLoadedTopics():
        dialog.deactivateTopic(topic)
        try:
            dialog.unloadTopic(topic)
        except RuntimeError:
            pass
    for subscriber in asr.getSubscribersInfo():
        asr.unsubscribe(subscriber[0])
    tts.stopAll()
    dialog.resetAll()
    dialog.setLanguage("Japanese")
    # must do this too - dialog can be still in English but ASR in French -> then it's gonna stay in French
    asr.setLanguage("Japanese")
    tts.setLanguage("Japanese")
    dialog.loadTopicContent(TEST_ACCEPTANCE_TOPIC_JPJ)
    dialog.activateTopic("test_acceptance")
    dialog.subscribe("test_acceptance_jpj")

    def ending():
        try:  # new method from starting from 2.4.0.42
            dialog.pause(False)
        except RuntimeError:
            pass
        dialog.stopDialog()
        for subscriber in dialog.getSubscribersInfo():
            dialog.unsubscribe(subscriber[0])
        for topic in dialog.getAllLoadedTopics():
            dialog.deactivateTopic(topic)
            try:
                dialog.unloadTopic(topic)
            except RuntimeError:
                pass
        for subscriber in asr.getSubscribersInfo():
            asr.unsubscribe(subscriber[0])
        tts.stopAll()
    request.addfinalizer(ending)



@pytest.fixture
def prepare_unengaged_dialog_jpj(dialog, tts, asr, request, autonomous_life, operator):
    try:  # new method from starting from 2.4.0.42
        dialog.pause(False)
    except RuntimeError:
        pass
    dialog.stopDialog()
    if autonomous_life.getState() != "disabled":
        operator.notif("\nDialog API tests should not be executed with ALAutonomousLife. Disabling ALAutonomousLife...")
        autonomous_life.setState("disabled")
    for subscriber in dialog.getSubscribersInfo():
        dialog.unsubscribe(subscriber[0])
    for topic in dialog.getAllLoadedTopics():
        dialog.deactivateTopic(topic)
        try:
            dialog.unloadTopic(topic)
        except RuntimeError:
            pass
    for subscriber in asr.getSubscribersInfo():
        asr.unsubscribe(subscriber[0])
    tts.stopAll()
    dialog.resetAll()
    dialog.setLanguage("Japanese")
    # must do this too - dialog can be still in English but ASR in French -> then it's gonna stay in French
    asr.setLanguage("Japanese")
    tts.setLanguage("Japanese")

    def ending():
        try:  # new method from starting from 2.4.0.42
            dialog.pause(False)
        except RuntimeError:
            pass
        dialog.stopDialog()
        for subscriber in dialog.getSubscribersInfo():
            dialog.unsubscribe(subscriber[0])
        for topic in dialog.getAllLoadedTopics():
            dialog.deactivateTopic(topic)
            try:
                dialog.unloadTopic(topic)
            except RuntimeError:
                pass
        for subscriber in asr.getSubscribersInfo():
            asr.unsubscribe(subscriber[0])
        tts.stopAll()
    request.addfinalizer(ending)


# Fixture téléchargement Companions
@pytest.fixture
def companions(behavior_manager, store):
    applications = '|'.join(behavior_manager.getInstalledBehaviors())
    if not "sbr_00380_frienbook" in applications:

        # Upload profile with companions on the robot

        friendbook_installed = False
        while not friendbook_installed:
            store.updateApps()
            time.sleep(3)
            friendbook_installed = "sbr_00380_frienbook" in applications

        return true
    return false

@pytest.fixture
def run_dialog_dev(behavior_manager, store):
    applications = '|'.join(behavior_manager.getInstalledBehaviors())
    if not "run_dialog_dev" in applications:
        # Upload profile with companions on the robot
        dialog_installed = False
        while not dialog_installed:
            store.updateApps()
            time.sleep(3)
            dialog_installed = "run_dialog_dev" in applications
        return true
    return false


@pytest.fixture
def switch_dialog_from_engaged_to_unengaged(dialog, autonomous_life, memory, behavior_manager, memory):
    if autonomous_life.getState() is not 'solitary':
        autonomous_life.setState('solitary')
    behavior_manager.runBehavior("run_dialog_dev/.")
    time.sleep(3)
    memory.raiseEvent('UserSession/ShouldExitInteractiveActivity')
    memory.insertData('EEU/Pleasure', 0)



