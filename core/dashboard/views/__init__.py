from .messages import *
from .views import *
from .settings import *
from .donations import *
from .doctrines import *
from .leaders import *
from .messages import *
from .notifications import *
from .users import *


class DashboardView(View):
    '''CBV for rendering the dashboard page'''

    template = 'dashboard/dashboard.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
