from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime, timedelta
import jwt
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        try:
            if User.objects.filter(email=data["email"]).exists():
                return Response(
                    {"error": "Email already exists"},
                )
            if User.objects.filter(username=data["username"]).exists():
                return Response(
                    {"error": "Username already exists"},
                )
            serializer = UserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user = User.objects.get(username=data["username"])
                cookieData = get_tokens_for_user(user)
                cookieData["is_staff"] = user.is_staff
                response = Response({"error": None})
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=cookieData["access"],
                    expires=300,
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.set_cookie(
                    key="refresh_token",
                    value=cookieData["refresh"],
                    expires=3600 * 24 * 90,
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )

                csrf.get_token(request)
                return response
        except:
            return Response({"error": "server error"}, status=500)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_user_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()
        login = data.get("login", None)
        password = data.get("password", None)

        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            return Response(
                {"error": "Username is not exists"},
                status=403
            )

        user = authenticate(request, username=login, password=password)

        if user is not None:
            data = get_tokens_for_user(user)
            data["is_staff"] = user.is_staff
            response = Response({"error": None})
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=data["access"],
                expires=300,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                expires=3600 * 24 * 90,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            csrf.get_token(request)
            return response

        else:
            return Response(
                {"error": "Invalid password"},
                status=401
            )


class CheckTokenView(APIView):
    def post(self, request, format=None):
        token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            exp_timestamp = decoded_token["exp"]
            if datetime.now().timestamp() < exp_timestamp:
                return JsonResponse({"value": True})
        except (
            jwt.exceptions.DecodeError,
            jwt.exceptions.ExpiredSignatureError,
            KeyError,
        ):
            pass

        return JsonResponse({"value": False}, status=401)


class RefreshTokenView(APIView):
    def post(self, request, format=None):
        refresh_token = request.COOKIES.get("refresh_token")
        access_token = None

        response = JsonResponse({"error": None})

        try:
            show = refresh_token
            token = RefreshToken(refresh_token)
            user = get_user_by_id(token.payload["user_id"])
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            access_token.set_exp(lifetime=timedelta(minutes=5))
            token.blacklist()

        except Exception as e:
            response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
            return JsonResponse({"error": str(e)}, status=401)

        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            expires=300,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            expires=3600 * 60 * 90,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        return response


class LogoutView(APIView):
    def post(self, request, format=None):
        try: 
            print('al')
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            response = Response()

            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value="3",
                expires=datetime(1970, 1, 1),
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.set_cookie(
                key="refresh_token",
                value="4",
                expires=datetime(1970, 1, 1),
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            token.blacklist()
            return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=401)
