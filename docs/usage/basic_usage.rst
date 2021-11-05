Basic usage
###########

Eager to start? This package provides scraping support for a multitude
of light novel sources.

Each scraper has support for scraping novel information and chapter content.
Also provides optional support for search.

You can check which sources are supported at:

* :doc:`../support/supported_novel_sources`
* :doc:`../support/supported_metadata_sources`
* :doc:`../support/rejected_sources`

Let's scrape a novel
********************

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

Now that we have a scraper, lets get finally get to scraping the novel.

.. code-block:: python

    novel = source.novel(url)

While this gives all the chapters, the objects do not yet have any content
in them for that we need to use another method.

.. code-block:: python

    for volume in novel.volumes:
        for chapter in volume.chapters:
            source.chapter(chapter)

Keep in mind that this can take a lot of time. That's it, it's that simple.

Find a novel
************

To get started we need a crawler that supports searching. We
could iterate over all the crawlers until we find one that works
for us. But for the sake of simplicity let's import a specific scraper.

.. code-block:: python

    from novelsave_sources.sources.novel.novelpub import NovelPub

    source = NovelPub()

Great, now we have our scraper. let's search for umm... "solo".

.. code-block:: python

    novels = source.search('solo')

:ref:`search <novel source>` returns a list of novel objects with minimal
information. You will need to do further scraping for chapter list.

Retrieve metadata
*********************

Let's assume you have a url that points toward the correct
metadata source.

.. code-block:: python

    url = ...

At the start, it is similar to scraping a novel. We must
first find a the correct crawler for the url.

.. code-block:: python

    metadata_source = nss.locate_metadata_source(url)()

And then to retrieve all the metadata:

.. code-block:: python

    metadata = metadata_source.retrieve(url)

This gives you a list of metadata objects.
