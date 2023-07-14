from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.user.serializers import UserAccountSerializer
from apps.user.models import UserAccount, OtpCode

import random


class RegisterUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        ser_data = UserAccountSerializer(data=request.data)

        if ser_data.is_valid():

            username = ser_data.validated_data['username']
            phone_number = ser_data.validated_data['phone_number']
            password = ser_data.validated_data['password']

            try:
                existing_otp = OtpCode.objects.get(phone_number=phone_number)
            except Exception as e:
                existing_otp = None

            if existing_otp is None:
                from apps.user.utils import send_otp_code

                otp_code = random.randint(100000, 999999)
                send_otp_code(phone_number, otp_code)
                OtpCode.objects.create(phone_number=phone_number, code=otp_code)
            else:
                return Response({'message': "your last code has not expired yet. please wait for 2 minutes"},
                                status=status.HTTP_400_BAD_REQUEST)

            request.session['user_registration_info'] = {
                'username': username,
                'phone_number': phone_number,
                'password': password,
            }

            return Response({'message': 'we sent you a code'}, status=status.HTTP_202_ACCEPTED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserVerifyCode(APIView):
    permission_classes = (permissions.AllowAny,)

    # user = UserAccount.objects.create_user(
    #     username=username,
    #     password=password,
    #     phone_number=phone_number,
    # )
    # user.save()
