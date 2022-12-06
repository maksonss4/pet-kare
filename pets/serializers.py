from rest_framework import serializers
from .models import Sexs, Pet
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer
from groups.models import Group
from traits.models import Trait


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=Sexs.choices,
        default=Sexs.DEFAULT,
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    traits_count = serializers.SerializerMethodField()

    def get_traits_count(self, obj):
        return len(obj.traits.all())

    def create(self, validated_data: dict) -> Pet:
        traits_list = validated_data.pop("traits")
        group_dict = validated_data.pop("group")

        pet_obj = Pet.objects.create(**validated_data)

        for trait in traits_list:
            trait_obj, trait_already_exists = Trait.objects.get_or_create(**trait)

            trait_obj.pets.add(pet_obj)

        group_obj, group_already_exists = Group.objects.get_or_create(**group_dict)

        group_obj.pets.add(pet_obj)

        return pet_obj

    def update(self, instance: Pet, validated_data: dict):
        traits_list = validated_data.pop("traits", None)
        group_dict = validated_data.pop("group", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        if traits_list:
            for trait in traits_list:
                trait_obj, trait_already_exists = Trait.objects.get_or_create(
                    **trait,
                )

                trait_obj.pets.add(instance)

        if group_dict:
            group_obj, group_already_exists = Group.objects.get_or_create(**group_dict)

            instance.group = group_obj

        return instance
