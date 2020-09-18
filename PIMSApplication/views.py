from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from PIMSApplication.decorator import secure, Authentication
from PIMSApplication.models import Article
from rest_framework.decorators import api_view
from PIMSApplication.serializers import PimsSerializer
import logging
from PIMSApplication.service import ArticleService
logger = logging.getLogger(__name__)


@api_view(['GET'])
def ui_article_fetch_all(request):
    if request.method == 'GET':
        articles_list_active = ArticleService().get_all_active_articles()
        if len(articles_list_active) <=0:
            return JsonResponse({"massage":"No article found!"},status=status.HTTP_200_OK)
        article_serializer = PimsSerializer(articles_list_active, many=True)
        logger.info(f"Found {len(articles_list_active)} Articles")
        return JsonResponse(article_serializer.data, safe=False)


@api_view(['GET'])
def ui_article_fetch_sorted(request):
    category = request.GET.get('category', None)
    if request.method == 'GET' and category is not None:
        logger.info(f"GET: Received fetch article request for category:{category}")
        try:
            article_list = ArticleService().get_all_active_articles()
        except Article.DoesNotExist:
            return JsonResponse({'message': 'The Article does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if category is not None:
            matched_category_list = list()
            for article in article_list:
                if  category in article.Name:
                    matched_category_list.append(article)
            article_serializer = PimsSerializer(matched_category_list, many=True)
            return JsonResponse(article_serializer.data, safe=False)
        return JsonResponse({'Message': 'Category not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        articles_list = ArticleService().get_all_articles()
        if len(articles_list) <=0:
            return JsonResponse({"massage":"No article found for sorting!"},status=status.HTTP_200_OK)
        orderbyList = ['price']  # default order
        if len(request.GET.getlist('order')) > 0:
            orderbyList = request.GET.getlist('order')
            articles_list=articles_list.order_by(*orderbyList)
        article_serializer = PimsSerializer(articles_list, many=True)
        return JsonResponse(article_serializer.data, safe=False)



# @secure
@api_view(['GET', 'POST', 'PUT'])
def article_list_admin(request, category=None):
    response=Authentication().authenticate(request)

    if response is not None and (response.status_code==status.HTTP_401_UNAUTHORIZED
                                 or response.status_code==status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED):
        return JsonResponse({'message': 'Unable to authenticate the user'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        article_list = ArticleService().get_all_active_articles()
    except Article.DoesNotExist:
        return JsonResponse({'message': 'The Article does not exist'}, status=status.HTTP_404_NOT_FOUND)
    SKU_NUMBER = request.GET.get('SKU', None)

    if request.method == 'GET' and SKU_NUMBER is not None:
        logger.info(f"GET: Received fetch article request for SKU:{SKU_NUMBER}")
        if SKU_NUMBER is not None:
            matched_SKU_list=list()
            for article in article_list:
                if article.SKU==int(SKU_NUMBER):
                    matched_SKU_list.append(article)
                    article_serializer = PimsSerializer(matched_SKU_list, many=True)
                    return JsonResponse(article_serializer.data, safe=False)
                    break
            return JsonResponse({'Message':'SKU not Found'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        articles_list_active = ArticleService().get_all_active_articles()
        if len(articles_list_active) <=0:
            return JsonResponse({"massage":"No article found for sorting!"},status=status.HTTP_200_OK)
        article_serializer = PimsSerializer(articles_list_active, many=True)
        logger.info(f"Successfully fetched articles:{article_serializer.data}")
        return JsonResponse(article_serializer.data, safe=False)

    elif request.method == 'PUT':
        article_request_data = JSONParser().parse(request)
        request_SKU_number=article_request_data.get('SKU')
        if request_SKU_number is None:
            return JsonResponse({'Message':'SKU not found in request payload!'},status=status.HTTP_400_BAD_REQUEST)
        new_categories=article_request_data.get('Name')
        if new_categories is None:
            return JsonResponse(article_request_data, status=status.HTTP_400_BAD_REQUEST)
        ArticleService().update_category_of_articles(new_categories=new_categories,
                                                     request_SKU_number=request_SKU_number)
        success = {
            "success": "success",
            "data": article_request_data
        }
        logger.info(f"Successfully updated article:{success}")
        return JsonResponse(success, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        article_data = JSONParser().parse(request)
        article_serializer = PimsSerializer(data=article_data)
        if article_serializer.is_valid():
            article_serializer.save()
            logger.info(f"Successfully created article:{article_serializer.data}")
            return JsonResponse(article_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def article_delete_category_admin(request):
    if request.method == 'DELETE':
        Delete_request_data = JSONParser().parse(request)
        ArticleService().disable_category_of_articles(Delete_request_data)
        return JsonResponse({'message': 'Category was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

