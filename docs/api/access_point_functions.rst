Access point functions
######################

This package provides two sets of utility functions for each source type.

It is important to note, that the following functions return the types and
the source instantiating is left to you.

This gives you the opportunity to inject your own http gateway and override the default behaviour.
Check out the :doc:`gateways` section for more information.

Novel
*****

.. autofunction:: novelsave_sources.novel_source_types

.. autofunction:: novelsave_sources.locate_novel_source

MetaData
********

.. autofunction:: novelsave_sources.metadata_source_types

.. autofunction:: novelsave_sources.locate_metadata_source
