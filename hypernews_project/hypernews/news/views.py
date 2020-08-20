from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.conf import settings
import json
from itertools import groupby
from datetime import datetime

NEWS_JSON_PATH = settings.NEWS_JSON_PATH


class ArticleView(View):

    def get(self, request, id_article, *args, **kwargs):
        with open(NEWS_JSON_PATH, 'r') as json_db:
            json_data = json.load(json_db)
            for article in json_data:
                if article['link'] == id_article:
                    article_data = article
                    break
        return render(request, 'news/article.html', {'article': article_data})


class MainPageView(View):

    # [{"created": "2020-02-09 16:15:10", "text": "Text of the news 3", "title": "News 3", "link": 3}]
    def get(self, request, *args, **kwargs):
        with open(NEWS_JSON_PATH, 'r') as json_db:
            json_data = json.load(json_db)
        query_string = request.GET.get('q', None)
        if query_string is not None:
            src_results = []
            for article in json_data:
                if query_string.strip().lower() in article['title'].lower():
                    src_results.append(article)
            grouped_by_day = self.sort_group_articles(src_results)
        else:
            grouped_by_day = self.sort_group_articles(json_data)
        return render(request, 'news/main.html', {'grouped_by_day': grouped_by_day})

    @staticmethod
    def sort_group_articles(json_data):
        json_data_sorted = sorted(json_data, key=lambda i: i['created'], reverse=True)
        grouped_by_day = {}
        for k, g in groupby(json_data_sorted, key=lambda i: i['created'][:10]):
            grouped_by_day[k] = list(g)
        return grouped_by_day


class CreateArticleView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'news/new_article.html')

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        text = request.POST['text']
        created = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        with open(NEWS_JSON_PATH, 'r') as json_db:
            json_data = json.load(json_db)
        last_id = max(i['link'] for i in json_data)
        new_id = last_id + 1
        new_record = {"created": created, "text": text, "title": title, "link": new_id}
        json_data.append(new_record)
        with open(NEWS_JSON_PATH, 'w') as json_db:  # clobber
            json.dump(json_data, json_db)

        return redirect('/news/')
