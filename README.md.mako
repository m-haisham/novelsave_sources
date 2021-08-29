${'#'} NovelSave Sources

A collection of novel sources offering varying amounts of scraping capability.

> Request a new source by [creating a new issue](https://github.com/mHaisham/novelsave_sources/issues/new/choose)

${'##'} Sources

${'###'} Novel

<table>
    <thead>
        <tr>
            <th>Source</th>
            <th align="center">Search</th>
            <th align="center">Last Checked</th>
        </tr>
    </thead>
    <tbody>
        % for source in sorted(sources, key=lambda s: s.base_urls):
        <tr>
            <td>${source.base_urls[0]}</td>
            <td align="center"></td>
            <td align="center">${getattr(source, 'last_updated', '')}</td>
        </tr>
        % endfor
    </tbody>
</table>

${'####'} Rejected

| Sources                                   | Reason                    |
| ----------------------------------------- | ------------------------- |
| https://www.fanfiction.net                | Cloudflare bot protection |

${'###'} Metadata

<table>
    <thead>
        <tr>
            <th>Metadata Source</th>
            <th align="center">Last Checked</th>
        </tr>
    </thead>
    <tbody>
        % for source in sorted(metasources, key=lambda s: s.base_urls):
        <tr>
            <td>${source.base_urls[0]}</td>
            <td align="center">${getattr(source, 'last_updated', '')}</td>
        </tr>
        % endfor
    </tbody>
</table>

${'##'} Disclaimer

We are not affiliated, associated, authorized, endorsed by, or in any way officially
connected with any of the [sources](#sources) mentioned above.

${'##'} License

[Apache-2.0](https://github.com/mHaisham/novelsave_sources/blob/master/LICENSE)