import graphene
from graphene_django.types import DjangoObjectType

from test_app.pet.models import Pet
from test_app.client.models import Client


class PetType(DjangoObjectType):
    """
    Represent the GraphQL type for the Pet model.

    The PetType maps the Django Pet model to a GraphQL type.
    """

    class Meta:
        model = Pet
        fields = '__all__'


class CreatePet(graphene.Mutation):
    """
    Handle the creation of a new Pet instance via GraphQL.

    :param name: The name of the pet.
    :type name: str
    :param species: The species of the pet.
    :type species: str
    :param breed: The breed of the pet.
    :type breed: str
    :param owner_id: The ID of the pet's owner.
    :type owner_id: int, optional
    """

    class Arguments:
        name = graphene.String()
        species = graphene.String()
        breed = graphene.String()
        owner_id = graphene.Int()

    pet = graphene.Field(PetType)

    def mutate(self, info, name, species, breed, owner_id=None):
        """
        Create a new Pet instance and return it.

        :param info: GraphQL context info.
        :param name: The name of the pet.
        :param species: The species of the pet.
        :param breed: The breed of the pet.
        :param owner_id: The ID of the pet's owner (optional).
        :return: The newly created pet.
        :rtype: CreatePet
        """
        owner = None
        if owner_id:
            owner = Client.objects.get(id=owner_id)

        new_pet = Pet(
            name=name,
            species=species,
            breed=breed,
            owner=owner,
        )
        new_pet.save()
        return CreatePet(pet=new_pet)


class PetQuery(graphene.ObjectType):
    """
    Define the queries related to Pet.

    Includes fetching all Pet instances from the database.
    """
    all_pets = graphene.List(PetType)

    def resolve_all_pets(self, info):
        """
        Resolve all_pets query.

        :return: List of all pets.
        :rtype: QuerySet[Pet]
        """
        return Pet.objects.all()


class PetMutation(graphene.ObjectType):
    """
    Define the mutations related to Pet.

    Includes creating a new pet instance.
    """
    create_pet = CreatePet.Field()

    def resolve_create_pet(self, name, species, breed, owner):
        """
        Resolve the create_pet mutation manually.

        :param name: The name of the pet.
        :param species: The species of the pet.
        :param breed: The breed of the pet.
        :param owner: The owner of the pet.
        :return: The newly created Pet instance.
        :rtype: Pet
        """
        new_pet = Pet.objects.create(
            name=name,
            species=species,
            breed=breed,
            owner=owner,
        )
        return new_pet


pet_schema = graphene.Schema(query=PetQuery, mutation=PetMutation)
