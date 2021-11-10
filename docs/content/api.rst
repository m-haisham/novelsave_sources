API
###

Crawler
*******

.. autoclass:: novelsave_sources.sources.Crawler
    :members: of, init, set_cookies, get_soup, make_soup, request,
        is_blacklisted, clean_contents, clean_element, find_paragraphs, to_absolute_url

Sources
*******

Sources are divided into the groups:

* :ref:`Novel <novel source>`
    Interface to be implemented by primary novel content scrapers
* :ref:`MetaData <metadata source>`
    Interface to be implemented by supplementary metadata scrapers

.. _novel source:

Novel source interface
======================

.. autoclass:: novelsave_sources.Source
    :members: search, login, novel, chapter
    :special-members: __init__
    :show-inheritance:

.. _metadata source:

MetaData source interface
=========================

.. autoclass:: novelsave_sources.MetaSource
    :members: retrieve
    :show-inheritance:

Gateways
********

Http Gateway
============

.. autoclass:: novelsave_sources.utils.gateways.BaseHttpGateway
    :members: request, get, post, cookies

Default http gateway
====================

.. autoclass:: novelsave_sources.utils.gateways.DefaultHttpGateway

Models
******

Novel
=====

.. autoclass:: novelsave_sources.Novel
    :members: get_default_volume, add_metadata

Volume
======

.. autoclass:: novelsave_sources.Volume
    :members: default, add

Chapter
=======

.. autoclass:: novelsave_sources.Chapter

Metadata
========

.. autoclass:: novelsave_sources.Metadata
    :special-members: __init__

Utilities
*********

This package provides two sets of utility functions for each source type.

It is important to note, that the following functions return the types and
the source instantiating is left to you.

This gives you the opportunity to inject your own http gateway and override the default behaviour.
Check out the gateways api section for more information.

Retrieve all novel sources
==========================

.. autofunction:: novelsave_sources.novel_source_types

Find the novel source that can parse a specific url
===================================================

.. autofunction:: novelsave_sources.locate_novel_source

Retrieve all metadata sources
=============================

.. autofunction:: novelsave_sources.metadata_source_types

Find the metadata source that can parse a specific url
======================================================

.. autofunction:: novelsave_sources.locate_metadata_source

Exceptions
**********

.. autoexception:: novelsave_sources.SourcesException

.. autoexception:: novelsave_sources.BadResponseException

.. autoexception:: novelsave_sources.UnknownSourceException

.. autoexception:: novelsave_sources.UnavailableException

.. autoexception:: novelsave_sources.ChapterException
