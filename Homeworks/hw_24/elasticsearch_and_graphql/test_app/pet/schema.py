import graphene
from graphene_django.types import DjangoObjectType

from test_app.pet.models import Pet
from test_app.client.models import Client


class PetType(DjangoObjectType):
    class Meta:
        model = Pet
        fields = '__all__'


class CreatePet(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        species = graphene.String()
        breed = graphene.String()
        owner_id = graphene.Int()

    pet = graphene.Field(PetType)

    def mutate(self, info, name, species, breed, owner_id=None):
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
    all_pets = graphene.List(PetType)

    def resolve_all_pets(self, info):
        return Pet.objects.all()


class PetMutation(graphene.ObjectType):
    create_pet = CreatePet.Field()

    def resolve_create_pet(self, name, species, breed, owner):
        new_pet = Pet.objects.create(
            name=name,
            species=species,
            breed=breed,
            owner=owner,
        )
        return new_pet


pet_schema = graphene.Schema(query=PetQuery, mutation=PetMutation)
