from rest_framework import serializers
from .models import LostOrFound, UploadImage, Category, Subcategory
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')
            
            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            if file_extension:
                import imghdr
                complete_file_name = "%s.%s" % (file_name, file_extension, )
                data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class LostOrFoundListSerializer(serializers.ModelSerializer):
    upload_image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = LostOrFound
        fields = ['id','name', 'item_name', 'upload_image', 'select', 'description']

    def get_name(self, obj):
        return f'{obj.name}'

    def get_upload_image(self, obj):
        try:
            image = obj.uploadimage_set.all().first().upload_image.url
        except:
            image = None
        return image

class UploadImageSerializer(serializers.ModelSerializer):
    upload_image = Base64ImageField(allow_null=True, required=False, use_url=True, allow_empty_file=True)
       
    class Meta:
        model=UploadImage
        fields = ['id', 'upload_image']


class LostOrFoundDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    class Meta:
        model = LostOrFound
        fields = ['id', 'name', 'item_name', 'select', 'phone_number', 'pin_code','latitude', 'longitude', 'category', 'subcategory', 'description', 'images']

    def get_name(self, obj):
        return f'{obj.name}'

    def get_images(self, obj):
        try:
            image = UploadImageSerializer(obj.uploadimage_set, many=True).data
            # im = dict(image[0])
            # d = {}
            # d['id'] = im['id']
            # for i in range(len(im)-1):
            #     string = f'upload_image_{i + 1}'
            #     if im[string] is not None:
            #         d[string] = im[string]
            # image = d       
        except:
            image = None
        return image


class LostOrFoundCreateSerializer(serializers.ModelSerializer):
    SELECT = {'Lost':'lost', 'Found':'found'}
    
    select = serializers.ChoiceField(choices=SELECT)
    class Meta:
        model = LostOrFound
        fields = ['id', 'item_name', 'select', 'phone_number', 'pin_code']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category_name']


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ['id', 'subcategory_name', 'category_id']

class RetreiveCategorySerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'category', 'subcategory']

    def get_category(self, obj):
        cat = CategorySerializer(Category.objects.all(), many=True).data
        return cat

    def get_subcategory(self, obj):
        subcat = SubcategorySerializer(Subcategory.objects.all(), many=True).data
        return subcat

class LostOrFoundUpdateSerializer(serializers.ModelSerializer):
    upload_image = serializers.SerializerMethodField()
    choose = serializers.SerializerMethodField()
    # subcategory = serializers.SerializerMethodField()
    
    class Meta:
        model = LostOrFound
        fields = ['id', 'item_name', 'select', 'phone_number', 'pin_code','latitude', 'longitude', 'description', 'upload_image', 'category', 'subcategory', 'choose']

    def get_upload_image(self, obj):
        try:
            image = UploadImageSerializer(obj.uploadimage_set, many=True).data
            # im = dict(image[0])
            # d = {}
            # d['id'] = im['id']
            # for i in range(len(im)-1):
            #     string = f'upload_image_{i + 1}'
            #     if im[string] is not None:
            #         d[string] = im[string]
            # image = d
        except:
            image = None
        return image

    def get_choose(self, obj):
        b = Category.objects.all()[0]
        return RetreiveCategorySerializer([b], many=True).data

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        # if User.objects.filter(email=data['email']).exists():
        #     raise serializers.ValidationError('email already exists')
        return data

    def validate_email(self, value):
        data = self.get_initial()
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('This email already exists')
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='Email/Username')
    class Meta:
        model = User
        fields = ['email', 'password']

        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if '@gmail.com' in email:
            username = User.objects.filter(email=email).first()
        elif email:
            username = User.objects.filter(username=email).first()
        else:
            raise serializers.ValidationError('Bad credentials.Try again!')
        if not username.check_password(password):
            raise serializers.ValidationError('Bad credentials.Try again!')
        return data