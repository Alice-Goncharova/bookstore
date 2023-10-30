from api.models import Hotel
from api.serializers import HotelSerializer
s = HotelSerializer(Hotel.objects.create(name = "Test hotel"))
print(s.data)
