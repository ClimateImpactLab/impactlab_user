
ImpactLab User Setup Tool
=========================

.. image:: https://img.shields.io/pypi/v/impactlab_user.svg
        :target: https://pypi.python.org/pypi/impactlab_user

.. image:: https://travis-ci.org/ClimateImpactLab/impactlab_user.svg?branch=master
        :target: https://travis-ci.org/ClimateImpactLab/impactlab_user?branch=master

.. image:: https://coveralls.io/repos/github/ClimateImpactLab/impactlab_user/badge.svg?branch=master
        :target: https://coveralls.io/github/ClimateImpactLab/impactlab_user?branch=master

.. image:: https://readthedocs.org/projects/impactlab_user/badge/?version=latest
        :target: https://impactlab_user.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/climateimpactlab/impactlab_user/shield.svg
        :target: https://pyup.io/repos/github/climateimpactlab/impactlab_user/
        :alt: Updates

.. image:: https://api.codacy.com/project/badge/Grade/89e3750e62a64dc9b9d6d8930cf5ded9
        :alt: Codacy Badge
        :target: https://www.codacy.com/app/delgadom/impactlab_user?utm_source=github.com&utm_medium=referral&utm_content=ClimateImpactLab/impactlab_user&utm_campaign=badger


Usage
-----

Interactive setup for your machine:

.. code-block:: bash

    $ pip install --upgrade impactlab_user
    $ impactlab-user setup all

You'll need to be ready to configure all Climate Impact Lab tools, specifically:

* OSDC griffin access keys (get these from griffin)
* AWS access keys (get these from Mike or Justin)

Individual subcommands can be run by specifying them:

.. code-block:: bash

    Commands:
      all
      aws
      brc
      datafs
      osdc
      osdc_data
      ssh_keys
