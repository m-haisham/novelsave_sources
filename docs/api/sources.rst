Sources
#######

Sources are divided into the groups:

* :ref:`Novel <novel source>`
* :ref:`MetaData <metadata source>`

.. _novel source:

Novel source interface
**********************

.. autoclass:: novelsave_sources.Source
    :members: __init__, of, search, login, novel, chapter

.. _metadata source:

MetaData source interface
*************************

.. autoclass:: novelsave_sources.MetaSource
    :members: retrieve
