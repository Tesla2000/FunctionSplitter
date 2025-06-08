from __future__ import annotations

from pathlib import Path

from _config import Config
from _transaction import transaction
from config_parser import ConfigCreator
from modify_file import modify_file


def main() -> int:
    config = ConfigCreator().create_config(Config)
    with transaction(config.pos_args):
        return _main(config)


def _main(config: Config) -> int:
    fail = 0
    paths = map(Path, config.pos_args)
    for filepath in filter(lambda path: path.suffix == ".py", paths):
        fail |= modify_file(
            filepath,
            config=config,
        )
    return fail
