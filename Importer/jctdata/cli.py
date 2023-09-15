import click

from jctdata import resolver
from jctdata.indexes import factory
from jctdata.lib import loader
from jctdata import settings


@click.command()
@click.argument("mode")
@click.argument("targets", nargs=-1)
@click.option("-s", "--stage")
@click.option("-o", "--only", "full_pipeline", flag_value=False)
@click.option("-a", "--all", "full_pipeline", flag_value=True, default=True)
@click.option("-f", "--force-resolve", is_flag=True)
def entry_point(mode, targets, stage=None, full_pipeline=True, force_resolve=False):
    run(mode, targets, stage, full_pipeline, force_resolve)


def run(mode:str, targets:tuple, stage:str=None, full_pipeline:bool=True, force_resolve:bool=False):
    processor = MODE_MAP.get(mode)
    if not processor:
        return

    processor(targets, stage, full_pipeline, force_resolve)


def resolve(targets, stage=None, full_pipeline=True, force_resolve=False):
    if targets[0] == "_all":
        targets = resolver.SOURCES.keys()

    for target in targets:
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


def index(targets, stage=None, full_pipeline=True, force_resolve=False):
    if targets[0] == "_all":
        indexers = factory.get_all_indexers()
    else:
        indexers = [factory.get_indexer(target) for target in targets]

    for indexer in indexers:
        if full_pipeline:
            for s in INDEX_PIPELINE:
                if s == "gather" and force_resolve:
                    getattr(indexer, s)(force=True)
                else:
                    getattr(indexer, s)()
                if s == stage:
                    break
        else:
            getattr(indexer, stage)()


def load(targets, stage=None, full_pipeline=True, force_resolve=False):
    if targets[0] == "_all":
        targets = factory.get_all_index_names()

    if full_pipeline:
        index(targets)

    for t in targets:
        load_type = settings.INDEX_LOADERS[t]
        if load_type == "es":
            loader.index_latest_with_alias(t, settings.ES_INDEX_SUFFIX)
        elif load_type == "file":
            loader.load_to_file(t)
        elif load_type == "helpdesk":
            loader.load_to_helpdesk(t)



MODE_MAP = {
    "resolve": resolve,
    "index": index,
    "load": load
}

RESOLVE_PIPELINE = ["gather", "analyse"]
INDEX_PIPELINE = ["gather", "analyse", "assemble"]

if __name__ == "__main__":
    entry_point()