
import click
import os
import yaml
from jinja2 import Template
import ConfigParser


def _recursive_dict_merge(new, default):
    '''
    .. code-block:: python

        >>> new = {
        ...     'a': {
        ...         'b': 1,
        ...         'c': {
        ...             'd': 2
        ...          }
        ...     },
        ...     'e': 3
        ... }
        >>>
        >>> default = {
        ...     'a': {
        ...         'c': {
        ...             'd': 4,
        ...             'f': 5
        ...          }
        ...     },
        ...     'e': 6
        ... }
        >>> _recursive_dict_merge(new, default) == {
        ...     'a': {
        ...         'b': 1,
        ...         'c': {
        ...             'd': 2,
        ...             'f': 5
        ...          }
        ...     },
        ...     'e': 3
        ... }
        True

    '''
    final = {}

    for key in set(new.keys()) | set(default.keys()):
        if key in new:
            if isinstance(new[key], dict):
                final[key] = _recursive_dict_merge(
                    new[key],
                    default.get(key, {}))

            else:
                final[key] = new[key]
        else:
            final[key] = default[key]

    return final


DEFAULT_DATAFS_CONFIG = '''
default-profile: impactlab
profiles:
  impactlab:
    api:
      constructor: {}
      user_config:
        contact: {{contact}}
        name: {{name}}
        team: {{team}}
        institution: {{institution}}

    authorities:
      osdc:
        args: [cil-data]
        kwargs:
          calling_format: \
            !!python/object:boto.s3.connection.OrdinaryCallingFormat {}
          host: griffin-objstore.opensciencedatacloud.org
          profile_name: cil
        service: S3FS
    manager:
      class: DynamoDBManager
      kwargs:
        resource_args: {region_name: us-east-1}
        session_args: {profile_name: cil_dynamo}
        table_name: cil-data

'''


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.group(chain=True, invoke_without_command=True)
@click.pass_context
def setup(ctx):
    pass


@setup.command()
@click.pass_context
def ssh_keys(ctx, *args, **kwargs):
    click.echo('setting up ssh keys')


@setup.command()
@click.pass_context
def osdc(ctx, *args, **kwargs):
    click.echo('setting up osdc-comupte')


@setup.command()
@click.pass_context
def brc(ctx, *args, **kwargs):
    click.echo('setting up brc')


@setup.command()
@click.option('--ACCESS_KEY_ID', default=None)
@click.option('--SECRET_ACCESS_KEY', default=None)
@click.pass_context
def osdc_data(
        ctx,
        ACCESS_KEY_ID=None,
        SECRET_ACCESS_KEY=None,
        *args,
        **kwargs):

    click.echo('setting up osdc-data')

    config = ConfigParser.RawConfigParser()

    config.read(os.path.expanduser('~/.aws/credentials'))

    if 'cil' not in config.sections():
        config.add_section('cil')

        if ACCESS_KEY_ID is None:
            ACCESS_KEY_ID = click.prompt(
                'Your OSDC ACCESS_KEY_ID (get this from griffin)')

        config.set(
            'cil', 'aws_access_key_id', ACCESS_KEY_ID)

        if SECRET_ACCESS_KEY is None:
            SECRET_ACCESS_KEY = click.prompt(
                'Your OSDC SECRET_ACCESS_KEY (get this from griffin)')

        config.set(
            'cil', 'aws_secret_access_key', SECRET_ACCESS_KEY)

    # Writing our configuration file to 'example.cfg'
    # This is a joined split test so our tests can mock os.path.expanduser
    if not os.path.isdir(os.path.join(os.path.expanduser('~/'), '.aws')):
        os.makedirs(os.path.join(os.path.expanduser('~/'), '.aws'))

    with open(
            os.path.join(os.path.expanduser('~/'), '.aws/credentials'),
            'wb') as configfile:

        config.write(configfile)


@setup.command()
@click.option('--AWS_ACCESS_KEY_ID', default=None)
@click.option('--AWS_SECRET_ACCESS_KEY', default=None)
@click.pass_context
def aws(
        ctx,
        AWS_ACCESS_KEY_ID=None,
        AWS_SECRET_ACCESS_KEY=None,
        *args,
        **kwargs):

    click.echo('setting up aws')

    config = ConfigParser.RawConfigParser()

    config.read(os.path.expanduser('~/.aws/credentials'))

    if 'cil_dynamo' not in config.sections():
        config.add_section('cil_dynamo')

        if AWS_ACCESS_KEY_ID is None:
            AWS_ACCESS_KEY_ID = click.prompt(
                'Your amazon AWS_ACCESS_KEY_ID (get this from Justin)')

        config.set(
            'cil_dynamo', 'aws_access_key_id', AWS_ACCESS_KEY_ID)

        if AWS_SECRET_ACCESS_KEY is None:
            AWS_SECRET_ACCESS_KEY = click.prompt(
                'Your amazon AWS_SECRET_ACCESS_KEY (get this from Justin)')

        config.set(
            'cil_dynamo', 'aws_secret_access_key', AWS_SECRET_ACCESS_KEY)

    # Writing our configuration file to 'example.cfg'
    # This is a joined split test so our tests can mock os.path.expanduser
    if not os.path.isdir(os.path.join(os.path.expanduser('~'), '.aws')):
        os.makedirs(os.path.join(os.path.expanduser('~'), '.aws'))

    with open(
            os.path.join(os.path.expanduser('~/'), '.aws/credentials'),
            'wb') as configfile:

        config.write(configfile)


@setup.command()
@click.option('--name', default=None)
@click.option('--contact', default=None)
@click.option('--team', default=None)
@click.option('--institution', default=None)
@click.pass_context
def datafs(ctx, name, contact, team, institution):
    click.echo('setting up datafs'.format(name))

    config_file = os.path.join(click.get_app_dir('datafs'), 'config.yml')
    if not os.path.isdir(os.path.dirname(config_file)):
        os.makedirs(os.path.dirname(config_file))

    current_config = {}
    current_user_config = {}

    if os.path.isfile(config_file):
        with open(config_file, 'r') as conf:
            try:
                contents = yaml.load(conf.read())
                assert isinstance(contents, dict)
                current_config = contents
                current_user_config = current_config['profiles'][
                    current_config['default-profile']]['api']['user_config']

            except:
                pass

    if name is None:
        name = click.prompt(
            'Your full name',
            current_user_config.get('name'))

    if contact is None:
        contact = click.prompt(
            'Your email address',
            current_user_config.get('contact'))

    if team is None:
        team = click.prompt(
            'Your team name (e.g. labor, management)',
            current_user_config.get('team'))

    if institution is None:
        institution = click.prompt(
            'Your institution (e.g. Berkeley)',
            current_user_config.get('institution'))

    user_config = {
        'name': name,
        'contact': contact,
        'team': team,
        'institution': institution}

    template = Template(DEFAULT_DATAFS_CONFIG)
    user_config_file = template.render(**user_config)
    new_user_config = yaml.load(user_config_file)

    config = _recursive_dict_merge(current_config, default=new_user_config)

    with open(config_file, 'w+') as conf:
        conf.write(yaml.dump(config))


@setup.command()
@click.pass_context
def all(ctx):
    ctx.forward(ssh_keys)
    ctx.forward(osdc)
    ctx.forward(brc)
    ctx.forward(osdc_data)
    ctx.forward(aws)
    ctx.forward(datafs)
