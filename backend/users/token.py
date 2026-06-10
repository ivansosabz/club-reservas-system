from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ClubTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["is_staff"] = user.is_staff
        token["email"] = user.email
        token["phone"] = user.profile.phone if hasattr(user, "profile") else None
        return token
