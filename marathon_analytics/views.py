from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Result
from django.db.models.query import QuerySet
from typing import Any
import plotly
import plotly.graph_objects as go

# Create your views here.
class ResultsListView(ListView):
    '''View to display list of marathonresults'''
    template_name='marathon_analytics/results.html'
    model = Result
    context_object_name = "results"
    paginate_by = 50


    def get_queryset(self) -> QuerySet[Any]:
        '''Return the set of Results'''
        
        # start with entire queryset
        qs = super().get_queryset().order_by('place_overall')
        # filter results by these field(s):
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            if city:
               qs = Result.objects.filter(city__contains=city)
                    
        return qs

class ResultDetailView(DetailView):
    '''Show the results for one record.'''
    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Add soem data to the context object, including graphs.'''
        context = super().get_context_dtat(**kwargs)
        r = context['r']

        # build the graph
        x = [f'Runners Passed by {r.first_name}',
             f'Runners who Passed {r.first_name}']
        
        y = [r.get_runners_passed(),
             r.get_runner_passed_by()]
        
        fig = go.Bar(x=x, y=y)
        graph_div = plotly.offline.plot({"data": [fig]},
                                        auto_open=False,
                                        output_type="div")

        # add the graph to the context
        context['graph_div'] = graph_div

        # build a pie chart of first half and second half
        x = ['first half time', 'second_half_time']

        first_half_time_seconds = r.time_half_1.hour * 3600 + r.time_half1.minute * 60 + r.time_half1.second
        second_half_time_seconds = r.time_half_2.hour * 3600 + r.time_half2.minute * 60 + r.time_half2.second

        y = [first_half_time_seconds, second_half_time_seconds]

        fig = go.Pie(labels=x, values=y)
        pie_div = plotly.offline.plot({"data": [fig]},
                                        auto_open=False,
                                        output_type="div")

        context['pie_div'] = pie_div
        
        return context