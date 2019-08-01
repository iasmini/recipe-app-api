from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # extra - allows to configure extra settings in model serializer
        # used to ensure that the password is right with the complexity rules
        extra_kwargs = {'password': {'write_only': True, 'min_length': 1}}

    # see django rest_framework docs
    # when we create the user django restframework will call this create
    # function and it will pass in the validated data that will contain all
    # the data that was passed into our serializer which would be json data
    # that was made in a http post. And it passes it as the as the argument
    # here and then we can use that to query
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
