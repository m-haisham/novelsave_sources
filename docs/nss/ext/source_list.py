from typing import List


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from docutils.parsers.rst import Directive, directives
from docutils import nodes

from novelsave_sources import (
    novel_source_types,
    metadata_source_types,
    rejected_sources,
)


class SourceListDirective(Directive):
    has_content = False
    option_spec = {
        "type": lambda arg: directives.choice(arg, ("novel", "metadata", "rejected"))
    }

    def run(self):
        list_type = self.options.get("type")

        if list_type == "novel":
            table, tgroup = self._table(4)

            self._head(
                tgroup,
                [
                    {"text": "Lang", "align": "center"},
                    {"text": "Source"},
                    {"text": "Search", "align": "center"},
                    {"text": "Last Updated", "align": "center"},
                ],
            )

            self._body(
                tgroup,
                [
                    [
                        {"text": source.lang, "align": "center"},
                        {"text": source.base_urls[0], "link": True},
                        {
                            "text": "✅" if source.search_viable else "",
                            "align": "center",
                        },
                        {"text": str(source.last_updated), "align": "center"},
                    ]
                    for source in sorted(
                        novel_source_types(), key=lambda s: (s.lang, s.base_urls[0])
                    )
                ],
            )
        elif list_type == "metadata":
            table, tgroup = self._table(4)

            self._head(
                tgroup,
                [
                    {"text": "Lang", "align": "center"},
                    {"text": "Source"},
                    {"text": "Last Updated", "align": "center"},
                ],
            )

            self._body(
                tgroup,
                [
                    [
                        {"text": source.lang, "align": "center"},
                        {"text": source.base_urls[0], "link": True},
                        {"text": str(source.last_updated), "align": "center"},
                    ]
                    for source in sorted(
                        metadata_source_types(), key=lambda s: (s.lang, s.base_urls[0])
                    )
                ],
            )
        elif list_type == "rejected":
            table, tgroup = self._table(4)

            self._head(
                tgroup,
                [
                    {"text": "Lang", "align": "center"},
                    {"text": "Source"},
                    {"text": "Reason"},
                    {"text": "Added", "align": "center"},
                ],
            )

            self._body(
                tgroup,
                [
                    [
                        {"text": source.lang, "align": "center"},
                        {"text": source.base_url, "link": True},
                        {"text": source.reason},
                        {"text": str(source.added), "align": "center"},
                    ]
                    for source in sorted(
                        rejected_sources, key=lambda r: (r.lang, r.base_url)
                    )
                ],
            )
        else:
            table = nodes.error(f"Unknown list type: {list_type}")

        return [table]

    def _table(self, cols: int):
        table = nodes.table()
        table["classes"] += ["colwidths-auto"]

        tgroup = nodes.tgroup(cols=cols)
        for _ in range(cols):
            colspec = nodes.colspec(colwidth=1)
            tgroup.append(colspec)

        table += tgroup

        return table, tgroup

    def _head(self, tgroup, options: List[dict]):
        thead = nodes.thead()
        tgroup += thead
        row = nodes.row()

        for col in options:
            entry = nodes.entry()

            try:
                entry["classes"] += ["text-" + col["align"]]
            except KeyError:
                pass

            entry += nodes.paragraph(text=col["text"])
            row += entry

        thead.append(row)
        return thead

    def _body(self, tgroup, options: List[List[dict]]):
        rows = []
        for option in options:
            row = nodes.row()
            rows.append(row)

            for col in option:
                entry = nodes.entry()

                try:
                    entry["classes"] += ["text-" + col["align"]]
                except KeyError:
                    pass

                if col.get("link", False):
                    text_node = nodes.paragraph()
                    text_node += nodes.reference(
                        col["text"], col["text"], refuri=col["text"], internal=False
                    )
                else:
                    text_node = nodes.paragraph(text=col["text"])

                entry += text_node
                row += entry

        tbody = nodes.tbody()
        tbody.extend(rows)
        tgroup += tbody

        return tbody


def setup(app):
    app.add_directive("source-list", SourceListDirective)
