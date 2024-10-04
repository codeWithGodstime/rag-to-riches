from rest_framework import viewsets, status, permissions
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView as SimpleJWTTokenObtainPairView


from .serializers import UserSerializer, TokenObtainSerializer
from .models import User
from .utils import generate_token_link, generate_password_reset_message, verify_email_token

class UserViewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self, *args, **kwargs):

        if self.action == 'create':
            return UserSerializer.UserCreateSerializer
        elif self.action == 'list':
            return UserSerializer.UserRetrieveSerializer
        elif self.action == 'retrieve':
            return UserSerializer.UserRetrieveSerializer
        elif self.action == 'reset_password':
            return UserSerializer.UserResetPasswordSerializer
        elif self.action == 'reset_password_confirmation':
            return UserSerializer.UserResetPasswordConfirmationSerializer
        elif self.action == 'change_password':
            return UserSerializer.UserChangePasswordSerializer
        elif self.action == 'verify':
            return UserSerializer.UserVerificationSerializer
        elif self.action == 'update':
            return UserSerializer.UserUpateSerializer

        return super().get_serializer(*args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.filter(email=serializer.validated_data['email']).first()
        reset_link = generate_token_link(user, 'verify')
        message = generate_password_reset_message(user, reset_link)

        user.email_user("Account confirmation link", message, "admin@developer.com")

        return Response({"detail": "User registration is successful, check your email for account verification link"}, status=status.HTTP_201_CREATED)
    
    @action(methods=['post'], detail=False)
    def verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']

        user = verify_email_token(uid, token)
        if not user:
            return Response(dict(errors="Token is not valid"), status=status.HTTP_403_FORBIDDEN)
        
        user.is_active = True
        user.is_verified = True
        user.save()
    
        return Response({"message": "Your account has been verified successfully"}, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, permission_classes=[permissions.AllowAny])
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer = UserSerializer.UserResetPassword(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializer.validated_data['email']).first()
        reset_link = generate_token_link(user, 'reset-password')
        message = generate_password_reset_message(user, reset_link)

        user.email_user("Reset password link", message, "admin@developer.com")
        return Response(dict(message="Password reset link has been sent to your mail"), status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny])
    def reset_password_confirmation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        user = verify_email_token(uid, token)
        if not user:
            return Response(dict(errors="Token is not valid"), status=status.HTTP_403_FORBIDDEN)

        user.set_password(new_password)
        user.save()


        return Response(dict(message="Your password has been reset successfully. You can now log in with your new password"), status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data.get('current_password')
        new_password = serializer.validated_data.get('new_password')

        # Check the current password
        if not user.check_password(current_password):
            return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({"success": "Password has been changed successfully."}, status=status.HTTP_200_OK)
    

class TokenObtainPairView(SimpleJWTTokenObtainPairView):
    serializer_class = TokenObtainSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:

        return super().post(request, *args, **kwargs)

