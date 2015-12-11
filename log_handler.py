import os
import numpy as np
from qi import Session, logging

### Should centralize those informations for use with cpuWatch?
RECORD_DIRECTORY = "/tmp/acceptance_dialog/log_viewer"
HEADERS = ('timestamp', 'log')
CSV_SEP = ','

class log_viewer(object):
    message_start   = ''
    message_stop    = ''
    is_logging      = False
    log_records     = []

    def __init__(self, ip, message_start = 'Enable wav logging', message_stop = 'Preload finished'):
        log_viewer.message_start = message_start
        log_viewer.message_stop = message_stop
        self.s = Session()
        self.s.connect(ip)
        self.log_manager = self.s.service("LogManager")
        self.listener = self.log_manager.getListener()
        self.watch()

    def watch(self):
        self.listener.clearFilters()
        self.listener.setLevel(logging.DEBUG)
        self.listener.onLogMessage.connect(dialog_preload_timestamp_message)

    ###
    ### Helpers
    ###
    def get_log_subset(self, substring = '', begin = '', end = '', logs = False):
        if not logs:
            logs = self.log_records
        subset = []
        appending = False
        for log in logs:
            if begin in log[1]:
                appending = True
            if substring in log[1] and appending:
                subset.append(log)
            if end in log[1]:
                appending = False
        return subset

    def dump_logs(self, file_name):
        if not os.path.isdir(RECORD_DIRECTORY):
            os.makedirs(RECORD_DIRECTORY)
        file_path = os.path.join(RECORD_DIRECTORY, file_name)
        with open(file_path, 'w') as f:
            f.write(CSV_SEP.join([x for x in HEADERS]))
            for line in self.log_records:
                f.write(CSV_SEP.join([str(x) for x in line]))

    ###
    ### Access functions
    ###
    def get_load_time(self):
        logs = self.get_log_subset(substring = 'Load topic')
        timestamps = [x[0] for x in logs]
        return np.max(timestamps) - np.min(timestamps)

    def get_bundle_compile_time(self, bundle):
        begin = 'Compile bundle: {}'.format(bundle)
        print begin
        log = self.get_log_subset(substring = 'Bundle compilation time', begin = begin, end = 'Bundle compilation time')
        print log
        return float(log[0][1].split()[-2]) / 1000

    def get_model_compile_time(self, bundle):
        begin = 'Compile bundle: {}'.format(bundle)
        print begin
        log = self.get_log_subset(substring = '...model compiled', begin = 'Compile bundle: {}'.format(bundle), end = 'Bundle compilation time')
        print log
        return float(log[0][1].rsplit()[-2].strip('(')) / 1000

    def get_reco_compile_time(self, bundle, language):
        bundle_log = self.get_log_subset(substring = '', begin = 'Compile bundle: {}'.format(bundle), end = 'Bundle compilation time')
        log = self.get_log_subset(substring = 'Speech Recognition: Compilation time', begin = language, end = 'Speech Recognition: Compilation time', logs = bundle_log)
        return float(log[0][1].rsplit()[-2]) / 1000

    def get_timestamp_range(self, sequence):
        begin       = ''
        end         = ''
        substring   = ''
        if sequence == 'loading':
            substring = 'Load topic'
        if sequence == 'compile_bundle':
            begin   = 'Compile bundle: welcome'
            end     = 'Bundle compilation time'
        if sequence == 'compile_model':
            begin   = 'compile_bundle'
            end     = '...model compiled'
        if sequence == 'compile_reco_Japanese':
            pass
        if sequence == 'compile_reco_English':
            pass
        log = self.get_log_subset(substring = substring, begin = begin, end = end)
        return [x[0] for x in log]

    def check_for_error(self, begin = '', end = ''):
        self.get_log_subset(begin = '', end = '')


###
###     Callbacks
###
def dialog_preload_timestamp_message(mess):
    if 'Dialog' in mess['category']:
        if log_viewer.message_start in mess['message']:
            log_viewer.is_logging = True
        if log_viewer.is_logging:
            log_viewer.log_records.append((mess['timestamp']['tv_sec'], mess['message'], mess['level']))
        if log_viewer.message_stop in mess['message']:
            log_viewer.is_logging = False


if __name__ == '__main__':
    ip = '10.0.132.103'
    x = log_viewer(ip = ip, message_start = 'Enable wav logging', message_stop = 'Preload finished')
    s = Session()
    s.connect(ip)
    dialog = s.service('ALDialog')
    dialog.deleteSerializationFiles()
    dialog._resetPreload()
    print 'Preloading ...'
    dialog._preloadMain()

    print 'Loading Time'
    print x.get_load_time()
    tme_range = x.get_timestamp_range('loading')
    print tme_range

    tme_range = x.get_timestamp_range('compile_bundle')
    print 'Bundle compilation time'
    print tme_range[-1] - tme_range[0]
    print x.get_bundle_compile_time('welcome')

    tme_range = x.get_timestamp_range('compile_model')
    print 'Model compilation time'
    print tme_range[-1] - tme_range[0]
    print x.get_model_compile_time('welcome')

    print x.get_reco_compile_time('welcome', 'Japanese')
    print x.get_reco_compile_time('welcome', 'English')




    mess_keys ={'category': 'Dialog.Model.personalData',
    'level': 4L,
    'timestamp': {'tv_sec': 1449740234L, 'tv_usec': 148171L},
    'source': ':compile:0',
    'location': '2a743c38-edf5-4ab5-b5d0-118a970207d3:3458',
    'message': 'Compiling the model...',
    'id': 14888L}

