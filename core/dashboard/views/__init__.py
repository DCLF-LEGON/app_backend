from .messages import *
from .views import *
from .settings import *
from .donations import *
from .doctrines import *
from .leaders import *
from .messages import *
from .notifications import *
from .users import *
from .preachers import *
from .categories import *

from core.utils.util_functions import get_api_wallet_balance
from accounts.models import User


class DashboardView(View):
    '''CBV for rendering the dashboard page'''

    template = 'dashboard/dashboard.html'

    def get(self, request):
        context = {
            'balance': get_api_wallet_balance(),
            'users': User.objects.count(),
            'staff_members': User.objects.filter(is_staff=True),
        }
        return render(request, self.template, context)
