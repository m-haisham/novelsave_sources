Usage
#####

Installation
************

You can install the package from the pypi

.. code-block:: bash

    python3 -m pip install novelsave-sources

or directly from github

.. code-block:: bash

    python3 -m pip install git+https://github.com/mensch272/novelsave_sources.git

Basic usage
***********

This package provides scraping support for a multitude
of light novel sources.

Each scraper has support for scraping novel information and chapter content,
while providing optional support for search.

You can check which sources are supported at :doc:`support` section.

Let's scrape a novel
====================

Let's say that we have a url and we have already checked
if the source is available.

.. code-block:: python

    url = ...

We can begin by importing the module

.. code-block:: python

    import novelsave_sources as nss

Now let's get a crawler instance that works with the url above:

.. code-block:: python

    source = nss.locate_novel_source(url)()

In this instance, we arent worried it won't find a matching crawler.

Now that we have a scraper, lets finally get to scraping the novel.

.. code-block:: python

    novel = source.novel(url)

While this gives all the chapters, the objects do not yet have any content
in them for that we need to use another method.

.. code-block:: python

    for volume in novel.volumes:
        for chapter in volume.chapters:
            source.chapter(chapter)

Keep in mind that scraping chapters can take a lot of time depending on the
amount of chapters since it will be downloading each chapter page.

That's it, it's that simple.

Find a novel
============

To get started we need a crawler that supports searching. We
could iterate over all the crawlers until we find one that works
for us. But for the sake of simplicity let's import a specific scraper.

.. code-block:: python

    from novelsave_sources.sources.novel.novelpub import NovelPub

    source = NovelPub()

Great, now we have our scraper. let's search for umm... "solo".

.. code-block:: python

    novels = source.search('solo')

:meth:`search <novelsave_sources.Source.search>` returns a list of novel
objects with minimal information. You will need to do further scraping to
get the chapter list.

Retrieve metadata
=================

Let's assume you have a url that points toward the correct
metadata source.

.. code-block:: python

    url = ...

To start, it is similar to scraping a novel. We must
first find the correct crawler for the url.

.. code-block:: python

    metadata_source = nss.locate_metadata_source(url)()

And then to retrieve all the metadata:

.. code-block:: python

    metadata = metadata_source.retrieve(url)

This gives you a list of metadata objects.

Examples
********

Below are a collection of examples that you may find useful.

Scraping a novel
================

.. code-block:: python

    import novelsave_sources as nss

    # The novel url
    url = ...

    # Get source that can parse the url

    try:
        source = nss.locate_novel_source(url)()
    except nss.UnknownSourceException:  # source not found
        ...

    # Scrape novel information including chapter
    # table of contents
    novel = source.novel(url)

    # Download contents for all the chapters
    for volume in novel.volumes:
        for chapter in volume.chapters:
            source.chapter(chapter)

Searching in a specific source
==============================

.. code-block:: python

    from novelsave_sources.sources.novel.novelpub import NovelPub

    # Create the specific source
    source = NovelPub()

    # Search using the query word: 'solo'
    novels = source.search('solo')

Retrieving metadata
===================

.. code-block:: python

    import novelsave_sources as nss

    # The metadata url
    url = ...

    # Get metadata source to parse the url
    try:
        metadata_source = nss.locate_metadata_source(url)()
    except nss.UnknownSourceException:  # source not found
            ...

    # Retrieve the metadata
    metadata = metadata_source.retrieve(url)

Searching in all supported sources
==================================

.. code-block:: python

    import novelsave_sources as nss

    # Get all source types that can search
    sources = [source() for source in nss.metadata_source_types() if source.search_viable]

    # The search query word
    query = 'solo'

    # Iterate and collect the novels found
    novels = []
    for source in sources:
        novels += source.search(query)
