${'#'} 📚 Novelsave Sources

A collection of novel sources offering varying amounts of scraping capability.

> Request a new source by [creating a new issue](https://github.com/mHaisham/novelsave_sources/issues/new/choose)

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