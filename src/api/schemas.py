from marshmallow import Schema, fields


class UserSchema(Schema):
    password = fields.Str(load_only=True)
    class Meta:
        fields = ("id", "username", "email", "password", "avatar")


class TeamSchema(Schema):
    owner = fields.Nested(UserSchema)
    class Meta:
        fields = ("id", "name", "slug", "owner")


class NotificationSchema(Schema):
    #team = fields.Nested(TeamSchema)
    author = fields.Nested(UserSchema)
    class Meta:
        fields = ("id", "team", "author", "type", "message", "creation_date")
