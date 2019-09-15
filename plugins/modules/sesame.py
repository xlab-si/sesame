#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["stableinterface"],
    "supported_by": "community",
}

DOCUMENTATION = """
module: sesame
author: Tadej Borovšak (@tadeboro)
short_description: Manage doors on AnsibleFest2019 contraption thingy
description:
  - There is no long description, because the module does very little.
version_added: 1.0.0
options:
  state:
    description:
      - Target state of the doors.
    type: str
    choices: [ opened, closed ]
    required: true
"""

EXAMPLES = """
- name: Make sure the doors are opened
  sesame:
    state: opened

- name: Make sure the doors are closed
  sesame:
    state: closed
"""

RETURN = """
state:
  description: State of the doors.
  returned: always
  type: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    import sesame
    HAS_SESAME = True
except ImportError:
    HAS_SESAME = False


def sync(desired_state, check_mode):
    current_state = sesame.state()
    if current_state == desired_state:
        return False, desired_state

    if check_mode:
        return True, desired_state

    if desired_state == "closed":
        sesame.close_doors()
    else:
        sesame.open_doors()

    return True, desired_state


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            state=dict(
                choices=["opened", "closed"],
            ),
        ),
    )

    if not HAS_SESAME:
        module.fail_json(
            msg="This module must be run on Steampunked rPI",
        )

    changed, state = sync(module.params["state"], module.check_mode)
    module.exit_json(changed=changed, state=state)


if __name__ == "__main__":
    main()
