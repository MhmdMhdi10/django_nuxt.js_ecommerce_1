from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.user.serializers import UserAccountSerializer, OtpCodeSerializer
from apps.user.models import UserAccount, OtpCode
from apps.user.permissions import HasOTPCode
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenRefreshView

import datetime
import random
import pytz


class RegisterUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        ser_data = UserAccountSerializer(data=request.data)

        if ser_data.is_valid():
            username = ser_data.validated_data['username']
            phone_number = ser_data.validated_data['phone_number']
            password = ser_data.validated_data['password']
            re_password = request.data.get('re_password')

            if re_password != password:
                return Response({"type": "failure", 'message': "your passwords doesn't match"},
                                status=status.HTTP_400_BAD_REQUEST)

            # checks for any existing otp code

            try:
                existing_otp = OtpCode.objects.get(phone_number=phone_number)
            except Exception as e:
                existing_otp = None

            # if otp has been expired it will be deleted
            if existing_otp is not None:
                if existing_otp is not None:

                    # checks for code expiration and deletes the code

                    if datetime.datetime.now(tz=pytz.UTC) > existing_otp.created + datetime.timedelta(minutes=2):
                        existing_otp.delete()
                        existing_otp = None

            # sends otp code if none exist in the database with this specific phone_number

            if existing_otp is None:
                from apps.user.otp_sender import send_otp_code

                otp_code = random.randint(100000, 999999)
                send_otp_code(phone_number, otp_code)
                OtpCode.objects.create(phone_number=phone_number, code=otp_code)
            else:
                return Response({"type": "failure",
                                 'message': "your last code has not expired yet. please wait for 2 minutes"},
                                status=status.HTTP_400_BAD_REQUEST)

            # keeps user information in cookies

            request.session['user_registration_info'] = {
                'username': username,
                'phone_number': phone_number,
                'password': password,
            }

            return Response({"type": "success", 'message': 'we sent you a code'}, status=status.HTTP_202_ACCEPTED)
        return Response({"type": "failure", "message": f"{ser_data.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserVerifyCode(APIView):
    permission_classes = (HasOTPCode, )

    def post(self, request):

        ser_data = OtpCodeSerializer(data=request.data)

        user_data = UserAccountSerializer(data=request.data)

        # getting the otp code from database

        if user_data.is_valid():

            try:
                code = OtpCode.objects.get(phone_number=user_data.validated_data['phone_number'])
            except Exception as e:
                code = None

            # permission HasOTPCode checks if the user has any active otp code

            self.check_object_permissions(request, obj=code)

            if ser_data.is_valid():

                # checks for code expiration

                if datetime.datetime.now(tz=pytz.UTC) < code.created + datetime.timedelta(minutes=2):

                    # checks if the code is right

                    if code.code == ser_data.validated_data['code']:
                        user = UserAccount.objects.create_user(
                            username=user_data.validated_data['username'],
                            password=user_data.validated_data['password'],
                            phone_number=user_data.validated_data['phone_number'],
                        )
                        user.save()
                        code.delete()

                        return Response({"type": "success", 'message': 'your account has been created'},
                                        status=status.HTTP_201_CREATED)
                    else:
                        return Response({"type": "failure", 'message': 'the code is not correct'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"type": "failure", 'message': 'this otp code has been expired'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"type": "failure", "message": f"{ser_data.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        try:
            user = UserAccount.objects.get(phone_number=phone_number)
        except Exception as e:
            return Response({"type": "failure", "message": "Phone number doesn't exist"},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.password == password:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Return the tokens in the response
            return Response({
                "type": "success",
                "message": "login successful",
                "access": access_token,
                "refresh": refresh_token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"type": "failure", "message": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(TokenRefreshView):
    pass


class LogoutUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            else:
                return Response({"type": "failure", "message": "Refresh token not provided."},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({"type": "success", "message": "Logout Successful."},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"type": "failure", "message": "Invalid refresh token."},
                            status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request):
        try:
            current_password = request.data.get("current_password")
            new_password = request.data.get("new_password")
            new_re_password = request.data.get("new_re_password")

            username = UserAccountSerializer(request.user).data['username']

            user = UserAccount.objects.get(username=username)

            if user.password == current_password:
                if new_password == new_re_password:
                    user.password = new_password
                    user.save()

                    access_token = RefreshToken(request.auth).access_token
                    access_token.blacklist()

                    return Response({"type": "success",
                                     "message": "password changed successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"type": "failure",
                                     "message": "new_passwords doesn't match"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"type": "failure",
                                 "message": "current password is wrong"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"type": "failure", "message": "Invalid Input"}, status=status.HTTP_400_BAD_REQUEST)


class RecoverPassword(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        try:
            phone_number = request.data.get('phone_number')

            password = UserAccount.objects.get(phone_number=phone_number)

            from apps.user.otp_sender import send_otp_code

            send_otp_code(phone_number, password, message="رمز فعلی شما:")

            return Response({"type": "success", "message": "Your password has been sent to you via sms"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"type": "failure", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class GetCurrentUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user = UserAccountSerializer(request.user)
            user_data = user.data
            user_data.pop('password')

            return Response({"type": "success",
                             'user': user_data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"type": "failure", "message": "data fetching failed. please try again"},
                            status=status.HTTP_409_CONFLICT)


class CheckAuthentication(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({"type": "success", "message": "Authenticated"}, status=status.HTTP_200_OK)
