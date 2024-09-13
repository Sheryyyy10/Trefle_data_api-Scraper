from django.db import models

class Genus(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Family(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class PlantImages(models.Model):
    image = models.ImageField(max_length=1500, upload_to='plant/images/', blank=True, null=True)


class MainSpecieImage(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    images = models.ManyToManyField('PlantImages', blank=True)


class MainSpecies(models.Model):
    slug = models.SlugField(unique=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    bibliography = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    rank = models.CharField(max_length=255, blank=True, null=True)
    family_common_name = models.CharField(max_length=255, blank=True, null=True)
    genus = models.TextField(blank=True, null=True)
    family = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    vegetable = models.BooleanField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='main_species_thumbnail/', blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    edible_part = models.CharField(max_length=255, blank=True, null=True)
    edible = models.BooleanField(blank=True, null=True)
    common_names = models.JSONField(default=list, blank=True, null=True)
    flower = models.JSONField(blank=True, null=True)
    foliage = models.JSONField(blank=True, null=True)
    fruit_or_seed = models.JSONField(blank=True, null=True)
    specifications = models.JSONField(blank=True, null=True)
    growth = models.JSONField(blank=True, null=True)
    part_images  = models.ManyToManyField('MainSpecieImage', blank=True)

    def __str__(self):
        return self.scientific_name



class Species(models.Model):
    slug = models.SlugField(unique=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    bibliography = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    rank = models.CharField(max_length=255, blank=True, null=True)
    family_common_name = models.CharField(max_length=255, blank=True, null=True)
    genus = models.TextField( blank=True, null=True)
    family = models.TextField(blank=True, null=True)
    image = models.ImageField(max_length=1500, upload_to='specie_images/', blank=True, null=True)
    synonyms = models.JSONField(default=list, blank=True, null=True)
    # Add any other fields as needed

    def __str__(self):
        return self.common_name or self.scientific_name

class SubSpecies(models.Model):
    slug = models.SlugField(unique=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    bibliography = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    rank = models.CharField(max_length=255, blank=True, null=True)
    family_common_name = models.CharField(max_length=255, blank=True, null=True)
    genus = models.TextField(blank=True, null=True)  # or use a ForeignKey if applicable
    image = models.ImageField(max_length=1500, upload_to='subspecie_images/', blank=True, null=True)
    synonyms = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.scientific_name


class Variety(models.Model):
    slug = models.SlugField(unique=True)
    scientific_name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    bibliography = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    rank = models.CharField(max_length=255, blank=True, null=True)
    family_common_name = models.CharField(max_length=255, blank=True, null=True)
    genus = models.CharField(max_length=255, blank=True, null=True)
    family = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(max_length=1500, upload_to='variety_images/', blank=True, null=True)
    synonyms = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.scientific_name

class Plant(models.Model):
    slug = models.SlugField(unique=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    scientific_name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    bibliography = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    family_common_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(max_length=1500, upload_to='plant_images', blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    vegetable = models.BooleanField(blank=True, null=True)
    main_species = models.ForeignKey(MainSpecies, on_delete=models.CASCADE, blank=True, null=True)
    # duration = models.CharField(max_length=255, blank=True, null=True)
    # edible_part = models.CharField(max_length=255, blank=True, null=True)
    edible = models.BooleanField(blank=True, null=True)
    genus = models.ForeignKey(Genus, on_delete=models.CASCADE, blank=True, null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, blank=True, null=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, blank=True, null=True)
    subspecies = models.ManyToManyField(SubSpecies, blank=True,)
    varieties = models.ManyToManyField(Variety, blank=True,) # Changed to ManyToManyField
    # images = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.common_name or self.scientific_name


