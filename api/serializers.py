from rest_framework import serializers
from rest_framework import validators

from api.models import ApiUser, Warehouse, Product


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    email = serializers.EmailField(validators=[
        validators.UniqueValidator(ApiUser.objects.all())
    ])
    password = serializers.CharField(min_length=6, \
                                     max_length=20, write_only=True)
    user_type = serializers.ChoiceField(choices=ApiUser.USER_TYPE_CHOICES)

    def update(self, instance, validated_data):
        if email := validated_data.get("email"):
            instance.email = email
            instance.save(update_fields=["email"])

        if password := validated_data.get("password"):
            instance.set_password(password)
            instance.save(update_fields=["password"])
        return instance

    def create(self, validated_data):
        user = ApiUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            user_type=validated_data["user_type"],
        )

        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user


class WarehouseSerializer(serializers.Serializer):
    warehouse_name = serializers.CharField(max_length=300, validators=[
        validators.UniqueValidator(Warehouse.objects.all())])

    def create(self, validated_data):
        return Warehouse.objects.create(**validated_data)
class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, validators=[
        validators.UniqueValidator(Product.objects.all())
    ])
    count = serializers.IntegerField()
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
