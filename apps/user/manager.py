from django.contrib.auth.base_user import BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)

        user.set_password(password)
        user.save()

        # import the models here to avoid circular import
        from apps.cart.models import Cart
        from apps.user_profile.models import UserProfile
        from apps.wishlist.models import Wishlist

        shopping_cart = Cart.objects.create(user=user)
        shopping_cart.save()

        profile = UserProfile.objects.create(user=user)
        profile.save()

        wishlist = Wishlist.objects.create(user=user)
        wishlist.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
