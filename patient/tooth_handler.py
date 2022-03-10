def teeth_creator(patient, Tooth_class, Tooth_status_class):
    tooth_11 = Tooth_class.objects.create(code=11, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_12 = Tooth_class.objects.create(code=12, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_13 = Tooth_class.objects.create(code=13, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_14 = Tooth_class.objects.create(code=14, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_15 = Tooth_class.objects.create(code=15, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_16 = Tooth_class.objects.create(code=16, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_17 = Tooth_class.objects.create(code=17, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_18 = Tooth_class.objects.create(code=18, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_21 = Tooth_class.objects.create(code=21, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_22 = Tooth_class.objects.create(code=22, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_23 = Tooth_class.objects.create(code=23, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_24 = Tooth_class.objects.create(code=24, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_25 = Tooth_class.objects.create(code=25, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_26 = Tooth_class.objects.create(code=26, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_27 = Tooth_class.objects.create(code=27, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_28 = Tooth_class.objects.create(code=28, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_31 = Tooth_class.objects.create(code=31, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_32 = Tooth_class.objects.create(code=32, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_33 = Tooth_class.objects.create(code=33, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_34 = Tooth_class.objects.create(code=34, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_35 = Tooth_class.objects.create(code=35, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_36 = Tooth_class.objects.create(code=36, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_37 = Tooth_class.objects.create(code=37, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_38 = Tooth_class.objects.create(code=38, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_41 = Tooth_class.objects.create(code=41, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_42 = Tooth_class.objects.create(code=42, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_43 = Tooth_class.objects.create(code=43, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_44 = Tooth_class.objects.create(code=44, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_45 = Tooth_class.objects.create(code=45, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_46 = Tooth_class.objects.create(code=46, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_47 = Tooth_class.objects.create(code=47, status=Tooth_status_class.objects.get(pk=1), patient=patient)
    tooth_48 = Tooth_class.objects.create(code=48, status=Tooth_status_class.objects.get(pk=1), patient=patient)


def get_teeth(patient, Tooth_class):
    teeth = Tooth_class.objects.filter(patient=patient)
    upper_codes = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
    lower_codes = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]
    teeth_upper = []
    teeth_lower = []
    for code in upper_codes:
        teeth_upper.append(
            teeth.filter(code=code).first()
        )
    for code in lower_codes:
        teeth_lower.append(
            teeth.filter(code=code).first()
        )
    return teeth_upper, teeth_lower
