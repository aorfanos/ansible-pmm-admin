# community.aorfanos.pmm_admin

An Ansible module to add or remove services in [Percona Monitoring and Management 2](https://www.percona.com/doc/percona-monitoring-and-management/2.x/index.html).

## Installation

`ansible-galaxy collection install aorfanos.pmm_admin`

## Requirements

- `pmm-admin` executable and in `$PATH` on the host that will be executing the task

## Parameters

| Parameter    | Required | Choices/Defaults                                           | Comments                                                   |
|--------------|----------|------------------------------------------------------------|------------------------------------------------------------|
| cluster      | False    |                            None                            | Cluster name for the service                               |
| database     | True     | Choices:   <ul><li>mysql</li><li>proxysql</li><li>mongodb</li><li>postgresql</li></ul> | Database type                                              |
| environment  | False    | None                                                       | Service environment (e.g. staging)                         |
| state        | True     | Choices:   <ul><li>present (default)</li><li>absent</li></ul>                 |                                                            |
| hostname     | False    | IP or FQDN for the monitored host                          | Is required to add a service, not required for removing it |
| username     | False    | None                                                       |                                                            |
| password     | False    | None                                                       |                                                            |
| metrics_mode | False    | Choices: <ul><li>push (default)</li><li>pull</li></ul>                       | Metrics mode as mentioned in documentation.                |
| port         | False    | None                                                       |                                                            |
| service_name | True     | None                                                       | Name to use for the monitoring service                     |

## Usage/examples

```yaml
- name: Add a MySQL service to PMM2
    community.aorfanos.pmm_admin:
        database: "mysql"
        username: "VAULTME"
        password: "VAULTME"
        hostname: "mysql-001.mydomain.com"
        service_name: "mysql-001"
        environment: staging
        cluster: staging-cluster
        port: 3306
        metrics_mode: push
        state: present

- name: Add a ProxySQL service to PMM2
    community.aorfanos.pmm_admin:
        database: "proxysql"
        username: "VAULTME"
        password: "VAULTME"
        hostname: "proxysql-001.mydomain.com"
        service_name: "proxysql-001"
        environment: production
        cluster: main-cluster
        port: 6032
        metrics_mode: pull
        state: present

- name: remove a PMM service
    community.aorfanos.pmm_admin:
        database: "proxysql"
        service_name: "proxysql-001"
        state: absent
```
