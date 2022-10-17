import click
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError

from app.users import db, users
from app.users.models import Role, User


@users.cli.command('create_admin_role')
@with_appcontext
def create_admin_role():
    role = Role.query.filter_by(name='admin').first()
    if not role:
        try:
            db.session.add(Role(name='admin'))
            db.session.commit()
            click.echo('Role created')
        except SQLAlchemyError:
            db.session.rollback()


@users.cli.command('create_role')
@with_appcontext
@click.argument('name')
def create_rol(name):
    role = Role.query.filter_by(name=name).first()
    if role:
        click.echo(f'Role name {name} already exists')
        return
    try:
        db.session.add(Role(name=name))
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()


@users.cli.command('create_admin_user')
@with_appcontext
@click.argument('first_name')
@click.argument('last_name')
@click.argument('email')
@click.password_option()
def create_admin_user(
    first_name,
    last_name,
    email,
    password
):
    role = Role.query.filter_by(name='admin').first()
    if not role:
        click.echo(
            'Role admin not created, '
            'please run create_admin_role command first'
        )
        return

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role_id=role.id
    )
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()

    click.echo('created admin user')
