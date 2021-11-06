${'#'} 📚 Novelsave Sources

![PyPI](https://img.shields.io/pypi/v/novelsave_sources)
![Python Version](https://img.shields.io/badge/Python-v3.8-blue)
![Repo Size](https://img.shields.io/github/repo-size/mensch272/novelsave_sources)
[![Contributors](https://img.shields.io/github/contributors/mensch272/novelsave_sources)](https://github.com/mensch272/novelsave_sources/graphs/contributors)
![Last Commit](https://img.shields.io/github/last-commit/mensch272/novelsave_sources/main)
![Issues](https://img.shields.io/github/issues/mensch272/novelsave_sources)
![Pull Requests](https://img.shields.io/github/issues-pr/mensch272/novelsave_sources)
[![License](https://img.shields.io/github/license/mensch272/novelsave_sources)](LICENSE)
[![Tests](https://github.com/mensch272/novelsave_sources/actions/workflows/tests.yml/badge.svg)](https://github.com/mensch272/novelsave_sources/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/novelsave-sources/badge/?version=latest)](https://novelsave-sources.readthedocs.io/en/latest/?badge=latest)

A collection of novel sources offering varying amounts of scraping capability.

Read the [docs](https://novelsave-sources.readthedocs.io/en/latest/) for more information.

> Request a new source by [creating a new issue](https://github.com/mensch272/novelsave_sources/issues/new/choose)

${'###'} Development

Make sure you complete the following before you start development:

1. Install poetry as described in their [documentation](https://python-poetry.org/docs/#installation).

2. Install all project dependencies

    ```bash
    poetry install
    ```

3. And setup git hooks by running

    ```bash
    pre-commit install
    ```

___

If you have updated a source make sure to update the
sources segment in the README.md by running the following command:

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
