Sources
#######

Sources are divided into the groups:

* :ref:`Novel <novel source>`
    Interface to be implemented by primary novel content scrapers
* :ref:`MetaData <metadata source>`
    Interface to be implemented by supplementary metadata scrapers

.. _novel source:

Novel source interface
**********************

.. autoclass:: novelsave_sources.Source
    :members: search, login, novel, chapter
    :special-members: __init__
    :show-inheritance:

.. _metadata source:

MetaData source interface
*************************

.. autoclass:: novelsave_sources.MetaSource
    :members: retrieve
    :show-inheritance:
