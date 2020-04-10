#!/usr/bin/env python

import os
import random
import string


def main():
    admin_password = ''.join(random.choice(string.ascii_lowercase) for i in range(12))
    name_prefix_identifier = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
    ec2_name_prefix = 'tqe-gating-%s' % name_prefix_identifier
    with open('provisioner/tests/ci-common.yml', 'w') as f:
        f.write("""---
admin_password: %s
ec2_name_prefix: %s
""" % (admin_password, ec2_name_prefix))

    change_id = os.getenv('WORKSHOPS_CHANGE_ID')
    if change_id:
        with open('provisioner/tests/ci-common.yml', 'a') as f:
            f.write("""ansible_workshops_refspec: +refs/pull/%s/head:refs/remotes/origin/PR-%s
ansible_workshops_version: PR-%s
""" % (change_id, change_id, change_id))


if __name__ == '__main__':
    main()
