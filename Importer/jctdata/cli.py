import click

from jctdata import resolver
from jctdata.indexes import factory
from jctdata.lib import loader
from jctdata import settings


@click.command()
@click.argument("mode")
@click.argument("target")
@click.option("-s", "--stage")
@click.option("-o", "--only", "full_pipeline", flag_value=False)
@click.option("-a", "--all", "full_pipeline", flag_value=True, default=True)
def run(mode, target, stage=None, full_pipeline=True):
    processor = MODE_MAP.get(mode)
    if not processor:
        return

    processor(target, stage, full_pipeline)


def resolve(target, stage=None, full_pipeline=True):
    datasource = resolver.SOURCES.get(target)
    if not stage:
        stage = RESOLVE_PIPELINE[-1]

    if full_pipeline:
        for s in RESOLVE_PIPELINE:
            getattr(datasource, s)()
            if s == stage:
                break
    else:
        getattr(datasource, stage)()


def index(target, stage=None, full_pipeline=True):
    if target == "_all":
        indexers = factory.get_all_indexers()
    else:
        indexers = [factory.get_indexer(target)]

    for indexer in indexers:
        if full_pipeline:
            for s in INDEX_PIPELINE:
                getattr(indexer, s)()
                if s == stage:
                    break
        else:
            getattr(indexer, stage)()


def load(target, stage=None, full_pipeline=True):
    if full_pipeline:
        index(target)

    if target == "_all":
        targets = factory.get_all_index_names()
    else:
        targets = [target]

    for t in targets:
        loader.index_latest_with_alias(t, settings.ES_INDEX_SUFFIX)



MODE_MAP = {
    "resolve": resolve,
    "index": index,
    "load": load
}

RESOLVE_PIPELINE = ["gather", "analyse"]
INDEX_PIPELINE = ["gather", "analyse", "assemble"]

if __name__ == "__main__":
    run()