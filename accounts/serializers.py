from rest_framework import serializers
from home.models import User



class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password','password2')
        extra_kwargs = {
            'password': {'write_only': True,'required': True},
            'email': {'required': True},
            'username': {'required': True}
        }
    def create(self, validated_data):
        return User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('username cant be `admin`')
        return value

    def validate(self, data):
        if data ['password'] != data['password2']:
            raise serializers.ValidationError('passwords do not match')
        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


