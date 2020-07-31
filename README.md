# Pakaa installer

This repo is
a git and Python environment
to run Ansible playbooks
on localhost
that install my hobby projects
on a Debian 10 host.


## Install the installer

Clone repo and init git and Python environments as root.

    cd /opt
    git clone https://github.com/tessercat/pakaa-installer.git installer
    chmod 0700 installer
    cd installer

    # Roles and playbooks are in git submodules.
    git submodule init
    git submodule update

    apt -y update
    apt -y install python3-venv
    python3 -m venv venv
    . venv/bin/activate
    pip install --upgrade pip wheel pip-tools
    pip-sync requirements.txt


## Run the stack playbook

See the
[`stack-deploy`](https://github.com/tessercat/stack-deploy)
repo's readme
for more information.

Copy vars from the submodule.

    cd /opt/installer
    cp stack-deploy/stack-vars.yml .

Read and edit the copied vars file.

Activate the venv.

    . venv/bin/activate

Run the playbook.

    ansible-playbook stack-deploy/local.yml \
    -i stack-deploy/hosts \
    -e @stack-vars.yml


## Run the daoistic playbook

See the
[`daoistic-deploy`](https://github.com/tessercat/daoistic-deploy)
repo's readme
for more information.

Copy vars from the submodule.

    cd /opt/installer
    cp daoistic-deploy/daoistic-vars.yml .

Read and edit the copied vars file.

Activate the venv.

    . venv/bin/activate

Run the playbook.

    ansible-playbook daoistic-deploy/local.yml \
    -i daoistic-deploy/hosts \
    -e @stack-vars.yml \
    -e @daoistic-vars.yml


## Run the PBX playbook

See the
[`pbx-deploy`](https://github.com/tessercat/pbx-deploy)
repo's readme
for more information.

Copy vars from the submodule.

    cd /opt/installer
    cp pbx-deploy/pbx-vars.yml .

Read and edit the copied vars file.

Activate the venv.

    . venv/bin/activate

Run the playbook.

    ansible-playbook pbx-deploy/local.yml \
    -i pbx-deploy/hosts \
    -e @stack-vars.yml \
    -e @pbx-vars.yml
