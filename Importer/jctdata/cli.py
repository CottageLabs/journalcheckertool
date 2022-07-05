import click

from jctdata import resolver
from jctdata.indexes import factory


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
        stage = "analyse"

    if full_pipeline:
        for s in RESOLVE_PIPELINE:
            getattr(datasource, s)()
            if s == stage:
                break
    else:
        getattr(datasource, stage)()


def index(target, stage=None, full_pipeline=True):
    indexer = factory.get_indexer(target)

    if full_pipeline:
        for s in INDEX_PIPELINE:
            getattr(indexer, s)()
            if s == stage:
                break
    else:
        getattr(indexer, stage)()


def load():
    pass


MODE_MAP = {
    "resolve": resolve,
    "index": index,
    "load": load
}

RESOLVE_PIPELINE = ["gather", "analyse"]
INDEX_PIPELINE = ["gather", "analyse", "assemble"]

if __name__ == "__main__":
    run()