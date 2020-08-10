from django.views import View
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from collections import deque

line_of_cars = {
    'Change oil': deque(),
    'Inflate tires': deque(),
    'Get diagnostic test': deque(),
}
last_ticket_id = 0
next_ticket_id = None


class WelcomeView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    menu = {
        'change_oil': 'Change oil',
        'inflate_tires': 'Inflate tires',
        'diagnostic': 'Get diagnostic test',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', {'menu': self.menu})


def get_ticket():
    global last_ticket_id
    last_ticket_id += 1
    return last_ticket_id


class ChangeOilView(View):

    def get(self, request, *args, **kwargs):
        ticket_id = get_ticket()
        tickets = line_of_cars['Change oil']
        n_tickets = len(tickets)
        tickets.append(ticket_id)
        minutes_to_wait = 2 * n_tickets  # priority 1

        return render(request, 'tickets/change_oil.html', {'id': ticket_id, 'minutes_to_wait': minutes_to_wait})


class InflateTiresView(View):

    def get(self, request, *args, **kwargs):
        ticket_id = get_ticket()
        tickets = line_of_cars['Inflate tires']
        n_tickets = len(tickets)
        tickets.append(ticket_id)

        minutes_to_wait_extra = 2 * len(line_of_cars['Change oil'])  # priority 2
        minutes_to_wait = (5 * n_tickets) + minutes_to_wait_extra

        return render(request, 'tickets/inflate_tires.html', {'id': ticket_id, 'minutes_to_wait': minutes_to_wait})


class DiagnosticView(View):

    def get(self, request, *args, **kwargs):
        ticket_id = get_ticket()
        tickets = line_of_cars['Get diagnostic test']
        n_tickets = len(tickets)
        tickets.append(ticket_id)

        # priority 3, least priority
        minutes_to_wait_extra = (2 * len(line_of_cars['Change oil'])) + (5 * len(line_of_cars['Inflate tires']))
        minutes_to_wait = (30 * n_tickets) + minutes_to_wait_extra

        return render(request, 'tickets/diagnostic.html', {'id': ticket_id, 'minutes_to_wait': minutes_to_wait})


class ProcessingView(View):

    def get(self, request, *args, **kwargs):
        queue = {}
        for service, list_tickets in line_of_cars.items():
            if service == 'Get diagnostic test':
                queue['Get diagnostic'] = len(list_tickets)  # remove "test"
            else:
                queue[service] = len(list_tickets)
        return render(request, 'tickets/processing.html', {'queue': queue})

    def post(self, request, *args, **kwargs):
        global next_ticket_id
        if line_of_cars['Change oil']:
            next_ticket_id = line_of_cars['Change oil'].popleft()
        elif line_of_cars['Inflate tires']:
            next_ticket_id = line_of_cars['Inflate tires'].popleft()
        elif line_of_cars['Get diagnostic test']:
            next_ticket_id = line_of_cars['Get diagnostic test'].popleft()
        return redirect('next/')


class NextView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html', {'next_id': next_ticket_id})
