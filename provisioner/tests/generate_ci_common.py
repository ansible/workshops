#!/usr/bin/env python

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


if __name__ == '__main__':
    main()
