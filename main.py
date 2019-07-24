import os
from core import MainLoop
import click

@click.command()
@click.option("batch_size", default=5, help="how many datas execute one time")
if __name__ == '__main__':
    MainLoop.main_loop(batch_size)

