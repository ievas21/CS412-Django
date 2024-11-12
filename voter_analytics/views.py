from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.query import QuerySet
from typing import Any
import plotly
import plotly.graph_objects as go
from .models import Voter
from django.utils import timezone
from django.db.models import Count

# Ieva sagaitis, ievas@bu.edu

elections = {
        'v20state': '2020 State Election',
        'v21town': '2021 Town Election',
        'v21primary': '2021 Primary Election',
        'v22general': '2022 General Election',
        'v23town': '2023 Town Election'
    }


# Create your views here.
class VotersListView(ListView):
    '''View to display list of voters'''
    template_name='voter_analytics/results.html'
    model = Voter
    context_object_name = "results"
    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        '''Return the set of Results'''
        
        # start with entire queryset
        qs = super().get_queryset()

        # filter results by these field(s):
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        elections = self.request.GET.getlist('elections')

        if party_affiliation:
            qs = qs.filter(party_affiliation=party_affiliation)

        if min_dob:
            qs = qs.filter(dob__year__gte=int(min_dob))

        if max_dob:
            qs = qs.filter(dob__year__lte=int(max_dob))

        if voter_score:
            qs = qs.filter(voter_score=int(voter_score))

        if elections:
            for election in elections:
                # builds a filter based on the current election field (e.g. v20state, v23town , etc)
                qs = qs.filter(**{election: True})

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['scores'] = range(1, 6)

        current_year = timezone.now().year
        context['years'] = range(1913, current_year + 1)
        
        return context
    
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'r'


class GraphListView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'r'

    def get_queryset(self) -> QuerySet[Any]:
        '''Return the set of Results'''
        
        # start with entire queryset
        qs = super().get_queryset()

        # filter results by these field(s):
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        elections = self.request.GET.getlist('elections')

        if party_affiliation:
            qs = qs.filter(party_affiliation=party_affiliation)

        if min_dob:
            qs = qs.filter(dob__year__gte=int(min_dob))

        if max_dob:
            qs = qs.filter(dob__year__lte=int(max_dob))

        if voter_score:
            qs = qs.filter(voter_score=int(voter_score))

        if elections:
            for election in elections:
                # builds a filter based on the current election field (e.g. v20state, v23town , etc)
                qs = qs.filter(**{election: True})

        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Add some data to the context object, including graphs.'''
        
        context = super().get_context_data(**kwargs)

        context['scores'] = range(1, 6)
        current_year = timezone.now().year
        context['years'] = range(1924, current_year + 1)

        voters = self.get_queryset()

        # count how many voters exist for each birth year 
        voter_data = voters.values('dob__year').annotate(count=Count('id')).order_by('dob__year')

        # build the graph
        x = [entry['dob__year'] for entry in voter_data]
        
        y = [entry['count'] for entry in voter_data]

        fig = go.Figure(data=[go.Bar(x=x, y=y)]) 
        total_voters = sum(y)

        fig.update_layout(
            title=f"Voter Birth Year Distribution (n={total_voters})",
            xaxis_title="Birth Year",
            yaxis_title="Number of Voters",
        )

        graph_div = plotly.offline.plot(fig, 
                                        auto_open=False, 
                                        output_type="div")

        # add the graph to the context
        context['birth_graph_div'] = graph_div


        # count the number of voters in each political party
        party_data = voters.values('party_affiliation').annotate(count=Count('id'))
        labels = [entry['party_affiliation'] for entry in party_data]
        values = [entry['count'] for entry in party_data]

        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig_pie.update_layout(
            title=f"Voter Distribution by Party Affiliation (n={total_voters})"
        )

        pie_chart = plotly.offline.plot(fig_pie, 
                                        auto_open=False, 
                                        output_type="div")
        
        context['pie_chart'] = pie_chart

        election_labels = []
        election_counts = []

        for field, label in elections.items():
            # count the number of voters who voted in each election
            count = voters.filter(**{field: True}).count()
            # name of each election
            election_labels.append(label)
            # how many people voted in each specific election (stored matching with each corresponding label)
            election_counts.append(count)

        fig_elect = go.Figure(data=[go.Bar(x=election_labels, y=election_counts)])

        fig_elect.update_layout(
            title=f"Voter Count by Election (n={total_voters})",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
        )

        histogram = plotly.offline.plot(fig_elect, 
                                        auto_open=False, 
                                        output_type="div")
        
        context['histogram'] = histogram

        return context


