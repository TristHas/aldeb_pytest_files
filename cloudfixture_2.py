# -*- coding: utf-8 -*-

"""
Cloud fixtures
"""

__author__ = "thascoet"
__copyright__ = "Copyright September 2015, Aldebaran Robotics"

import pytest
import sys
from qi import Session
import time
try:
    from qualifcloudsdk import cloud
except ImportError:
    print "You don't have QualifCloudSdk however... Don't Care about it"
from functionaltools import ssh_tools
from deploy_data import *

UID_thascoet = '3936'
PPD_URL = "ppd-cloud.aldebaran-robotics.com"
PROD_URL = "cloud.aldebaran-robotics.com"
FLASH_TIME = 60 * 15
REBOOT_TIME = 60 * 7

@pytest.fixture(scope="function")
def set_no_life(preference_manager, request):
    preference_manager.setValue("com.aldebaran.debug", "DisableLifeAndDialog", 1)
    def ending():
        s = Session()
        s.connect(ssh_tools.get_ip())
        preference_manager = s.service("ALPreferenceManager")
        preference_manager.setValue("com.aldebaran.debug", "DisableLifeAndDialog", 0)

    #request.addfinalizer(ending)

############################
####    Not working     ####
############################
@pytest.fixture(scope="function")
def reboot_no_life(preference_manager, system, request):
    preference_manager.setValue("com.aldebaran.debug", "DisableLifeAndDialog", 1)
    print "rebooting..."
    system.reboot()
    preference_manager = None
    system = None
    time.sleep(REBOOT_TIME)
    def ending():
        s = Session()
        s.connect(ssh_tools.get_ip())
        preference_manager = s.service("ALPreferenceManager")
        preference_manager.setValue("com.aldebaran.debug", "DisableLifeAndDialog", 0)
    request.addfinalizer(ending)


@pytest.fixture(scope="function")
def disable_life(autonomous_life):
    autonomous_life.setState('disabled')

@pytest.fixture(scope="function")
def force_compilation(dialog, autonomous_life):
    from fabric.api import env, run
    #dialog.deleteSerializationFiles()
    env.user        = 'nao'
    env.password    = 'nao'
    env.host_string = ssh_tools.get_ip()
    run('rm -r /home/nao/.local/share/dialog/*')
#    run('rm /home/nao/.local/share/PackageManager/apps/run_dialog_dev/init/*.fcf')
    dialog._resetPreload()

@pytest.fixture(scope="function")
def force_compilation_old():
    s = Session()
    s.connect(ssh_tools.get_ip())
    dialog = s.service('ALDialog')
    #autonomous_life.setState("disabled")
    dialog.deleteSerializationFiles()
    dialog.resetAll()
    dialog._resetPreload()



@pytest.fixture(scope="function")
def dialog_compile(autonomous_life):
    autonomous_life.setState("solitary")
    autonomous_life.setState("disabled")


@pytest.fixture(scope="function")
def life_off():
    s = Session()
    s.connect(ssh_tools.get_ip())
    alife = s.service('ALAutonomousLife')
    alife.setState ('disabled')


@pytest.fixture(scope="function")
def restart_naoqi():
    ssh_tools.nao_restart()

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


# CPU watch fixture
@pytest.fixture(scope="function")
def cpu_server(request):
    ip = ssh_tools.get_ip()
    kill_server(ip = ip)
    clean_server(ip = ip)
    deploy_server(ip = ip)
    run_server(ip = ip)
    def ending():
        kill_server(ip = ip)
        clean_server(ip = ip)
    request.addfinalizer(ending)

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
    nuage = cloud.Cloud(domain=PPD_URL, protocol="https")
    x = nuage.set_credentials(oauth=True)
    r = nuage.get_core_api_robots(fullHeadId)
    result = r.json()
    if result['id']:
        robotId = result['id']
    else:
        sys.exit("ERROR : can't find robot rid on the cloud.")

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
def set_profile_Nestle(life_off, check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    NESTLE_GROUPS = ["dialog_compile_Nestle_Test"]
    associate_group(memory, request, store, NESTLE_GROUPS)

@pytest.fixture
def set_profile_Mizuho(life_off, check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    MIZUHO_GROUPS = ["dialog_compile_Mizuho_Test"]
    associate_group(memory, request, store, MIZUHO_GROUPS)

@pytest.fixture
def set_profile_SMBC(life_off, check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    SMBC_GROUPS = ["dialog_compile_SMBC_Nikko_Test"]
    associate_group(memory, request, store, SMBC_GROUPS)

@pytest.fixture
def set_profile_Benesse(life_off, check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    BENESSE_GROUPS = ["dialog_compile_Benesse_Test"]
    associate_group(memory, request, store, BENESSE_GROUPS)

@pytest.fixture
def set_profile_Shopfor24(life_off, check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    SHOP_GROUPS = ["dialog_compile_LeCommon", "dialog_compile_LeShop_for2.4"]
    associate_group(memory, request, store, SHOP_GROUPS)

@pytest.fixture
def set_profile_Shopfor20(life_off, check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_Nestle_Test to the robot
    """
    SHOP_GROUPS = [u"dialog_compile_ダンスなしモード_本番", u"dialog_compile_コモングループ"]
    associate_group(memory, request, store, SHOP_GROUPS)


@pytest.fixture
def set_profile_B2C(life_off, check_cloud_env, request, memory, store):
    """
    Associate group dialog_compile_B2C_Config to the robot
    """
    B2C_GROUPS = ["dialog_compile_B2C_Config"]  # To be filled with appropriate Name
    associate_group(memory, request, store, B2C_GROUPS)


@pytest.fixture(scope="function")
def check_cloud_env():
    ses = Session()
    ses.connect(ssh_tools.get_ip())
    system = ses.service("ALSystem")
    version = system.version().split(".")
    if len(version) < 2:
        print version
        sys.exit("wrong version format")
    else:
        if int(version[0]) == 2:
            if int(version[1]) < 4:
                print """Check cloud environment fixture:
                    This script is not made for versions inferior to 2.4.
                    You need to manually set the environment to preproduction. Use Simon's script to do so
                    Once you've done that, remove check_cloud_env fixture from all tests"""
                sys.exit("Exiting program")
            if int(version[1]) > 4:
                alcloud = ses.service("_ALCloud")
            if int(version[1]) == 4:
                alcloud = ses.service("ALCloud")
        if int(version[0]) != 2:
            print """Check cloud environment fixture:
                  This script is made for naoqi version 2.0. You probably need to update it in order to make it work
                  for the version you are using"""
            sys.exit("Exiting program")


    if alcloud.getEnvironment() != "ppd":
        print "Your robot cloud configuration needs to be changed to a preproduction environment."

        #clean prod settings
        #ssh_tools.runcommand('rm -r .local')

        alcloud.setEnvironment("ppd")
        print "Please wait for naoqi to restart..."
        ssh_tools.nao_restart(life=False)

        ses = Session()
        ses.connect(ssh_tools.get_ip())
        if int(version[1]) > 4:
            alcloud = ses.service("_ALCloud")
        if int(version[1]) == 4:
            alcloud = ses.service("ALCloud")

        if alcloud.getEnvironment() == "ppd":
            print "Your configuration has been successfully changed"
        else:
            print "cloud configuration seems to have failed"
            sys.exit("Exiting program")
        return True
    else:
        return False







        #################################################
        ####           Test groups creation          ####
        #################################################

@pytest.fixture
def check_group_content():
    groupNames = ["Nestle_Test", "Mizuho_Test", "SMBC_Nikko_Test", "Benesse_Test",
                   "LeCommon", "LeShop_for2.4", u"ダンスなしモード_本番", u"コモングループ"]
    for name in groupNames:
        baseName = "_".join(["dialog", "compile", name])
        print_group_content(baseName)

def print_group_content(baseName):
    nuage = cloud.Cloud(domain=PPD_URL, protocol="https")
    nuage.set_credentials(oauth=True)
    r = nuage.get_fleet_api_groups()
    result = r.json()
    for item in result["groups"]:
        if item["name"] == baseName:
            oldGID = item["id"]
            print baseName + " found with ID " + str(oldGID)
            group_profiles = cloud_get_group_profiles(nuage, oldGID)
            for i in range(len(group_profiles)):
                profileName = "_".join([baseName, str(i)])
                oldProfileId = group_profiles[i]
                r = nuage.get_ade_api_profiles(pid = oldProfileId)
                result = r.json()
                profile_name = result["name"]
                print "     found profile " + profile_name + " with ID " + str(oldProfileId) + " containing apps:"
                profile_applis = cloud_get_profile_app_names(nuage, oldProfileId)
                for appli in profile_applis:
                    print "          Appli " +  str(appli)


# Helper Functions
def cloud_get_group_profiles(nuage, gid):
    """
    Description: This function
    """
    r = nuage.get_fleet_api_groups_profiles(gid = gid)
    result = r.json()
    profile_ids = [prof["id"] for prof in result["profiles"]]
    #print "profile ids " + str(profile_ids)
    return profile_ids

def cloud_get_profile_app_names(nuage, pid):
    """
    """
    r = nuage.get_ade_api_profiles_applis(pid = pid)
    result = r.json()
    appli_slugs = [appli["slug"] for appli in result["applis"]]
    return appli_slugs

@pytest.fixture
def osef():
    nuage_ppd = cloud.Cloud(domain=PPD_URL, protocol="https")
    nuage_ppd.set_credentials(oauth=True)
    r = nuage_ppd.get_ade_api_applis()
    app_list = r.json()
    for apps in app_list["applis"]:
        print apps

def create_clone_group(gName, nuage_prod, nuage_ppd):
    """
    """
    baseName = "_".join(["dialog", "compile", gName])
    r = nuage_ppd.post_fleet_api_groups(data={"owner":UID_thascoet, "name":baseName})
    result = r.json()
    newGroupId = result["id"]

    print " ".join(["Created new group", baseName, "with ID", str(newGroupId)])
    r = nuage_prod.get_fleet_api_groups()
    result = r.json()
    for item in result["groups"]:
        if item["name"] == gName:
            oldGID = item["id"]
            clone_group_prefs(nuage_prod, oldGID, nuage_ppd, newGroupId)
            print "Cloning prefs"
            group_profiles = cloud_get_group_profiles(nuage_prod, oldGID)
            for i in range(len(group_profiles)):
                profileName = "_".join([baseName, str(i)])
                oldProfileId = group_profiles[i]
                r = nuage_ppd.post_ade_api_profiles( data={"owner":UID_thascoet, "name":profileName} )
                result = r.json()
                newProfileId = result["id"]
                # Associate profile prefs(nuage_prod, oldProfileId, nuage_ppd, newProfileId)
                print " ".join(["    Created new profile", profileName, "with ID", str(newProfileId),
                                "from old profile", str(oldProfileId)])
                # Associate profiles to group
                print "    Cloning prefs"
                clone_profile_prefs(nuage_prod, oldProfileId, nuage_ppd, newProfileId)
                nuage_ppd.post_fleet_api_groups_profiles(gid = newGroupId, pid = newProfileId)
                # Get profile app list

                profile_appli_names = cloud_get_profile_app_names(nuage_prod, oldProfileId)
                r = nuage_ppd.get_ade_api_applis()
                app_list = r.json()

                # associate apps to profile
                for apps in app_list["applis"]:
                    if apps['slug'] in profile_appli_names:
                        appli = apps['id']
                        nuage_ppd.post_ade_api_profiles_applis(pid = newProfileId, aid = appli)
                        print " ".join(["        Associated appli",apps['slug'],"(id =", str(appli), ") to profile", str(profileName),
                                    "with ID", str(newProfileId)])
    return newGroupId

# Fixtures

@pytest.fixture
def cloud_create_B2B_Groups(request, store, memory):
    """
    Description:    Create clone groups of the following "Nestle_Test", "Mizuho_Test", "SMBC_Nikko_Test", "Benesse_Test",
                    "LeCommon", "LeShop_for2.4", u"ダンスなしモード_本番", u"コモングループ".
                    This function does not copy preferences, but only the app content.
                    You should not have to use this function as you should use the existing clone groups.
    Return Value:   list of the clone groups IDs
    """
    nuage_ppd = cloud.Cloud(domain=PPD_URL, protocol="https")
    nuage_ppd.set_credentials(oauth=True)
    nuage_prod = cloud.Cloud(domain=PROD_URL, protocol="https")
    nuage_prod.set_credentials(oauth=True)

    groupNames = ["Nestle_Test", "Mizuho_Test", "SMBC_Nikko_Test", "Benesse_Test",
                   "LeCommon", "LeShop_for2.4", u"ダンスなしモード_本番", u"コモングループ"]

    groupIds = []
    for name in groupNames:
        print " ".join(["Cloning Group", name, "..."])
        newGroup = create_clone_group(name, nuage_prod, nuage_ppd)
        print " ".join(["Created group ", str(newGroup)])
        groupIds.extend([newGroup])
        print groupIds
    return groupIds


@pytest.fixture
def create_B2C_group():
    """
    Description:    Create a clone group containing profiles corresponding to "SB Default Channel", "Default Channel for SB" and
                    "SB Application Channel"
                    This function does not copy preferences, but only the app content.
                    You should not have to use this function as you should use the existing clone group.
    Return Value:   list of the clone group ID
    """
    nuage_ppd = cloud.Cloud(domain=PPD_URL, protocol="https")
    nuage_ppd.set_credentials(oauth=True)
    nuage_prod = cloud.Cloud(domain=PROD_URL, protocol="https")
    nuage_prod.set_credentials(oauth=True)


    oldProfiles = [6613, 5099, 5097]
    baseName = "_".join(["dialog", "compile", "B2C","Config"])
    r = nuage_ppd.post_fleet_api_groups(data={"owner":UID_thascoet, "name":baseName})
    result = r.json()
    newGroupId = result["id"]
    print " ".join(["Created new group", baseName, "with ID", str(newGroupId)])
    for i in range(len(oldProfiles)):
        profileName = "_".join([baseName, str(i)])
        oldProfileId = oldProfiles[i]
        r = nuage_ppd.post_ade_api_profiles( data={"owner":UID_thascoet, "name":profileName} )
        result = r.json()
        newProfileId = result["id"]
        print " ".join(["    Created new profile", profileName, "with ID", str(newProfileId),
                        "from old profile", str(oldProfileId)])
        print "    Cloning prefs"

        clone_profile_prefs(nuage_prod, oldProfileId, nuage_ppd, newProfileId)
        nuage_ppd.post_fleet_api_groups_profiles(gid = newGroupId, pid = newProfileId)
        profile_appli_names = cloud_get_profile_app_names(nuage_prod, oldProfileId)
        r = nuage_ppd.get_ade_api_applis()
        app_list = r.json()

        # associate apps to profile
        for apps in app_list["applis"]:
            if apps['slug'] in profile_appli_names:
                appli = apps['id']
                nuage_ppd.post_ade_api_profiles_applis(pid = newProfileId, aid = appli)
                print " ".join(["        Associated appli",apps['slug'],"(id =", str(appli), ") to profile", str(profileName),
                                "with ID", str(newProfileId)])
    return newGroupId

# Prefs

@pytest.fixture
def test_check_prefs():
    print ""
    nuage_ppd = cloud.Cloud(domain=PPD_URL, protocol="https")
    nuage_ppd.set_credentials(oauth=True)
    r = nuage_ppd.get_prefs_api_profiles_preferences(pid = 7968)
    result = r.json()
    print result
    nuage_prod = cloud.Cloud(domain=PROD_URL, protocol="https")
    nuage_prod.set_credentials(oauth=True)
    r = nuage_prod.get_prefs_api_profiles_preferences(pid = 6613)
    result = r.json()
    print result


def clone_group_prefs(nuage_src, srcGroupId, nuage_dest, destGroupId):
    group_prefs = get_groupe_prefs(nuage_src, srcGroupId)
    r = set_group_prefs(nuage_dest, destGroupId, group_prefs)


def get_groupe_prefs(nuage_src, srcGroupId):
    r = nuage_src.get_prefs_api_groups_preferences(srcGroupId)
    result = r.json()
    group_prefs = result['preferences']
    return group_prefs

def set_group_prefs(nuage_dest, destGroupId, group_prefs):
    for domain_prefs in group_prefs:
        domain_name = domain_prefs["domain"]
        nuage_dest.post_prefs_api_groups_preferences(gid = destGroupId, data={"name":domain_name})
        for pair in domain_prefs["pairs"]:
            nuage_dest.post_prefs_api_groups_preferences(gid = destGroupId, domain = domain_name,
                                                        data = pair)

def clone_profile_prefs(nuage_src, srcProfileId, nuage_dest, destProfileId):
    profile_prefs = get_profile_prefs(nuage_src, srcProfileId)
    set_profile_prefs(nuage_dest, destProfileId, profile_prefs)


def get_profile_prefs(nuage_src, srcProfileId):
    r = nuage_src.get_prefs_api_profiles_preferences(srcProfileId)
    result = r.json()
    profile_prefs = result['preferences']
    return profile_prefs


def set_profile_prefs(nuage_dest, destProfileId, profile_prefs):
    for domain_prefs in profile_prefs:
        domain_name = domain_prefs["domain"]
        nuage_dest.post_prefs_api_profiles_preferences(pid = destProfileId, data={"name":domain_name})
        for pair in domain_prefs["pairs"]:
            nuage_dest.post_prefs_api_profiles_preferences(pid = destProfileId, domain = domain_name,
                                                          data = pair)


@pytest.fixture
def delete_groups():
    """
    Description:    Delete groups or profiles set in delete_profiles and delete_groups local variable.
                    Be very carefull which group you delete.
    """

    nuage = cloud.Cloud(domain=PPD_URL, protocol="https")
    nuage.set_credentials(oauth=True)
    # Fill profile and group Ids you want to delete
    delete_profiles = []
    delete_groups = []
    for profileId in delete_profiles:
        print "deleting profile " + str(profileId)
        nuage.delete_ade_api_profiles(pid = profileId)
    for groupId in delete_groups:
        nuage.delete_fleet_api_groups(gid = groupId)
        print "deleting group " + str(groupId)



# I'm pretty sure this is not the best practice
# The problem is _log_message_precompile_use and _log_message_compile_time cannot take a second input argument
# Either use class attributes, global keyword or lambdas. Maybe lambdas are better?

class log_viewer(object):

    bundle_buff = False
    log_message = {'Bundle compilation time':[],
                   '...model compiled':[],
                   'BNFwelcomeJapanese generated':[],
                   'BNFwelcomeEnglish generated' : [],
                   'Speech Recognition: Compilation time': [],
                   }

                   #[W] 1449044596.920087 3740 Dialog.StrategyBnf: Speech Recognition: Compilation time: 63623 ms
                   #[W] 1449044602.347930 3740 Dialog.StrategyBnf: Speech Recognition: Compilation time: 5262 ms


    def __init__(self, ip):
        self.s = Session()
        self.s.connect(ip)
        self.log_manager = self.s.service("LogManager")
        self.listener = self.log_manager.getListener()

    def watch_precompile(self):
        self.listener.clearFilters()
        self.listener.onLogMessage.connect(_log_message_precompile_use)

    def watch_compile(self):
        self.listener.clearFilters()
        self.listener.onLogMessage.connect(_log_message_compile_time)

    def get_precompile_result(self):
        if not log_viewer.log_message.has_key(" welcome  1"):   # Complete
            return None
        else:
            return log_viewer.log_message[" welcome  1"]   # Complete

    def get_compile_result(self):
        log_viewer.log_message
        if not self.check_bundle_compile_finished():
           return None
        else:
           #print int(log_viewer.log_message['Bundle compilation time'][0].rsplit()[-2])
           print log_viewer.log_message
           return_val = self.treat_compile_message()
           log_viewer.log_message = {'Bundle compilation time':[],
                                     '...model compiled':[],
                                     'BNFwelcomeJapanese generated':[],
                                     'BNFwelcomeEnglish generated' : [],
                                     'Speech Recognition: Compilation time': [],
                                    }
           return return_val

    def check_bundle_compile_finished(self):
        ### Custom
        #print len(log_viewer.log_message['Bundle compilation time'])
        if len(log_viewer.log_message['Bundle compilation time']) != 0:
            return True
        else:
            return False

    def treat_compile_message(self):
        ### Custom
        return_val = {}
        return_val['total']         =  int(log_viewer.log_message['Bundle compilation time'][0].rsplit()[-2])
        return_val['model']         =  int(log_viewer.log_message['...model compiled'][0].rsplit()[-2].strip('('))
        return_val['jpj bnf']       =  int(log_viewer.log_message['BNFwelcomeJapanese generated'][0].rsplit()[-2].strip('('))
        return_val['enu bnf']       =  int(log_viewer.log_message['BNFwelcomeEnglish generated'][0].rsplit()[-2].strip('('))
        return_val['jpj reco']      =  int(log_viewer.log_message['Speech Recognition: Compilation time'][0].rsplit()[-2])
        if len(log_viewer.log_message['Speech Recognition: Compilation time']) > 1:
            return_val['enu reco']      =  int(log_viewer.log_message['Speech Recognition: Compilation time'][1].rsplit()[-2])

        return return_val

def _log_message_precompile_use(mess):
    if "Dialog." in mess["category"]:
        print("\t".join([mess["category"],mess["message"]]))
        if "Compile bundle:" in mess["message"]:
            log_viewer.bundle_buff = mess["message"].rsplit(":")[1]
            log_viewer.log_message[log_viewer.bundle_buff] = None
            print "bundle_buff = " + log_viewer.bundle_buff

        if "Compiling the model..." in mess["message"]:
            if log_viewer.bundle_buff:
                log_viewer.log_message[log_viewer.bundle_buff] = False
                print "log_message[" + log_viewer.bundle_buff + "] = " + str(False)
                log_viewer.bundle_buff = None
            else:
                raise Exception("Log Error: Precompile of bundle done without bundle name knowledge")

        if "Model D-serialized" in mess["message"]:
            if log_viewer.bundle_buff:
                log_viewer.log_message[log_viewer.bundle_buff] = True
                print "log_message[" + log_viewer.bundle_buff + "] = " + str(False)
                log_viewer.bundle_buff = None
            else:
                raise Exception("Log Error: Precompile of bundle done without bundle name knowledge")


BUNDLE_NAME     = 'welcome'
START_WATCH_LOG = 'Compile bundle: ' + BUNDLE_NAME
STOP_WATCH_LOG  = 'Bundle compilation time'


def _log_message_compile_time(mess):
    if "Dialog." in mess["category"]:
        if START_WATCH_LOG in mess["message"]:
            log_viewer.bundle_buff = True
        if log_viewer.bundle_buff:
            for keys in log_viewer.log_message:
                if keys in mess["message"]:
                    try:
                        log_viewer.log_message[keys].append(mess["message"])
                        #print keys + ' = ' + mess["message"]
                    except Exception as e:
                        print e
                        print e.message
        if STOP_WATCH_LOG in mess["message"]:
            #print 'Stopping watching because of ' + mess["message"]
            log_viewer.bundle_buff = False


