# ansible-pmm-admin

An Ansible module to add or remove services in [Percona Monitoring and Management 2](https://www.percona.com/doc/percona-monitoring-and-management/2.x/index.html).

Requirements:

- `pmm-admin` on the host that will be executing the task

## Usage/examples

```yaml
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
        metrics_mode: push
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
        metrics_mode: pull
        state: present

- name: remove a PMM service
    pmm_admin:
        database: "proxysql"
        service_name: "proxysql-001"
        state: absent
```
