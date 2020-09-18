from rest_framework import serializers

from PIMSApplication.models import Article


class PimsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id',
                  'SKU',
                  'EAN',
                  'Name',
                  'Stock_quantity',
                  'price',
                  'active')
