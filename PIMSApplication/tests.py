from django.test import TestCase

from django.test import TestCase
from PIMSApplication.models import Article
from django.test import Client

from PIMSApplication.service import ArticleService


class AnimalTestCase(TestCase):
    def setUp(self):
        Article.objects.create(SKU=100,EAN=10001,Name={"category1":True},Stock_quantity=100,price=10,active=False)
        Article.objects.create(SKU=101,EAN=10002,Name={"category2":True},Stock_quantity=50,price=20,active=False)
        Article.objects.create(SKU=103,EAN=10006,Name={"category1":True},Stock_quantity=50,price=20,active=False)

    def test_animals_can_speak(self):
        SKU100 = Article.objects.get(SKU="100")
        self.assertEqual(SKU100.EAN,10001)
    def test_update_category_enable_case(self):
        old_category={"category1":True}
        Article.objects.create(SKU=2001,EAN=10001,Name=old_category,Stock_quantity=100,price=10,active=False)
        new_category={"category2":True}
        old_category.update(new_category)
        SKU_NUMBER=2001
        ArticleService().update_category_of_articles(new_categories=new_category,request_SKU_number=SKU_NUMBER)
        object = Article.objects.get(SKU=SKU_NUMBER)
        self.assertEqual(object.Name,old_category)

    def test_update_category_disable_single_article_case(self):
        old_category={"category1":True,"category2":True}
        Article.objects.create(SKU=3001,EAN=10001,Name=old_category,Stock_quantity=100,price=10,active=False)
        new_category={"category2":False}
        old_category.update(new_category)
        SKU_NUMBER=3001
        ArticleService().update_category_of_articles(new_categories=new_category,request_SKU_number=SKU_NUMBER)
        object = Article.objects.get(SKU=SKU_NUMBER)
        self.assertEqual(object.Name,old_category)

    def test_update_category_disable_multiple_article_case(self):
        old_category={"category1":True,"category2":True}
        Article.objects.create(SKU=4001,EAN=10001,Name=old_category,Stock_quantity=100,price=10,active=False)
        Article.objects.create(SKU=4002,EAN=10001,Name=old_category,Stock_quantity=100,price=10,active=False)
        new_category={"category2":False}
        old_category.update(new_category)
        SKU_NUMBER_4001=4001
        SKU_NUMBER_4002=4002
        ArticleService().update_category_of_articles(new_categories=new_category,request_SKU_number=SKU_NUMBER_4001)
        ArticleService().update_category_of_articles(new_categories=new_category,request_SKU_number=SKU_NUMBER_4002)
        object = Article.objects.get(SKU=SKU_NUMBER_4001)
        self.assertEqual(object.Name,old_category)
        object = Article.objects.get(SKU=SKU_NUMBER_4002)
        self.assertEqual(object.Name, old_category)

    def test_update_category_enable_multiple_article_case(self):
        old_category={"category1":True,"category2":False}
        Article.objects.create(SKU=5001,EAN=10001,Name=old_category,Stock_quantity=100,price=10,active=False)
        Article.objects.create(SKU=5002,EAN=10001,Name=old_category,Stock_quantity=100,price=10,active=False)
        new_category={"category2":True}
        old_category.update(new_category)
        SKU_NUMBER_5001=5001
        SKU_NUMBER_5002=5002
        ArticleService().update_category_of_articles(new_categories=new_category,request_SKU_number=SKU_NUMBER_5001)
        ArticleService().update_category_of_articles(new_categories=new_category,request_SKU_number=SKU_NUMBER_5002)
        object = Article.objects.get(SKU=SKU_NUMBER_5001)
        self.assertEqual(object.Name,old_category)
        object = Article.objects.get(SKU=SKU_NUMBER_5002)
        self.assertEqual(object.Name, old_category)

    def test_view_testing(self):
        c = Client()
        payload={
            "SKU": 100011,
            "EAN": 10002,
            "Name": {
                "Bags": False
            },
            "Stock_quantity": 2,
            "price": 100000,
            "active": False
        }
        response = c.get('http://localhost:8090/api/v1/admin/article/fetch')
        print(response.json())

    def test_get_all_articles_number_success_case(self):
        list_of_articles=Article.objects.all()
        self.assertEqual(3, len(list_of_articles))

    def test_get_all_articles_number_failure_case(self):
        list_of_articles=Article.objects.all()
        self.assertEqual(3, len(list_of_articles))

    def test_get_all_active_articles_success_case(self):
        list_of_articles=Article.objects.all()
        list_of_active_articles=list()
        for item in (list_of_articles):
            if item.active==True:
                list_of_active_articles.append(item)
        self.assertEqual(0, len(list_of_active_articles))

    def test_get_all_active_articles_failure_case(self):
        list_of_articles=Article.objects.all()
        list_of_active_articles=list()
        for item in (list_of_articles):
            if item.active==True:
                list_of_active_articles.append(item)
        self.assertNotEqual(1, len(list_of_active_articles))

