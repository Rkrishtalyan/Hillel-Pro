import graphene
from graphene_django.types import DjangoObjectType

from test_app.data_document.models import DataDocument


class DataDocumentType(DjangoObjectType):
    """
    Represent the GraphQL type for the DataDocument model.

    The DataDocumentType maps the Django DataDocument model to a GraphQL type.
    """

    class Meta:
        model = DataDocument
        fields = '__all__'


class CreateDataDocument(graphene.Mutation):
    """
    Handle the creation of a new DataDocument instance via GraphQL.

    :param title: The title of the data document.
    :type title: str
    :param description: The description of the data document.
    :type description: str
    """

    class Arguments:
        title = graphene.String()
        description = graphene.String()

    data_document = graphene.Field(DataDocumentType)

    def mutate(self, info, title, description):
        """
        Create a new DataDocument instance and return it.

        :return: The newly created DataDocument.
        :rtype: DataDocumentType
        """
        new_document = DataDocument(title=title, description=description)
        new_document.save()
        return CreateDataDocument(data_document=new_document)


class DataDocumentQuery(graphene.ObjectType):
    """
    Define the queries related to DataDocument.

    Includes fetching all DataDocument instances from the database.
    """
    all_data_documents = graphene.List(DataDocumentType)

    # def resolve_all_data(self, info):
    #     return data_document.search.execute()

    def resolve_all_data_documents(self, info):
        """
        Resolve all DataDocument query.

        :return: List of all data documents.
        :rtype: QuerySet[DataDocument]
        """
        return DataDocument.objects.all()


class DataDocumentMutation(graphene.ObjectType):
    """
    Define the mutations related to DataDocument.

    Includes creating a new data document.
    """
    create_data_document = CreateDataDocument.Field()

    # class Arguments:
    #     title = graphene.String()
    #     description = graphene.String()
    #
    # success = graphene.Boolean()
    #
    # def mutate(self, title, description):
    #     data = data_document(title=title, description=description)
    #     data.save()
    #     return Mutation(success=True)

    def resolve_create_data_document(self, title, description):
        """
        Resolve the create_data_document mutation manually.

        :param title: The title of the data document.
        :type title: str
        :param description: The description of the data document.
        :type description: str
        :return: The newly created DataDocument.
        :rtype: DataDocument
        """
        new_document = DataDocument.objects.create(title=title, description=description)
        return new_document


schema = graphene.Schema(query=DataDocumentQuery, mutation=DataDocumentMutation)
