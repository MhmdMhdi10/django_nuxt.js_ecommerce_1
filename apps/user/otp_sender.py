# from django.contrib.auth.mixins import UserPassesTestMixin
from kavenegar import *

import environ
import os

env = environ.Env()
environ.Env.read_env()

api_key = os.environ.get('KAVEH_KEY')
sender = os.environ.get('KAVEH_SENDER')


def send_otp_code(phone_number, code, message='کد تایید شما'):
	try:
		api = KavenegarAPI(api_key)
		params = {
			'sender': sender,
			'receptor': phone_number,
			'message': f'{code} :{message} '
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)



# class IsAdminUserMixin(UserPassesTestMixin):
# 	def test_func(self):
# 		return self.request.user.is_authenticated and self.request.user.is_admin
