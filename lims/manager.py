from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, uid, password=None, **extra_fields):
        if not uid:
            raise ValueError('UserID is required!')

        user = self.model(uid=uid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, uid, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is staff true')

        return self.create_user(uid, password, **extra_fields)
