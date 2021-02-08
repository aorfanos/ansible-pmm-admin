#!/usr/bin/python

DOCUMENTATION = """
---
module: pmm_admin
short_description: Use pmm-admin to add DB instances to PMM2
"""

DOCUMENTATION = """
---
module: pmm_admin

short_description: Use pmm-admin to add DB instances to PMM2. Does not autoconfigure (pmm-admin config)

version_added: "2.9.10"

description:
    - "A module used to add/remove instances to a PMM2 instance"

options:
    state:
        description:
            - Desired state of the item (present|absent)
        required: true
    database:
        description:
            - What kind of DB to connect to (mysql|mongodb|postgresql|proxysql)
        required: true
    username:
        description:
            - Username to use when connecting
        required: false
    password:
        description:
            - Password to authenticate to DB
        required: false
    hostname:
        description:
            - DB hostname
        required: false
    environment:
        description:
            -  Environment name
        required: false
    cluster:
        description:
            - Cluster name
        required: false
    replication_set:
        description:
            - Replication set
        required: false
    tls:
        description:
            - Use TLS (true|false)
        required: false


author:
    - Alexandros Orfanos (@aorfanos)
"""

EXAMPLES = """
- name: Create a Grafana annotation
  add_grafana_annotation:
    grafana_api_url: "https://grafana.myproject.com"
    grafana_api_key: "..."
    dashboard_id: 468
    panel_id: 20
    text: "Annotation description"
    tags:
      - tag1
      - tag2
  register: result
"""

RETURN = """
remote_status_code:
    description: The HTTP return code of the RESTFul call to Grafana API
    type: int
message:
    description: An auxiliary message, containing the return code and (very) basic troubleshooting info
"""

ANSIBLE_METADATA = {
    "status": ["preview"],
    "supported_by": "community",
    "metadata_version": "1.0",
}

from ansible.module_utils.basic import AnsibleModule
import subprocess
import json


def exists(operation, hostname="", service_name=""):
    _list = subprocess.run(
        "pmm-admin list", shell=True, check=True, capture_output=True
    )
    if operation == "present":
        if hostname in str(_list.stdout):
            return True
        else:
            return False
    # reverse logic below, bc. when we want to remove
    # we need the configuration to be present
    elif operation == "absent":
        if service_name in str(_list.stdout):
            return False
        else:
            return True


def run_module():

    module_args = dict(
        database=dict(type="str", required=True),
        hostname=dict(type="str", required=False),
        service_name=dict(type="str", required=True),
        username=dict(type="str", required=False, no_log=True),
        password=dict(type="str", required=False, no_log=True),
        port=dict(type="int", required=False),
        environment=dict(type="str", required=False),
        tls=dict(type="bool", required=False, default=False),
        register=dict(type="bool", required=False, default=False),
        state=dict(type="str", required=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if exists(
        module.params["state"], module.params["hostname"], module.params["service_name"]
    ):
        result = dict(
            changed=False,
        )
        module.exit_json(**result)
    else:
        pass

    cmd = [
        "pmm-admin",
        str(module.params["database"]),
    ]

    if module.params["state"] == "present":
        cmd.insert(1, "add")
        if module.params["username"] is not None:
            cmd.append("--username={}".format(module.params["username"]))
        if module.params["password"] is not None:
            cmd.append("--password={}".format(module.params["password"]))
        if module.params["hostname"] is not None:
            cmd.append("--host={}".format(module.params["hostname"]))
        if module.params["port"] is not None:
            cmd.append("--port={}".format(module.params["port"]))
        if module.params["environment"] is not None:
            cmd.append("--environment={}".format(module.params["environment"]))
        if module.params["service_name"] is not None:
            cmd.append("--service-name={}".format(module.params["service_name"]))
    elif module.params["state"] == "absent":
        cmd.insert(1, "remove")
        if module.params["service_name"] is not None:
            cmd.append("{}".format(module.params["service_name"]))

    proc = subprocess.run(" ".join(cmd), shell=True, check=True, capture_output=True)

    if proc.returncode == 0:
        _changed = True
    else:
        _changed = False

    result = dict(
        changed=_changed,
        cmd=cmd,
        stdout_lines=proc.stdout,
        stderr_lines=proc.stderr,
    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
