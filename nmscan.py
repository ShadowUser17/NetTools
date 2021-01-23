import ipaddress as ip
import subprocess as sp
from datetime import datetime
from traceback import print_exc


class BaseScan:
    def __init__(self, hosts):
        'hosts = ip/cidr, fout = enable output to file.'
        self.hosts = ip.ip_network(hosts)
        self.time_format = '%Y-%m-%d'
        self._case_prefix = 'scan'
        self._case_now = None
        self._get_cases()

    def __call__(self):
        'Start testing...'
        for host in self.hosts.hosts():
            self._exec_cases(str(host))

    def _get_cases(self):
        prefix = self._case_prefix
        cases = dir(self)
        cases = filter(lambda item: item.startswith(prefix), cases)
        self._case_list = list(cases)

    @property
    def cases(self):
        return self._case_list

    def _get_date(self):
        date = datetime.now()
        return date.strftime(self.time_format)

    def _get_output_fd(self, host):
        date = self._get_date()
        case = self._case_now
        fname = '{}_{}-{}.log'.format(host, date, case)
        return open(fname, 'wb')

    def exec_cmd(self, args, host):
        with self._get_output_fd(host) as fd:
            cmd = '{} {}'.format(args, host)
            ps = sp.Popen(cmd, shell=True, stdout=fd, stderr=fd)
            ps.communicate()

    def _exec_cases(self, host):
        for case in self._case_list:
            self._case_now = case
            func = getattr(self, case)

            try:
                print('Start:', host, case)
                func(host)
                print('Exit:', host, case)
            except Exception:
                print_exc()