# Rolling deployment with Ansible

## What it is
A rolling deployment strategy updates one application server at a time instead of replacing the whole production stack at once. In this Microblog setup it means the load balancer temporarily removes one app server, the server gets the new container version, the deployment verifies `/version` locally on that server, and then the server is added back before the next one is updated.

## How to use it in Microblog
1. Provision and bootstrap the Azure hosts with the Ansible playbooks in `ansible/`.
2. Publish a versioned production image to Docker Hub.
3. Run `ansible/deploy_production.yml`, which imports `deploy_database.yml`, `deploy_lb.yml`, and `deploy_app.yml`.
4. In `deploy_app.yml`, the play runs with `serial: 1`, rebuilds the upstream host list, delegates the Nginx update to the load balancer, deploys the current app server, verifies `/version`, and re-adds the server to the upstream.
5. The CD workflow in `.github/workflows/cd.yml` triggers the same deploy playbook after the publish job succeeds.

## How it relates to DevOps
Rolling deployment fits DevOps because it turns production rollout into repeatable automation with verification built in. It also reduces release risk: one node is updated at a time, which avoids the full downtime that a recreate strategy would cause. The verification step against `/version` gives fast feedback and makes the deployment observable rather than trust-based.

## Captured output
These images were generated from the real commands used in this repo.

![Rolling deployment task list](docs/images/kmom03-rolling-tasks.png)

![Live production proof](docs/images/kmom03-live-proof.png)
