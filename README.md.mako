${'#'} 📚 Novelsave Sources

A collection of novel sources offering varying amounts of scraping capability.

> Request a new source by [creating a new issue](https://github.com/mensch272/novelsave_sources/issues/new/choose)

${'##'} 🤖 Usage

${'###'} API

This package exposes 4 basic functions that can be used to interact with the provided
sources, both of novel and metadata variety.

| Function                 | Description                                                  | Parameters   | Returns                  |
| ------------------------ | ------------------------------------------------------------ | ------------ | ------------------------ |
| `novel_source_types`     | Locate and return all the novel source types                 |              | `List[Type[Source]]`     |
| `locate_novel_source`    | Locate and return the novel source parser for the url if it is supported | url:str | `Type[Source]`           |
| `metadata_source_types`  | Locate and return all the metadata source types              |              | `List[Type[MetaSource]]` |
| `locate_metadata_source` | Locate and return the metadata source parser for the url if it is supported | url:str | `Type[MetaSource]`       |

${'####'} Example

Given that you have a novel url you want to parse, you may do the following

```python
import novelsave_sources as nss

# url of the novel you want to parse
url = ...

# tries to find a source that can scrape the provided url
# if not found throws a nss.UnknownSourceException
source = nss.locate_novel_source(url)()

# scrape the website and parse the data into a novel object
novel = source.novel(url)
```

${'###'} Behaviour

${'####'} HttpGateway

`Crawler` type which `Source` extends from takes a `BaseHttpGateway` as a dependency.

The default implementation has the following properties:

- Uses `cloudscraper` package, which detects Cloudflare's anti-bot pages.
- Disables SSL protection, as this seems to break most sites.

You may override this behaviour by implementing `BaseHttpGateway` interface,
and providing it as a dependency when sources are instantiated.

${'###'} Build

To update the sources segment in the README.md, run the following command:

```bash
python3 manage.py compile
```

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
        % for source in sources:
            <tr>
                <td align="center">${source.lang}</td>
                <td>${source.base_urls[0]}</td>
                % if source.search_viable:
                    <td align="center">✅</td>
                % else:
                    <td align="center"></td>
                % endif
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
            <th>Added</th>
        </tr>
    </thead>
    <tbody>
        % for source in rejected:
            <tr>
                <td align="center">${source.lang}</td>
                <td>${source.base_url}</td>
                <td>${source.reason}</td>
                <td>${source.added}</td>
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