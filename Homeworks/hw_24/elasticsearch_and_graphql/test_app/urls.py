from django.urls import path
from graphene_django.views import GraphQLView
from test_app.data_document.schema import schema
from test_app.client.schema import schema as client_schema
from test_app.pet.schema import pet_schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('documents/', csrf_exempt(GraphQLView.as_view(schema=schema))),
    path('clients/', csrf_exempt(GraphQLView.as_view(graphiql=False, schema=client_schema))),
    path('pets/', csrf_exempt(GraphQLView.as_view(graphiql=False, schema=pet_schema))),

]
