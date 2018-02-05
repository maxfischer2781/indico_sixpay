Installation
============

The plugin can be installed using standard Python package managers.
Note that at least ``indico`` 2.0 is required, and will be installed automatically if it is missing.

After reloading the EPayment plugin in the Indico Admin panel, you can enable the SixPay service.

:note: The ``indico_sixpay`` plugin must be installed for the python version running ``indico``.

Release Version
---------------

The latest release version is available for the default python package managers.
You can directly install the module using ``pip``:

.. code:: bash

    python -m pip install indico_sixpay

This can also be used to upgrade to a newer version:

.. code:: bash

    python -m pip install indico_sixpay --upgrade

Development Version
-------------------

Checkout the `indico_sixpay repository <https://github.com/maxfischer2781/indico_sixpay>`_ to any host running indico.
From its root directory, install the plugin by running:

.. code::

    python setup.py install

:warning: It is not recommended to use the Development Version outside of a testing environment.
