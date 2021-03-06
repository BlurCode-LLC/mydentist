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
        ('3', _("Tekshirtirmaganman"))
    ],
    'anesthesia': [
        ('1', _("Qo'llanilmagan")),
        ('2', "1 marta"),
        ('3', "2 marta"),
        ('4', _("3 va undan ko'proq")),
    ],
    'hepatitis': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Tekshirtirmaganman"))
    ],
    'aids': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Tekshirtirmaganman"))
    ],
    'pressure': [
        ('1', _("Normal")),
        ('2', _("Past")),
        ('3', _("Baland"))
    ],
    'allergy': [
        ('1', _("Yo'q")),
        ('2', _("Bor (nimadanligini yozing)"))
    ],
    'asthma': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'dizziness': [
        ('1', _("Yo'q")),
        ('2', _("Ba‘zan")),
        ('3', _("Tez-tez"))
    ],
    'fainting': [
        ('1', _("Yo'q")),
        ('2', _("Ba‘zan")),
        ('3', _("Tez-tez"))
    ],
    'epilepsy': [
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
        ('2', _("Oz")),
        ('3', _("Ko'p"))
    ],
    'pregnancy': [
        ('1', _("Yo'q")),
        ('2', _("Bor (nechinchi oy)"))
    ],
    'breastfeeding': [
        ('1', _("Yo'q")),
        ('2', _("Ha"))
    ],
    'duration': [
        ("30", _("30 daqiqa")),
        ("60", _("1 soat")),
        ("90", _("1 soat 30 daqiqa")),
        ("120", _("2 soat")),
        ("150", _("2 soat 30 daqiqa")),
        ("180", _("3 soat")),
        ("210", _("3 soat 30 daqiqa")),
        ("240", _("4 soat")),
    ],
    # 'reason': [
    #     ("1", _("Konsultatsiya")),
    #     ("2", _("Tish og‘rig‘i (doimiy)")),
    #     ("3", _("Tish og‘rig‘i (tunda)")),
    #     ("4", _("Tish og‘rig‘i (issiq va sovuqqa)")),
    #     ("5", _("Tish og‘rig‘i (faqat sovuqqa)")),
    #     ("6", _("Tish og‘rig‘i (kovakka ovqat kirib qolganda)")),
    #     ("7", _("Tish og‘rig‘i (tishlaganda)")),
    #     ("8", _("Tish og‘rig‘i (shirinlikda)")),
    #     ("9", _("Tish og‘rig‘i (jag‘ning to'la bir tomonida)")),
    #     ("10", _("Tish og‘rig‘i (ertalab, og‘izni ochganda, yutinganda)")),
    #     ("11", _("Tish qimirlashi")),
    #     ("12", _("Milk qonashi")),
    #     ("13", _("Milk shishishi")),
    #     ("14", _("Isitma")),
    #     ("15", _("Tish ildiz")),
    #     ("16", _("Estetik nuqson (ko‘rinishi yomon)")),
    #     ("17", _("Kovak")),
    #     ("18", _("Tish qo‘ydirish")),
    #     ("19", _("Tishni oldirish")),
    #     ("20", _("Tishlarni tozalatish")),
    #     ("21", _("Implant qo‘ydirish")),
    #     ("22", _("Breket qo'ydirish")),
    #     ("23", _("Protez qildirish")),
    #     ("24", _("Plombalash")),
    #     ("25", _("Boshqa sabab")),
    # ]
}

ILLNESSES = {
    'diabet': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Tekshirtirmaganman"))
    ],
    'anesthesia': [
        ('1', _("Qo'llanilmagan")),
        ('2', "1 marta"),
        ('3', "2 marta"),
        ('4', _("3 va undan ko'proq")),
    ],
    'hepatitis': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Tekshirtirmaganman"))
    ],
    'aids': [
        ('1', _("Yo'q")),
        ('2', _("Bor")),
        ('3', _("Tekshirtirmaganman"))
    ],
    'pressure': [
        ('1', _("Normal")),
        ('2', _("Past")),
        ('3', _("Baland"))
    ],
    'allergy': [
        ('1', _("Yo'q")),
        ('2', _("Bor (nimadanligini yozing)"))
    ],
    'asthma': [
        ('1', _("Yo'q")),
        ('2', _("Bor"))
    ],
    'dizziness': [
        ('1', _("Yo'q")),
        ('2', _("Ba‘zan")),
        ('3', _("Tez-tez"))
    ],
    'fainting': [
        ('1', _("Yo'q")),
        ('2', _("Ba‘zan")),
        ('3', _("Tez-tez"))
    ],
    'epilepsy': [
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
        ('2', _("Oz")),
        ('3', _("Ko'p"))
    ],
    'pregnancy': [
        ('1', _("Yo'q")),
        ('2', _("Bor (nechinchi oy)"))
    ],
    'breastfeeding': [
        ('1', _("Yo'q")),
        ('2', _("Ha"))
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
        'name': _("Navoiy viloyati")
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
