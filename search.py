# coding: utf-8

import sys
import traceback

import click
from pixivpy3 import AppPixivAPI


ILLUST_URL = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}"


@click.command()
@click.argument("keyword")
def search(keyword):
    pixiv = AppPixivAPI()
    json_result = None
    page = 0
    illusts = []

    while True:
        if json_result:
            next_qs = pixiv.parse_qs(json_result.next_url)
            json_result = pixiv.search_illust(**next_qs)
        else:
            json_result = pixiv.search_illust(keyword)

        page += 1

        if "illusts" in json_result and json_result.illusts is not None:
            illusts += json_result.illusts

        if "next_url" not in json_result or json_result.next_url is None:
            break

        sys.stdout.write(".")
        if page % 100 == 0:
            sys.stdout.write("\n")
        sys.stdout.flush()

    sys.stdout.write("\n")
    sys.stdout.write("\t".join(["No", "Bookmarks", "URL", "Title"]))
    sys.stdout.write("\n")

    illusts = sorted(illusts, key=lambda x: x.total_bookmarks, reverse=True)
    for (i, illust) in enumerate(illusts):
        try:
            sys.stdout.write("\t".join([
                str(i),
                str(illust.total_bookmarks),
                ILLUST_URL.format(illust.id),
                illust.title
            ]))
            sys.stdout.write("\n")
        except:
            sys.stderr.write("Exception occured at illust {}".format(
                illust.id))
            sys.stderr.write(traceback.format_exc())


if __name__ == "__main__":
    search()
