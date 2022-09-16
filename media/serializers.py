from rest_framework import serializers
from .models import MyUser, Employee, Profile


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = MyUser(email=self.validated_data['email'], name=self.validated_data['name'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = MyUser
        fields = '__all__'

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error': 'Please enter valid credentials'})


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

