import sqlalchemy as sa

# db metadata
metadata = sa.MetaData()

users = sa.Table('users', metadata,
                 sa.Column('id', sa.Integer, primary_key=True),
                 sa.Column('username', sa.Unicode(40)),
                 sa.Column('email', sa.Unicode(253)),
                 sa.Column('password', sa.String)
                 )

# users_auth = sa.Table('users_auth', metadata,
#                       sa.Column('id', sa.Integer, primary_key=True),
#                       sa.Column('user_id', None, sa.ForeignKey('users.id')),
#                       sa.Column('salt', sa.LargeBinary, nullable=False),
#                       sa.Column('key', sa.LargeBinary, nullable=False)
#                       )

notifications = sa.Table('notifications', metadata,
                         sa.Column('id', sa.Integer, primary_key=True),
                         sa.Column('author_id', None, sa.ForeignKey('users.id')),
                         sa.Column('message', sa.Text(convert_unicode=True)),
                         sa.Column('creation_date', sa.DateTime()))