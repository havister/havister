"""havister index views
"""
from dateutil.relativedelta import relativedelta

from django.http import Http404
from django.views import generic

from index.models import Index, Day, Expiration

class ExpirationView(generic.DetailView):
    model = Index
    context_object_name = 'index'
    template_name = 'index/expiration.html'

    def get_context_data(self, **kwargs):
        # base 
        context = super(ExpirationView, self).get_context_data(**kwargs)
        # index object
        index = kwargs['object']
        if not index.option:
            raise Http404
        # expiration list
        context['detail_list'] = Expiration.objects.filter(index=index).reverse()[:12]
        # max period: 120 months
        period = Expiration.objects.filter(index=index).count()
        if period > 120:
            period = 120
        context['period'] = period
        # extra
        if context['detail_list']:
            context['max_date'] = context['detail_list'].first().date + relativedelta(months=1)
            context['alpha_list'] = self.get_alpha_list(index, period)
            context['beta_list'] = self.get_beta_list(index, period)
        return context

    def get_alpha_list(self, index, period):
        # 변화율 분포
        start_at = Expiration.objects.filter(index=index).reverse()[period-1].date
        levels = [[100, 20], [20, 10], [10, 5], [5, 0], [0, 0], [0, -5], [-5, -10], [-10, -20], [-20, -100]]
        alpha_list = []

        for level in levels:
            # level
            high = level[0]
            low = level[1]
            # alpha
            alpha = {}
            if high > 0:
                if high < 100:
                    alpha['level'] = "상승 {0}% 미만".format(high)
                else:
                    alpha['level'] = "상승 {0}% 이상".format(low)
                alpha['count'] = Expiration.objects.filter(index=index, date__gte=start_at, change__lt=high, change__gte=low).count()
            elif high == 0 and low == 0:
                alpha['level'] = "보합 0%"
                alpha['count'] = Expiration.objects.filter(index=index, date__gte=start_at, change=0).count()
            elif low < 0:
                if low > -100:
                    alpha['level'] = "하락 {0}% 미만".format(abs(low))
                else:
                    alpha['level'] = "하락 {0}% 이상".format(abs(high))
                alpha['count'] = Expiration.objects.filter(index=index, date__gte=start_at, change__lte=high, change__gt=low).count()
            # alpha list
            alpha_list.append(alpha)
        return alpha_list

    def get_beta_list(self, index, period):
        # 변화율 리스트
        beta_list = Expiration.objects.filter(index=index).values('change').reverse()[:period]
        return beta_list

