from .models import Property


def property_count(request):
    city_1 = 'liverpool'
    count_1 = Property.location.filter_by_loaction(city_1).count()

    city_2 = 'manchester'
    count_2 = Property.location.filter_by_loaction(city_2).count()

    city_3 = 'London'
    count_3 = Property.location.filter_by_loaction(city_3).count()

    city_4 = 'Glasgow'
    count_4 = Property.location.filter_by_loaction(city_4).count()
    
    return {'count_1': count_1, 'count_2': count_2, 'count_3': count_3, 'count_4': count_4 }