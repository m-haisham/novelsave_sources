Sources
#######

Sources are divided into the groups:

* :ref:`Novel <novel_source>`
* :ref:`MetaData <metadata_source>`

Novel source interface
**********************

.. autoclass:: novelsave_sources.Source
    :members: __init__, of, search, login, novel, chapter

MetaData source interface
*************************

.. autoclass:: novelsave_sources.MetaSource
    :members: retrieve
