from graphene import Node, ObjectType, String, Field, Schema, Int
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from core.models import Set, Card


class SetType(DjangoObjectType):
    class Meta:
        model = Set
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }


class CardType(DjangoObjectType):
    class Meta:
        model = Card
        interfaces = (Node,)
        filter_fields = {
            'name': ['exact', 'contains', 'startswith'],
        }


class Query(ObjectType):
    set = Field(SetType, id=String())
    card = Field(CardType, id=String())
    cards = DjangoFilterConnectionField(CardType)

    def resolve_set(parent, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Set.objects.get(pk=id)
        return None

    def resolve_card(parent, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Card.objects.get(pk=id)
        return None


schema = Schema(query=Query)
