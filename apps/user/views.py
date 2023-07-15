from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.user.serializers import UserAccountSerializer, OtpCodeSerializer
from apps.user.models import UserAccount, OtpCode
from apps.user.permissions import HasOTPCode


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
                return Response({'message': "your last code has not expired yet. please wait for 2 minutes"},
                                status=status.HTTP_400_BAD_REQUEST)

            # keeps user information in cookies

            request.session['user_registration_info'] = {
                'username': username,
                'phone_number': phone_number,
                'password': password,
            }

            return Response({'message': 'we sent you a code'}, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserVerifyCode(APIView):
    permission_classes = (HasOTPCode, )

    def post(self, request):

        user_session = request.session['user_registration_info']

        ser_data = OtpCodeSerializer(data=request.data)

        # getting the otp code from database

        try:
            code = OtpCode.objects.get(phone_number=user_session['phone_number'])
        except Exception as e:
            code = None

        # permission HasOTPCode checks if the user has any active otp code

        self.check_object_permissions(request, obj=code)

        if ser_data.is_valid():

            # checks for code expiration

            if datetime.datetime.now(tz=pytz.UTC) > code.created + datetime.timedelta(minutes=2):

                # checks if the code is right

                if code.code == ser_data.validated_data['code']:
                    user = UserAccount.objects.create_user(
                        username=user_session['username'],
                        password=user_session['password'],
                        phone_number=user_session['phone_number'],
                    )
                    user.save()
                    code.delete()

                    return Response({'message': 'your account has been created'}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'message': 'the code is not correct'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'this otp code has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)




