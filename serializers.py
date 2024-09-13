from rest_framework import serializers
from .models import *

class GenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genus
        fields = ['id', 'name', 'slug']

class PlantImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImages
        fields = ['id', 'image']


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ['id', 'name', 'slug', 'common_name']

class SpeciesSerializer(serializers.ModelSerializer):
    genus = serializers.CharField()  # Changed to CharField
    family = serializers.CharField()  # Changed to CharField

    class Meta:
        model = Species
        fields = [
            'id', 'slug', 'common_name', 'scientific_name', 'year',
            'bibliography', 'author', 'status', 'rank', 'family_common_name',
            'genus', 'family', 'image', 'synonyms'
        ]

class MainSpecieImageSerializer(serializers.ModelSerializer):
    images = PlantImagesSerializer(many=True)  # Nested serializer for images

    class Meta:
        model = MainSpecieImage
        fields = ['id', 'name', 'images']

class MainSpeciesSerializer(serializers.ModelSerializer):
    part_images = MainSpecieImageSerializer(many=True)
    class Meta:
        model = MainSpecies
        fields = [
            'id', 'slug', 'common_name', 'scientific_name', 'year',
            'bibliography', 'author', 'status', 'rank', 'family_common_name',
            'genus', 'family', 'observations', 'vegetable', 'thumbnail',
            'duration', 'edible_part', 'edible', 'common_names',
            'flower', 'foliage', 'fruit_or_seed', 'specifications', 'growth', 'part_images',
        ]

class SubSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSpecies
        fields = [
            'id', 'slug', 'common_name', 'scientific_name', 'year',
            'bibliography', 'author', 'status', 'rank', 'family_common_name',
            'genus', 'image', 'synonyms'
        ]

class VarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Variety
        fields = [
            'id', 'slug', 'scientific_name', 'year',
            'bibliography', 'author', 'status', 'rank', 'family_common_name',
            'genus', 'image', 'synonyms', 'family'
        ]

class PlantSerializer(serializers.ModelSerializer):
    main_species = MainSpeciesSerializer()
    species = SpeciesSerializer()
    subspecies = SubSpeciesSerializer(many=True)
    varieties = VarietySerializer(many=True)
    genus = GenusSerializer()
    family = FamilySerializer()

    class Meta:
        model = Plant
        fields = [
            'id', 'slug', 'common_name', 'scientific_name', 'year',
            'bibliography', 'author', 'family_common_name', 'image',
            'observations', 'vegetable', 'main_species', 'subspecies', 'species',
            'varieties', 'edible', 'genus', 'family'
        ]
