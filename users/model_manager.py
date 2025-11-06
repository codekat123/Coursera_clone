from django.contrib.auth.models import BaseUserManager
from polymorphic.managers import PolymorphicManager


class CustomUserManager(BaseUserManager,PolymorphicManager):

     def create_user(self,username,password,**extrafields):
          if not username:
               raise ValueError('the username field must be set')
          user = self.model(username=username,**extrafields)
          user.set_password(password)
          user.save(using=self.__db)
          return user
     
     def create_superuser(self,username,password,**extrafields):
          extrafields.setdefault('is_staff',True)
          extrafields.setdefault('is_superuser',True)

          if extrafields.get("is_staff") is not True:
              raise ValueError("Superuser must have is_staff as True.")
          if extrafields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser as True.")

          return self.create_user(username, password, **extrafields)