import sqlalchemy as sa

# db metadata
metadata = sa.MetaData()

users = sa.Table('users', metadata,
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('username', sa.Unicode(40)),
                 sa.Column('email', sa.Unicode(253)),
                 sa.Column('password', sa.String)
                 )

teams = sa.Table('teams', metadata,
                sa.Column('id', sa.Integer, primary_key=True),
                sa.Column('name', sa.String(255)),
                sa.Column('slug', sa.String(255)),
                sa.Column('owner', None, sa.ForeignKey('users.id'))
                )

teams_users = sa.Table('teams_users', metadata,
                       sa.Column('id', sa.Integer, primary_key=True),
                       sa.Column('team', None, sa.ForeignKey('teams.id')),
                       sa.Column('user', None, sa.ForeignKey('users.id'))
                       )


notifications = sa.Table('notifications', metadata,
                         sa.Column('id', sa.Integer, primary_key=True),
                         sa.Column('team', None, sa.ForeignKey('teams.id')),
                         sa.Column('author', None, sa.ForeignKey('users.id')),
                         sa.Column('type', sa.String(255)),
                         sa.Column('message', sa.Text(convert_unicode=True)),
                         sa.Column('creation_date', sa.DateTime()))