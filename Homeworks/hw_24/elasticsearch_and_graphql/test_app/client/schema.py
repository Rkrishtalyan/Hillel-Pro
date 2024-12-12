import graphene
from graphene_django.types import DjangoObjectType

from test_app.client.models import Client


class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = '__all__'


class CreateClient(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        is_active = graphene.Boolean()
        registered_at = graphene.DateTime()

    client = graphene.Field(ClientType)

    def mutate(self, info, first_name, last_name, email, is_active, registered_at):
        new_client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            registered_at=registered_at,
        )
        new_client.save()
        return CreateClient(client=new_client)


class ClientQuery(graphene.ObjectType):
    all_clients = graphene.List(ClientType)

    def resolve_all_clients(self, info):
        return Client.objects.all()


class ClientMutation(graphene.ObjectType):
    create_client = CreateClient.Field()

    def resolve_create_client(self, first_name, last_name, email, is_active, registered_at):
        new_client = Client.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=is_active,
            registered_at=registered_at,
        )
        return new_client


schema = graphene.Schema(query=ClientQuery, mutation=ClientMutation)
