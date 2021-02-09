from rest_framework import serializers
from .models import LostOrFound
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
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='detail', lookup_field='pk'
    # )
    item_image = serializers.SerializerMethodField()
    # delete_url = serializers.HyperlinkedIdentityField(
    #     view_name='detail', lookup_field='pk'
    # )
    name = serializers.SerializerMethodField()
    class Meta:
        model = LostOrFound
        fields = ['id','name', 'item_name', 'item_image', 'select', 'description']

    def get_name(self, obj):
        return f'{obj.name}'

    def get_item_image(self, obj):
        try:
            image = obj.item_image.url
        except:
            image = None
        return image

class LostOrFoundDetailSerializer(serializers.ModelSerializer):
    # delete_url = serializers.HyperlinkedIdentityField(
    #     view_name='detail', lookup_field='pk'
    # )
    name = serializers.SerializerMethodField()
    item_image = serializers.SerializerMethodField()
    class Meta:
        model = LostOrFound
        fields = ['id', 'name', 'item_name', 'item_image', 'phone_number', 'pin_number','latitude', 'longitude', 'category', 'description']

    def get_name(self, obj):
        return f'{obj.name}'

    def get_item_image(self, obj):
        try:
            image = obj.item_image.url
        except:
            image = None
        return image


class LostOrFoundCreateSerializer(serializers.ModelSerializer):
    SELECT = {'Lost':'lost', 'Found':'found'}

    c_id = {'School certificate':'School certificate',
        'College certificate':'College certificate',
        'Company certificate':'Company certificate',
        'College ID':'College ID',
        'Other':'Other'
        }
    e_itm = {
        'Mobile/Phone':'Mobile/Phone',
        'Laptop':'Laptop',
        'Charger':'Charger',
        'Trimmer':'Trimmer',
        'Wifi dongle':'Wifi dongle',
        'Other':'Other'
    }
    bg = {
        'School bag':'School bag',
        'Trolly bag':'Trolly bag',
        'Ladies purse/bag':'Ladies purse/bag',
        'Other':'Other'
    }
    jw_itm = {
        'Necklace':'Necklace',
        'Bracelet':'Bracelet',
        'Ring':'Ring',
        'Earrings':'Earrings',
        'Anklet':'Anklet',
        'Toe ring':'Toe ring',
        'Locket':'Locket'
    }
    CATEGORY = {
        'Bag':'Bag',
        'Certificate and ID':'Certificate and ID',
        'Bank stuff':'Bank stuff',
        'Electronic item':'Electronic item',
        'Jwellary item':'Jwellary item',
        'Trolly':'Trolly',
        'Wallet':'Wallet',
        'Other':'Other'
    }

    category = serializers.ChoiceField(choices=CATEGORY)
    
    select = serializers.ChoiceField(choices=SELECT)


    item_image = Base64ImageField(allow_null=True, required=False, use_url=True, allow_empty_file=True)
    class Meta:
        model = LostOrFound
        fields = ['item_name', 'item_image', 'select', 'category', 'phone_number', 'pin_number','latitude', 'longitude', 'description']

    def get_item_image(self, instance):
        return (instance.item_image.url if instance.item_image else None)

data =  {"item_image":"",
    "item_name":"something",
    "description":"this is description",
    "category":"Found",
    "phone_number":"44444444"
    }

class LostOrFoundUpdateSerializer(serializers.ModelSerializer):
    item_image = Base64ImageField(allow_null=True, required=False, use_url=True, allow_empty_file=True)
    class Meta:
        model = LostOrFound
        fields = ['item_image', 'phone_number', 'description']


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