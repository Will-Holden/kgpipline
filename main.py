import os
from core import MainLoop
import click

# test git
@click.command()
@click.option("batch_size", default=5, help="how many datas execute one time")
def _main(batch_size):
    MainLoop.main_loop(batch_size)


if __name__ == '__main__':
    _main()
