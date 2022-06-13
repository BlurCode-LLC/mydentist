from json import load
from django.conf import settings as global_settings

from baseapp.models import Language


def service_creator(dentist, Service, Service_category, Service_translation):
    file_path = global_settings.BASE_DIR / "dentist/services.json"
    with open(file_path, "r") as f:
        data = load(f)
    for item in data:
        service = Service.objects.create(
            dentist=dentist,
            name=item['name']['uz'],
            service_category=Service_category.objects.get(pk=item['category_id']),
            is_editable=False
        )
        for lang in Language.objects.all():
            service_trans = Service_translation.objects.create(
                name=item['name'][lang.name],
                language=Language.objects.get(name=lang.name),
                service=service
            )


# def get_teeth(patient, Tooth_class):
#     pass
