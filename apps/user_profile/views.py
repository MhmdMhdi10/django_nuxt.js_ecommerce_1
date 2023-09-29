from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Address
from .serializers import UserProfileSerializer, AddressSerializer
from .permissions import IsOwnerOfAddress  # Import the custom permission



class GetUserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = self.request.user
            user_profile = UserProfile.objects.active().get(user=user)
            user_profile_serializer = UserProfileSerializer(user_profile)
            data = {
                'message': 'Profile retrieved successfully',
                'type': 'success',
                'profile': user_profile_serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            data = {
                'message': 'Profile not found',
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data = {
                'message': str(e),
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserAddressView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_profile = UserProfile.objects.active().get(user=request.user)
            addresses = Address.objects.active().filter(user_profile=user_profile)
            address_serializer = AddressSerializer(addresses, many=True)

            data = {
                'message': 'Addresses retrieved successfully',
                'type': 'success',
                'addresses': address_serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            data = {
                'message': 'User profile not found',
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data = {
                'message': str(e),
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        try:
            user_profile = UserProfile.objects.active().get(user=request.user)
            serializer = UserProfileSerializer(
                user_profile, data=request.data, partial=True)  # Allow partial updates

            if serializer.is_valid():
                serializer.save()
                data = {
                    'message': 'Profile updated successfully',
                    'type': 'success',
                    'profile': serializer.data,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'message': 'Invalid data',
                    'type': 'failure',
                    'errors': serializer.errors,
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            data = {
                'message': 'User profile not found',
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data = {
                'message': 'Something went wrong when updating the profile',
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateAddressView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.active().get(user=user)

            request.data["user_profile"] = user_profile.id

            serializer = AddressSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                data = {
                    'message': 'Address created successfully',
                    'type': 'success',
                    'address': serializer.data,
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data = {
                    'message': 'Invalid data',
                    'type': 'failure',
                    'errors': serializer.errors,
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {
                'message': str(e),
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteAddressView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOfAddress)  # Use the custom permission

    def delete(self, request, address_id):
        try:
            address = Address.objects.active().get(id=address_id)  # Remove the user filter here
            if not IsOwnerOfAddress().has_object_permission(request, self, address):  # Explicitly check the permission
                data = {
                    'message': 'Permission denied: You are not the owner of this address',
                    'type': 'failure',
                }
                return Response(data, status=status.HTTP_403_FORBIDDEN)

            address.delete()
            data = {
                'message': 'Address deleted successfully',
                'type': 'success',
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            data = {
                'message': 'Address not found',
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            data = {
                'message': str(e),
                'type': 'failure',
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
