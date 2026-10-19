### Documentation

Ansible has surprisingly good [documentation](https://docs.ansible.com/ansible/latest/), use it find new modules and how to use a module.

They also have a [best practice](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) that is good to read.



### How to run playbooks

First open `group_vars/all.yml` and replace the commented values so it suits you.

Use the command `ansible-playbook` to run playbooks.

To create instances use `ansible-playbook provision_instances.yml`.

To destroy instances use `ansible-playbook terminate_instances.yml`.

To deploy the database use `ansible-playbook -i hosts.deploy deploy_database.yml`.

To deploy the app with rolling updates use `ansible-playbook -i hosts.deploy deploy_app.yml`.

To deploy the whole production setup over SSH use `ansible-playbook -i hosts.deploy deploy_production.yml`.



### Structure

#### Playbooks

We have 10 playbooks `provision_instances`, `terminate_instances`, `gather_instances`, `security_groups`, `stop_instances`, `start_instances`, `site`, `deploy_database`, `deploy_app` and `deploy_production`.

**provision_instances** is used to create the servers, listed in `roles/provision_instances/vars/main.yml`, on Azure together with their respective security groups, network settings and storage.
It Uses the roles provision_instances that waits for all of the security_groups to be created. It also connects the load balancers ip to your domain name.

**gather__instances** fins all active virtual machines has an ip address connected to it and, adds them to the hosts. After we have run this playbook we can use the following hosts in other playbooks:
- `appserver` only the servers for the app
- `loadbalancer` only the load balancer server
- `database` the database server. The database should be on its own VM, but to save costs we run it on the load balancer VM, so this group contains the same server as `loadbalancer`.

**security_groups** updates the security groups after `gather_instances` has run, when the IP addresses of the servers are known. The groups are first created when the servers are provisioned, with rules that do not know the IP addresses yet, `roles/security_groups/vars/main.yml` has the variables `app_sources` and `lb_sources` for the rules that should only allow the servers.

**terminate_instances** destroys all virtual machines that `gather_instances` finds, and the network interfaces, IP addresses, disks, security groups and network connected to them. Data on the servers is lost.

**stop_instances** stops (deallocates) all VMs in the resource group. A stopped VM costs no compute, you only pay for its disk and IP address, so stop your VMs when you are not working. **start_instances** starts them again. The VMs keep their IP addresses and disks.

**deploy_database** installs Docker on host `database`, starts MySQL in a Docker volume and waits until the app user can log in.

**deploy_app** installs Docker on host `appserver`, performs a rolling deployment with `serial: 1`, verifies `/version` on each app server and then verifies the deployed version through the load balancer.

**deploy_production** imports the database, load balancer and app playbooks so GitHub Actions can run one deploy command after publish.

**site** should run all of your playbooks to setup the whole project from scratch to a running production.



#### Other

**group_vars** contains variable files connected to hosts.

**roles** contains roles used by the playbooks.

**ansible.cfg** configuration for Ansible

**hosts** contains host groups. We only have the host `local` because our Azure servers are dynamic and we use a generated `hosts.deploy` file for the SSH based deploy workflow.
