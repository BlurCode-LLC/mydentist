from django.utils.translation import ugettext_lazy as _


CHOICES = {
    'regions': [
        ('1', _("Toshkent")),
        ('2', _("Toshkent viloyati")),
        ('3', _("Samarqand viloyati")),
        ('4', _("Buxoro viloyati")),
        ('5', _("Andijon viloyati")),
        ('6', _("Farg'ona viloyati")),
        ('7', _("Namangan viloyati")),
        ('8', _("Qashqadaryo viloyati")),
        ('9', _("Surxondaryo viloyati")),
        ('10', _("Sirdaryo viloyati")),
        ('11', _("Jizzax viloyati")),
        ('12', _("Xorazm viloyati")),
        ('13', _("Navoiy viloyati")),
        ('14', _("Qoraqalpog'iston Respublikasi")),
    ],
    'gender': [
        ('1', _("Erkak")),
        ('2', _("Ayol"))
    ],
    'diabet': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Bilmadim"))
    ],
    'anesthesia': [
        ('1', "1"),
        ('2', "2"),
        ('3', _("3 va undan ko'proq")),
        ('4', _("Qo'llanilmagan")),
    ],
    'hepatitis': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Bilmadim"))
    ],
    'aids': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Bilmadim"))
    ],
    'pressure': [
        ('1', _("Normal")),
        ('2', _("Past")),
        ('3', _("Baland"))
    ],
    'allergy': [
        ('1', _("Yo'q")),
        ('2', _("Bor (nimagaligini yozing)"))
    ],
    'asthma': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Bilmadim"))
    ],
    'dizziness': [
        ('1', _("Yo'q")),
        ('2', _("Ko'pincha")),
        ('3', _("Ba'zida"))
    ],
    'epilepsy': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'blood_disease': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'medications': [
        ('1', _("Yo'q")),
        ('2', _("Bor (qaysilar)"))
    ],
    'stroke': [
        ('1', _("Yo'q")),
        ('2', _("Ha"))
    ],
    'heart_attack': [
        ('1', _("Yo'q")),
        ('2', _("Ha"))
    ],
    'oncologic': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'tuberculosis': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'alcohol': [
        ('1', _("Yo'q")),
        ('2', _("Ha"))
    ],
    'pregnancy': [
        ('1', _("Yo'q")),
        ('2', _("Bor (nechinchi oy)"))
    ],
    'duration': [
        ("15", _("15 daqiqa")),
        ("30", _("30 daqiqa")),
        ("45", _("45 daqiqa")),
        ("60", _("1 soat")),
        ("75", _("1 soat 15 daqiqa")),
        ("90", _("1 soat 30 daqiqa")),
        ("105", _("1 soat 45 daqiqa")),
        ("120", _("2 soat")),
        ("135", _("2 soat 15 daqiqa")),
        ("150", _("2 soat 30 daqiqa")),
        ("165", _("2 soat 45 daqiqa")),
        ("180", _("3 soat")),
        ("195", _("3 soat 15 daqiqa")),
        ("210", _("3 soat 30 daqiqa")),
        ("225", _("3 soat 45 daqiqa")),
        ("240", _("4 soat")),
    ]
}

GENDERS = [
    _("Erkak"),
    _("Ayol")
]

REGIONS = [
    {
        'value': 1,
        'name': _("Toshkent")
    },
    {
        'value': 2,
        'name': _("Toshkent viloyati")
    },
    {
        'value': 3,
        'name': _("Samarqand viloyati")
    },
    {
        'value': 4,
        'name': _("Buxoro viloyati")
    },
    {
        'value': 5,
        'name': _("Andijon viloyati")
    },
    {
        'value': 6,
        'name': _("Farg'ona viloyati")
    },
    {
        'value': 7,
        'name': _("Namangan viloyati")
    },
    {
        'value': 8,
        'name': _("Qashqadaryo viloyati")
    },
    {
        'value': 9,
        'name': _("Surxondaryo viloyati")
    },
    {
        'value': 10,
        'name': _("Sirdaryo viloyati")
    },
    {
        'value': 11,
        'name': _("Jizzax viloyati")
    },
    {
        'value': 12,
        'name': _("Xorazm viloyati")
    },
    {
        'value': 13,
        'name': _("Navoiy viloyat")
    },
    {
        'value': 14,
        'name': _("Qoraqalpog'iston Respublikasi")
    },
]

MONTHS = [
    _("Yanvar"),
    _("Fevral"),
    _("Mart"),
    _("Aprel"),
    _("May"),
    _("Iyun"),
    _("Iyul"),
    _("Avgust"),
    _("Sentyabr"),
    _("Oktyabr"),
    _("Noyabr"),
    _("Dekabr"),
]

DAYS = [
    _("Dushanba"),
    _("Seshanba"),
    _("Chorshanba"),
    _("Payshanba"),
    _("Juma"),
    _("Shanba"),
    _("Yakshanba"),
]

NEW_LINE = "<br>"
