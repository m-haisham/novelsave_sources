${'#'} 📚 Novelsave Sources

A collection of novel sources offering varying amounts of scraping capability.

> Request a new source by [creating a new issue](https://github.com/mHaisham/novelsave_sources/issues/new/choose)

${'##'} 🤖 Usage

${'###'} API

This package exposes 4 basic functions that can be used to interact with the provided
sources, both of novel and metadata variety.

- [`novel_source_types`](#novel_source_types) - Locate and return all the novel source types
- [`locate_novel_source`](#locate_novel_source) - Locate and return the novel source parser for the url if it is supported
- [`metadata_source_types`](#metadata_source_types) - Locate and return all the metadata source types
- [`locate_metadata_source`](#locate_metadata_source) - Locate and return the metadata source parser for the url if it is supported

${'####'} novel_source_types

Finds all the novel source implementations defined by this package and returns their types.

`rtype` - `List[Type[Source]]`

${'####'} locate_novel_source

Takes a url and tries to find a defined novel source that can parse the webpage.
If found returns the source type otherwise raises a `UnknownSourceException`.

`rtype` - `Type[Source]`

${'####'} metadata_source_types

Finds all the metadata source implementations defined by this package and returns their types.

`rtype` - `List[Type[MetaSource]]`

${'####'} locate_metadata_source

Takes a url and tries to find a defined metadata source that can parse the webpage.
If found returns the source type otherwise raises a `UnknownSourceException`.

`rtype` - `Type[MetaSource]`

${'###'} Behaviour

${'####'} HttpGateway

`Crawler` type which `Source` extends from takes a `BaseHttpGateway` as a dependency.

The default implementation has the following properties:

- Uses `cloudscraper` package, which detects Cloudflare's anti-bot pages.
- Disables SSL protection, as this seems to break most sites.

You may override this behaviour by implementing `BaseHttpGateway` interface,
and providing it as a dependency when sources are instantiated.

${'##'} 📒 Sources

${'###'} Novel

${'####'} ✅ Supported

<table>
    <thead>
        <tr>
            <th align="center">Lang</th>
            <th>Source</th>
            <th align="center">Search</th>
            <th align="center">Last Checked</th>
        </tr>
    </thead>
    <tbody>
        % for source in sorted(filter(lambda s: not getattr(s, 'rejected', ''), sources), key=lambda s: s.base_urls[0]):
            <tr>
                <td align="center">${source.lang}</td>
                <td>${source.base_urls[0]}</td>
                <td align="center"></td>
                <td align="center">${getattr(source, 'last_updated', '')}</td>
            </tr>
        % endfor
    </tbody>
</table>

${'####'} ❌ Rejected

<table>
    <thead>
        <tr>
            <th align="center">Lang</th>
            <th>Source</th>
            <th>Reason</th>
        </tr>
    </thead>
    <tbody>
        % for source in sorted(filter(lambda s: getattr(s, 'rejected', None), sources), key=lambda s: s.base_urls[0]):
            <tr>
                <td align="center">${source.lang}</td>
                <td>${source.base_urls[0]}</td>
                <td>${source.rejected}</td>
            </tr>
        % endfor
    </tbody>
</table>

${'###'} Metadata

${'####'} ✅ Supported

<table>
    <thead>
        <tr>
            <th align="center">Lang</th>
            <th>Metadata Source</th>
            <th align="center">Last Checked</th>
        </tr>
    </thead>
    <tbody>
        % for source in sorted(meta_sources, key=lambda s: s.base_urls[0]):
            <tr>
                <td align="center">${source.lang}</td>
                <td>${source.base_urls[0]}</td>
                <td align="center">${getattr(source, 'last_updated', '')}</td>
            </tr>
        % endfor
    </tbody>
</table>

${'##'} 📝 Disclaimer

We are not affiliated, associated, authorized, endorsed by, or in any way officially
connected with any of the [sources](#sources) mentioned above.

${'##'} 📜 License

[Apache-2.0](https://github.com/mHaisham/novelsave_sources/blob/master/LICENSE)