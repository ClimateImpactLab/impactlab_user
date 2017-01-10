
import click
# import jinja2


def setup_ssh_keys():
    click.echo('setting up ssh keys')


def setup_osdc():
    click.echo('setting up osdc-comupte')


def setup_brc():
    click.echo('setting up brc')


def setup_osdc_data():
    click.echo('setting up osdc-data')


def setup_aws():
    click.echo('setting up aws')


def setup_datafs():
    click.echo('setting up datafs')


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
def setup(ctx):

    # auth services
    setup_ssh_keys()

    # compute services
    setup_osdc()
    setup_brc()

    # data services
    setup_osdc_data()
    setup_aws()
    setup_datafs()
