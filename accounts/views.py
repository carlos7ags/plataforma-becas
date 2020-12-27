from django.urls import reverse
from django.views.generic import CreateView

from accounts.forms import UserCreationForm
from becas.models import Student


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = "user_registration.html"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("student-profile-redirect")
