from django.core.paginator import Paginator
from rest_framework import status
from .serializers import *
from .models import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response

class ScrapePlantDataAPIView(APIView):
    def post(self, request, *args, **kwargs):
        base_url = "https://trefle.io/api/v1/plants"
        token = "CWFX0xm9Us8cgOzVFgsf2_3hDsFfCsLIDH9ul3BNams"
        page = 1

        def process_plant(plant):
            plant_id = plant['id']
            detail_url = f"{base_url}/{plant_id}?token={token}"
            detail_response = requests.get(detail_url)
            print(detail_url)
            plant_detail = detail_response.json()['data']

            # Process Genus
            genus, _ = Genus.objects.update_or_create(
                slug=plant_detail['genus']['slug'],
                defaults={'name': plant_detail['genus']['name']}
            )

            # Process Family
            family, _ = Family.objects.update_or_create(
                slug=plant_detail['family']['slug'],
                defaults={
                    'name': plant_detail['family']['name'],
                    'common_name': plant_detail['family'].get('common_name')
                }
            )

            # Process MainSpecies
            images_data = plant_detail['main_species'].get('images', {})
            thumbnail_url = plant_detail['main_species'].get('image_url')
            thumbnail_image = None
            if thumbnail_url:
                thumbnail_content = requests.get(thumbnail_url).content
                thumbnail_name = (
                    thumbnail_url.split("/")[-1] if thumbnail_url.split("/")[-1].lower().endswith('.jpg')
                    else thumbnail_url.split("/")[-1] + '.jpg'
                )
                thumbnail_image = ContentFile(thumbnail_content, name=thumbnail_name)

            main_species, _ = MainSpecies.objects.update_or_create(
                slug=plant_detail['main_species']['slug'],
                defaults={
                    'common_name': plant_detail['main_species'].get('common_name'),
                    'scientific_name': plant_detail['main_species'].get('scientific_name'),
                    'year': plant_detail['main_species'].get('year'),
                    'bibliography': plant_detail['main_species'].get('bibliography'),
                    'author': plant_detail['main_species'].get('author'),
                    'status': plant_detail['main_species'].get('status'),
                    'rank': plant_detail['main_species'].get('rank'),
                    'family_common_name': plant_detail['main_species'].get('family_common_name'),
                    'genus': plant_detail['main_species'].get('genus'),
                    'family': plant_detail['main_species'].get('family'),
                    'observations': plant_detail['main_species'].get('observations'),
                    'vegetable': plant_detail['main_species'].get('vegetable', False),
                    'thumbnail': thumbnail_image,  # Save the thumbnail image
                    'duration': plant_detail['main_species'].get('duration'),
                    'edible_part': plant_detail['main_species'].get('edible_part'),
                    'common_names': plant_detail['main_species'].get('common_names', {}).get('eng', []),
                    'edible': plant_detail['main_species'].get('edible', False),
                    'flower': plant_detail['main_species'].get('flower', {}),
                    'foliage': plant_detail['main_species'].get('foliage', {}),
                    'fruit_or_seed': plant_detail['main_species'].get('fruit_or_seed', {}),
                    'specifications': plant_detail['main_species'].get('specifications', {}),
                    'growth': plant_detail['main_species'].get('growth', {}),
                }
            )

            # Get or create Species
            species_obj = None
            species_list = plant_detail.get('species', [])
            if species_list:
                species_data = species_list[0]  # Use the first species if available
                species_image_url = species_data.get('image_url')
                species_image_content = requests.get(
                    species_image_url).content if species_image_url else None
                species_image_file = ContentFile(
                    species_image_content,
                    name=(
                        species_image_url.split("/")[-1] if species_image_url.split("/")[
                            -1].lower().endswith('.jpg')
                        else species_image_url.split("/")[-1] + '.jpg'
                    )
                ) if species_image_content else None

                species_obj, _ = Species.objects.update_or_create(
                    slug=species_data.get('slug'),
                    defaults={
                        'common_name': species_data.get('common_name'),
                        'scientific_name': species_data.get('scientific_name'),
                        'year': species_data.get('year'),
                        'bibliography': species_data.get('bibliography'),
                        'author': species_data.get('author'),
                        'status': species_data.get('status'),
                        'rank': species_data.get('rank'),
                        'family_common_name': species_data.get('family_common_name'),
                        'genus': species_data.get('genus'),
                        'family': species_data.get('family'),
                        'image': species_image_file,
                        'synonyms': species_data.get('synonyms', [])
                    }
                )
                # Get or create SubSpecies
                subspecies_objs = []
                subspecies_list = plant_detail.get('subspecies', [])
                for subspecies_data in subspecies_list:
                    subspecies_image_url = subspecies_data.get('image_url')
                    subspecies_image_content = requests.get(
                        subspecies_image_url).content if subspecies_image_url else None
                    subspecies_image_file = ContentFile(
                        subspecies_image_content,
                        name=(
                            subspecies_image_url.split("/")[-1] if subspecies_image_url.split("/")[-1].lower().endswith(
                                '.jpg')
                            else subspecies_image_url.split("/")[-1] + '.jpg'
                        )
                    ) if subspecies_image_content else None

                    subspecies_obj, _ = SubSpecies.objects.update_or_create(
                        slug=subspecies_data.get('slug'),
                        defaults={
                            'common_name': subspecies_data.get('common_name'),
                            'scientific_name': subspecies_data.get('scientific_name'),
                            'year': subspecies_data.get('year'),
                            'bibliography': subspecies_data.get('bibliography'),
                            'author': subspecies_data.get('author'),
                            'status': subspecies_data.get('status'),
                            'rank': subspecies_data.get('rank'),
                            'family_common_name': subspecies_data.get('family_common_name'),
                            'genus': subspecies_data.get('genus'),
                            'image': subspecies_image_file,
                            'synonyms': subspecies_data.get('synonyms', [])
                        }
                    )
                    subspecies_objs.append(subspecies_obj)


                # Get or create Varieties
                varieties_list = plant_detail.get('varieties', [])
                variety_objs = []
                for variety_data in varieties_list:
                    variety_image_url = variety_data.get('image_url')
                    variety_image_content = requests.get(variety_image_url).content if variety_image_url else None
                    variety_image_file = ContentFile(
                        variety_image_content,
                        name=(
                            variety_image_url.split("/")[-1] if variety_image_url.split("/")[-1].lower().endswith(
                                '.jpg')
                            else variety_image_url.split("/")[-1] + '.jpg'
                        )
                    ) if variety_image_content else None

                    variety_obj, _ = Variety.objects.update_or_create(
                        slug=variety_data.get('slug'),
                        defaults={
                            'scientific_name': variety_data.get('scientific_name'),
                            'year': variety_data.get('year'),
                            'bibliography': variety_data.get('bibliography'),
                            'author': variety_data.get('author'),
                            'status': variety_data.get('status'),
                            'rank': variety_data.get('rank'),
                            'family_common_name': variety_data.get('family_common_name'),
                            'genus': variety_data.get('genus'),
                            'family': variety_data.get('family'),
                            'image': variety_image_file,
                            'synonyms': variety_data.get('synonyms', [])
                        }
                    )
                    variety_objs.append(variety_obj)

            # Process images and associate them with MainSpecies
            for category, image_list in images_data.items():
                for image_data in image_list:
                    image_url = image_data['image_url']
                    image_content = requests.get(image_url).content
                    image_name = (
                        image_url.split("/")[-1] if image_url.split("/")[-1].lower().endswith('.jpg')
                        else image_url.split("/")[-1] + '.jpg'
                    )
                    image_file = ContentFile(image_content, name=image_name)

                    # Save image to PlantImages model
                    plant_image, _ = PlantImages.objects.update_or_create(
                        image=image_file
                    )

                    # Associate images with MainSpecieImage
                    main_specie_image, _ = MainSpecieImage.objects.update_or_create(
                        name=category
                    )
                    main_specie_image.images.add(plant_image)
                    main_species.part_images.add(main_specie_image)

            # Process Plant data and create/update relationships
            plant_image_url = plant_detail.get('image_url')
            plant_image_content = requests.get(plant_image_url).content if plant_image_url else None
            plant_image_file = ContentFile(
                plant_image_content,
                name=(
                    plant_image_url.split("/")[-1] if plant_image_url.split("/")[-1].lower().endswith('.jpg')
                    else plant_image_url.split("/")[-1] + '.jpg'
                )
            ) if plant_image_content else None

            # Create or update Plant and associate relationships
            plant_obj, _ = Plant.objects.update_or_create(
                slug=plant_detail['slug'],
                defaults={
                    'common_name': plant_detail.get('common_name'),
                    'scientific_name': plant_detail.get('scientific_name'),
                    'year': plant_detail.get('year'),
                    'bibliography': plant_detail.get('bibliography'),
                    'author': plant_detail.get('author'),
                    'family_common_name': plant_detail.get('family_common_name'),
                    'image': plant_image_file,  # Save the Plant image
                    'observations': plant_detail.get('observations'),
                    'vegetable': plant_detail.get('vegetable', False),
                    'main_species': main_species,
                    'edible': plant_detail.get('edible', False),
                    'genus': genus,
                    'family': family,
                    'species': species_obj,
                }
            )

            # Associate related species, subspecies, and varieties with the plant
            # plant_obj.species.set(species_objs)
            plant_obj.subspecies.set(subspecies_objs)
            plant_obj.varieties.set(variety_objs)

        while True:
            api_url = f"{base_url}?token={token}&page={page}"
            response = requests.get(api_url)
            data = response.json()

            if not data['data']:
                break  # Exit loop if no more data

            # Create a thread pool to process plant data concurrently
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(process_plant, plant) for plant in data['data']]
                for future in as_completed(futures):
                    future.result()  # This ensures any raised exceptions are handled

            page += 1

        return Response({"message": "Plants data scraped successfully"}, status=200)


class PlantListView(APIView):
    def get(self, request):
        plants = Plant.objects.all()

        # Get the page number from request query parameters, default to 1
        page_number = request.query_params.get('page', 1)

        # Set the number of items per page
        paginator = Paginator(plants, 10)  # Change 10 to the number of items you want per page

        # Get the page
        page_obj = paginator.get_page(page_number)

        # Serialize the plant objects on this page
        serializer = PlantSerializer(page_obj, many=True)

        # Create the response data
        response_data = {
            "status": "success",
            "total_plants": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)