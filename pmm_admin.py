#!/usr/bin/python

DOCUMENTATION = """
---
module: pmm_admin
short_description: Use pmm-admin to add/remove DB instances to/from PMM2
"""

DOCUMENTATION = """
---
module: pmm_admin

short_description: Use pmm-admin to add DB instances to PMM2. Does not autoconfigure (pmm-admin config)

version_added: "2.9.10"

description:
    - "A module used to add/remove instances to a PMM2 instance. PMM agent needs to be configured on the instance executing it."

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
    service_name:
        description:
            - Service name to be displayed on PMM
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
    port:
        description:
            - Port to use
        required: false
    metrics_mode:
        description:
            - Use either the "push" or "pull" metrics mode. Default is "push".
        required: false



author:
    - Alexandros Orfanos (@aorfanos)
"""

EXAMPLES = """
- name: Add a MySQL service to PMM2
    pmm_admin:
        database: "mysql"
        username: "VAULTME"
        password: "VAULTME"
        hostname: "mysql-001.mydomain.com"
        service_name: "mysql-001"
        environment: staging
        cluster: staging-cluster
        port: 3306
        state: present

- name: Add a ProxySQL service to PMM2
    pmm_admin:
        database: "proxysql"
        username: "VAULTME"
        password: "VAULTME"
        hostname: "proxysql-001.mydomain.com"
        service_name: "proxysql-001"
        environment: production
        cluster: main-cluster
        port: 6032
        state: present

- name: remove a PMM service
    pmm_admin:
        database: "proxysql"
        service_name: "proxysql-001"
        state: absent
"""

RETURN = """
cmd:
    description: List of the command components
    type: str
stdout_lines:
    description: STDOUT of the executed command
stderr_lines:
    description: STDERR of the executed command
"""

ANSIBLE_METADATA = {
    "status": ["preview"],
    "supported_by": "community",
    "metadata_version": "0.1",
}

from ansible.module_utils.basic import AnsibleModule
import subprocess


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
        cluster=dict(type="str", required=False),
        replication_set=dict(type="str", required=False),
        username=dict(type="str", required=False, no_log=True),
        password=dict(type="str", required=False, no_log=True),
        port=dict(type="int", required=False),
        environment=dict(type="str", required=False),
        metrics_mode=dict(type="str", default="push", required=False),
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
        if module.params["metrics_mode"] is not None:
            cmd.append("--metrics-mode={}".format(module.params["metrics_mode"]))
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
