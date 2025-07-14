class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")

schema = graphene.Schema(query=Query, mutation=Mutation)
