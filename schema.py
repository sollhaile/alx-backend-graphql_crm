import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQl!")

# 👇 This must exist — this is what Graphene is looking for!
schema = graphene.Schema(query=Query)
