from rest_framework_simplejwt.tokens import RefreshToken
from blog.serializers import TokenPairSerializer

def generate_jwt_tokens(user):
    refresh = TokenPairSerializer.get_token(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }