# Pakaa installer

This repo is
a Python environment
to run Ansible playbooks
on localhost
that install my art projects
on an Ubuntu 20.04 host.


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

See the `stack-deploy` repo's readme
for more information.

Copy vars from the submodule.

    cd /opt/installer
    cp stack-deploy/stack-vars.yml .

Read and edit the copied vars file.

Run the playbook.

    . venv/bin/activate
    ansible-playbook stack-deploy/local.yml \
    -i stack-deploy/hosts \
    -e @stack-vars.yml


## Run the peers playbook

See the `peers-deploy` repo's readme
for more information.

Copy vars from the submodule.

    cd /opt/installer
    cp peers-deploy/peers-vars.yml .

Read and edit the copied vars file.

Run the playbook.

    . venv/bin/activate
    ansible-playbook peers-deploy/local.yml \
    -i peers-deploy/hosts \
    -e @stack-vars.yml \
    -e @peers-vars.yml


## Run the daoistic playbook

See the `daoistic-deploy` repo's readme
for more information.

Copy vars from the submodule.

    cd /opt/installer
    cp daoistic-deploy/daoistic-vars.yml .

Read and edit the copied vars file.

Run the playbook.

    . venv/bin/activate
    ansible-playbook daoistic-deploy/local.yml \
    -i daoistic-deploy/hosts \
    -e @stack-vars.yml \
    -e @daoistic-vars.yml
