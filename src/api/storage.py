from marshmallow import Schema, fields


class UserSchema(Schema):
    password = fields.Str(load_only=True)
    class Meta:
        fields = ("id", "username", "email", "password")


class TeamSchema(Schema):
    id = fields.Int()
    owner = fields.Nested(UserSchema)
    name = fields.Str()
    slug = fields.Str()

