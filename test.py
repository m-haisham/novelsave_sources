# local imports
import sys

# from novelsave_sources.sources.novel.novelpub import NovelPub
sys.path.append(r"D:/Git/novelsave_sources")

# from novelsave_sources import novelsave_sources as nss
import novelsave_sources as nss

# The novel url
url = 'https://www.novelpub.com/novel/villainess-is-changing-her-role-to-a-brocon'

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
        print(chapter)
        source.chapter(chapter)
