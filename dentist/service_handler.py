from json import load
from django.conf import settings as global_settings

from baseapp.models import Language


def service_creator(dentist, Service, Service_category, Service_translation):
    file_path = global_settings.BASE_DIR / "dentist/services.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = load(f)
    for item in data:
        if item['category_id'] is not None:
            service = Service.objects.create(
                dentist=dentist,
                name=item['name']['uz'],
                service_category=Service_category.objects.get(pk=item['category_id']),
                is_editable=False,
                one_tooth=item['one_tooth']
            )
        else:
            service = Service.objects.create(
                dentist=dentist,
                name=item['name']['uz'],
                is_editable=False
            )
        for lang in Language.objects.all():
            service_trans = Service_translation.objects.get(
                service=service,
                language=lang
            )
            service_trans.name = item['name'][lang.name]
            service_trans.save()
            # service_trans = Service_translation.objects.create(
            #     name=item['name'][lang.name],
            #     language=Language.objects.get(name=lang.name),
            #     service=service
            # )


# def get_teeth(patient, Tooth_class):
#     pass
