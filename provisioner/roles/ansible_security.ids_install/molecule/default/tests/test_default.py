import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_snort_dir(host):
    f = host.file('/etc/snort')
    assert f.is_directory


def test_snort_rules_white_list(host):
    f = host.file('/etc/snort/rules/white_list.rules')
    assert f.exists


def test_snort_rules_black_list(host):
    f = host.file('/etc/snort/rules/black_list.rules')
    assert f.exists


def test_barnyard_conf(host):
    f = host.file('/etc/snort/barnyard2.conf')
    assert f.exists


def test_snort_service(host):
    s = host.service("snort")
    assert s.is_running
    assert s.is_enabled
