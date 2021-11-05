Examples
########

Scraping a novel
****************

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

Searching in specific source
****************************

.. code-block:: python

    from novelsave_sources.sources.novel.novelpub import NovelPub

    # Create the specific source
    source = NovelPub()

    # Search using the query word: 'solo'
    novels = source.search('solo')

Retrieving metadata
*******************

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
**********************************

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
