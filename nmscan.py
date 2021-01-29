import ipaddress as ip
import subprocess as sp
from datetime import datetime
from traceback import print_exc


class BaseScan:
    def __init__(self):
        self.time_format = '%Y-%m-%d'
        self._case_prefix = 'scan'
        self._case_rcode = None
        self._case_list = []
        self._case_now = None

        self._host_list = []
        self._host_now = None

        self._get_cases()
        self._sort_cases()

    def __call__(self):
        'Start testing...'
        for host in self._host_list:
            self._host_now = host
            self._exec_cases()

    def _get_cases(self):
        prefix = self._case_prefix
        cases = dir(self)
        cases = filter(lambda item: item.startswith(prefix), cases)
        self._case_list = list(cases)

    def _sort_cases(self):
        self._case_list.sort(
            key=lambda item: item.split('_')[:-1],
            reverse=True)

    def _host_validate(self, host):
        try:
            return str(ip.ip_address(host))

        except ValueError:
            pass

    def _hosts_filter(self):
        tmp = filter(self._host_validate, self._host_list)
        tmp = filter(None, tmp)
        self._host_list = list(tmp)

    def hosts_from_list(self, hosts):
        self._host_list = iter(hosts)
        self._hosts_filter()

    def hosts_from_file(self, fname):
        with open(fname) as fd:
            hosts = filter(None, fd)
            hosts = map(str.rstrip, hosts)
            self._host_list = hosts
            self._hosts_filter()

    def _get_date(self):
        date = datetime.now()
        return date.strftime(self.time_format)

    def _get_output_fd(self):
        fname = '{}_{}-{}.log'.format(
            self._host_now,
            self._get_date(),
            self._case_now)

        return open(fname, 'wb')

    def exec_cmd(self, cmd):
        with self._get_output_fd() as fd:
            ps = sp.Popen(cmd, shell=True, stdout=fd, stderr=fd)
            self._case_rcode = ps.wait()
            return self._case_rcode

    def _exec_cases(self):
        for case in self._case_list:
            self._case_now = case
            func = getattr(self, case)

            try:
                func(self._host_now)
                rcode = self._case_rcode
                print('Task: {}:{}:{}'.format(self._host_now, case, rcode))

            except Exception:
                print_exc()
