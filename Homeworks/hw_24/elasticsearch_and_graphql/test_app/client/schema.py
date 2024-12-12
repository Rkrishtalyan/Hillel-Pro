import graphene
from graphene_django.types import DjangoObjectType

from test_app.client.models import Client


class ClientType(DjangoObjectType):
    """
    Represent the GraphQL type for the Client model.

    The ClientType maps the Django Client model to a GraphQL type.
    """

    class Meta:
        model = Client
        fields = '__all__'


class CreateClient(graphene.Mutation):
    """
    Handle the creation of a new Client instance via GraphQL.

    :param first_name: The first name of the client.
    :type first_name: str
    :param last_name: The last name of the client.
    :type last_name: str
    :param email: The email address of the client.
    :type email: str
    :param is_active: Indicates whether the client is active.
    :type is_active: bool
    :param registered_at: The date and time the client was registered.
    :type registered_at: datetime
    """

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        is_active = graphene.Boolean()
        registered_at = graphene.DateTime()

    client = graphene.Field(ClientType)

    def mutate(self, info, first_name, last_name, email, is_active, registered_at):
        """
        Create a new Client instance and return it.

        :return: The newly created client.
        :rtype: ClientType
        """
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
    """
    Define the queries related to Client.

    Includes fetching all clients from the database.
    """
    all_clients = graphene.List(ClientType)

    def resolve_all_clients(self, info):
        """
        Resolve all clients query.

        :return: List of all clients.
        :rtype: QuerySet[Client]
        """
        return Client.objects.all()


class ClientMutation(graphene.ObjectType):
    """
    Define the mutations related to Client.

    Includes creating a new client.
    """
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
