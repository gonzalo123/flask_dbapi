from marshmallow import fields, Schema


class FooSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=False)
