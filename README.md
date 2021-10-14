# 📚 Novelsave Sources

A collection of novel sources offering varying amounts of scraping capability.

> Request a new source by [creating a new issue](https://github.com/mHaisham/novelsave_sources/issues/new/choose)

## 🤖 Usage

### API

This package exposes 4 basic functions that can be used to interact with the provided
sources, both of novel and metadata variety.

- [`novel_source_types`](#novel_source_types) - Locate and return all the novel source types
- [`locate_novel_source`](#locate_novel_source) - Locate and return the novel source parser for the url if it is supported
- [`metadata_source_types`](#metadata_source_types) - Locate and return all the metadata source types
- [`locate_metadata_source`](#locate_metadata_source) - Locate and return the metadata source parser for the url if it is supported

#### `novel_source_types`

Finds all the novel source implementations defined by this package and returns their types.

`rtype` - `List[Type[Source]]`

#### `locate_novel_source`

Takes a url and tries to find a defined novel source that can parse the webpage.
If found returns the source type otherwise raises a `UnknownSourceException`.

`rtype` - `Type[Source]`

#### `metadata_source_types`

Finds all the metadata source implementations defined by this package and returns their types.

`rtype` - `List[Type[MetaSource]]`

#### `locate_metadata_source`

Takes a url and tries to find a defined metadata source that can parse the webpage.
If found returns the source type otherwise raises a `UnknownSourceException`.

`rtype` - `Type[MetaSource]`

## 📒 Sources

### Novel

#### ✅ Supported

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
        <tr>
            <td align="center">en</td>
            <td>https://1stkissnovel.love</td>
            <td align="center"></td>
            <td align="center">2021-10-14</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://betwixtedbutterfly.com</td>
            <td align="center"></td>
            <td align="center">2021-10-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://boxnovel.com</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://chrysanthemumgarden.com/</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://creativenovels.com</td>
            <td align="center"></td>
            <td align="center">2021-09-17</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://dragontea.ink/</td>
            <td align="center"></td>
            <td align="center">2021-10-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://dummynovels.com</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://forums.spacebattles.com</td>
            <td align="center"></td>
            <td align="center">2021-09-09</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://forums.sufficientvelocity.com</td>
            <td align="center"></td>
            <td align="center">2021-09-09</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://novelfull.com</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://novelfun.net</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://novelgate.net</td>
            <td align="center"></td>
            <td align="center">2021-09-03</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://novelonlinefull.com</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://novelsite.net</td>
            <td align="center"></td>
            <td align="center">2021-09-06</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://novelsrock.com</td>
            <td align="center"></td>
            <td align="center">2021-09-04</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://peachpitting.com</td>
            <td align="center"></td>
            <td align="center">2021-09-04</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://rainofsnow.com/</td>
            <td align="center"></td>
            <td align="center">2021-09-04</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://readlightnovels.net</td>
            <td align="center"></td>
            <td align="center">2021-09-06</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://wuxiaworld.online</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://wuxiaworld.site</td>
            <td align="center"></td>
            <td align="center">2021-09-03</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.chickengege.org</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.foxaholic.com</td>
            <td align="center"></td>
            <td align="center">2021-09-03</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.lightnovelworld.com</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.mtlnovel.com</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.novelhall.com</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.novelpassion.com</td>
            <td align="center"></td>
            <td align="center">2021-09-04</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.readlightnovel.me</td>
            <td align="center"></td>
            <td align="center">2021-09-07</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.royalroad.com</td>
            <td align="center"></td>
            <td align="center">2021-09-06</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.scribblehub.com</td>
            <td align="center"></td>
            <td align="center">2021-09-06</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.wattpad.com</td>
            <td align="center"></td>
            <td align="center">2021-09-06</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.webnovel.com</td>
            <td align="center"></td>
            <td align="center">2021-09-03</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.wuxiaworld.co</td>
            <td align="center"></td>
            <td align="center">2021-09-04</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.wuxiaworld.com</td>
            <td align="center"></td>
            <td align="center">2021-09-04</td>
        </tr>
    </tbody>
</table>

#### ❌ Rejected

<table>
    <thead>
        <tr>
            <th align="center">Lang</th>
            <th>Source</th>
            <th>Reason</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center">en</td>
            <td>https://www.fanfiction.net</td>
            <td>Has cloudflare bot protection</td>
        </tr>
    </tbody>
</table>

### Metadata

#### ✅ Supported

<table>
    <thead>
        <tr>
            <th align="center">Lang</th>
            <th>Metadata Source</th>
            <th align="center">Last Checked</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center">en</td>
            <td>https://www.novelupdates.com</td>
            <td align="center">2021-09-03</td>
        </tr>
        <tr>
            <td align="center">en</td>
            <td>https://www.wlnupdates.com/</td>
            <td align="center">2021-08-25</td>
        </tr>
    </tbody>
</table>

## 📝 Disclaimer

We are not affiliated, associated, authorized, endorsed by, or in any way officially
connected with any of the [sources](#sources) mentioned above.

## 📜 License

[Apache-2.0](https://github.com/mHaisham/novelsave_sources/blob/master/LICENSE)
