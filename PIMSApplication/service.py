from django.http import JsonResponse
from rest_framework import status

from PIMSApplication.models import Article


class ArticleService():
    def __init__(self):
        pass
    def get_all_active_articles(self):
        list_of_articles=Article.objects.all()
        list_of_active_articles=list()
        for item in (list_of_articles):
            if item.active==True:
                list_of_active_articles.append(item)
        return list_of_active_articles

    def get_all_articles(self):
        list_of_articles=Article.objects.all()
        return list_of_articles

    def disable_category_of_articles(self,request_payload):
        category = request_payload.get('category', None)
        article_list = Article.objects.all()
        update_category={
            category:False
        }
        for item in article_list:
            object = Article.objects.get(SKU=item.SKU)
            object.Name.update(update_category)
            object.save()
        return

    def update_category_of_articles(self,new_categories,request_SKU_number):
        updated_categories = ''
        object = Article.objects.get(SKU=request_SKU_number)
        if object is None:
            return JsonResponse({'Message': 'SKU not found in db!'}, status=status.HTTP_404_NOT_FOUND)
        object.Name.update(new_categories)
        object.save()
        return