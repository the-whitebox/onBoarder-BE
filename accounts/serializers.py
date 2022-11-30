from rest_framework import serializers
from rest_framework.fields import empty
from django.contrib.auth import get_user_model
from accounts.models import (
    UserProfile
)
# from django.contrib.auth.models import Group
from custom_utilities.helpers import get_base64_image


User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    relative_profile_avatar = serializers.SerializerMethodField(read_only=True)
    encoded_profile_avatar = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.CharField(required=False)
    # full_name = serializers.CharField(required=False)
    # full_name = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_username(obj):
        return obj.user.username

    # @staticmethod
    # def get_full_name(obj):
    #     return obj.user.get_full_name()

    @staticmethod
    def get_user_id(obj):
        return obj.user.id

    @staticmethod
    def get_relative_profile_avatar(obj):
        if obj.profile_avatar:
            return obj.profile_avatar.url

    @staticmethod
    def get_relative_path_profile_avatar(obj):
        if obj.profile_avatar:
            return obj.profile_avatar.path

    @staticmethod
    def get_encoded_profile_avatar(obj):
        image_path = UserProfileSerializer.get_relative_path_profile_avatar(obj)
        return get_base64_image(image_path)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'profile_avatar', 'relative_profile_avatar', 'encoded_profile_avatar', 'display_name', 'state', 'country', 'zip_code', 'email', 'phone_number', 'username',
            'user_name', 'full_name', 'user_id')

    def update(self, instance, validated_data):
        instance.profile_avatar = validated_data.get('profile_avatar', instance.profile_avatar)
        instance.user.username = validated_data.get('user_name', instance.user.username)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        instance.user.save()

        return instance

class UserSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        if instance:
            setattr(self.Meta, 'depth', 1)
        else:
            setattr(self.Meta, 'depth', 0)
        super(UserSerializer, self).__init__(instance, data, **kwargs)

    profile = UserProfileSerializer(required=False)
    user_status = serializers.SerializerMethodField(read_only=True)
    # groups = GroupSerializer(many=True, required=False)
    # company_user_profile = serializers.DictField(required=False)

    class Meta:
        depth = 0
        model = User
        fields = (
            'id', 'url', 'first_name', 'last_name', 'is_superuser', 'is_admin', 'is_client', 'password', 'username',
            'email', 'profile', 'user_status', 'is_active'
        )
        # read_only_fields = ('groups', )
        extra_kwargs = {
            'password': {'write_only': True,
                         'required': False}
        }

    @staticmethod
    def get_user_status(obj):
        return obj.get_user_status()

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile = UserProfile.objects.create(**profile_data)
        password = validated_data.pop('password', None)
        user = User(**validated_data, profile=profile)
        if password:
            user.set_password(password)
        if user.is_superuser:
            user.is_staff = True
        user.save()
        # profile.display_name = user.get_full_name()
        profile.save()

        return user

    def update(self, instance, validated_data):
        # groups_data = validated_data.pop('groups')
        # profile_data = validated_data.pop('profile')


        profile = instance.profile

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_client = validated_data.get('is_client', instance.is_client)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.save()

        # instance.groups.clear()
        # for group_data in groups_data:
        #     # Group.objects.create(user=user, **group_data)
        #     instance.groups.add(group_data)

        # profile.title = profile_data.get('title', profile.title)
        profile.save()

        return instance