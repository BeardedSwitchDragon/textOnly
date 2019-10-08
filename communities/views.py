from django.shortcuts import render
from django.contrib import messages
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from communities.models import Community,CommunityMember

class CreateCommunity(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Community

class SingleCommunity(generic.DetailView):
    model = Community

class ListCommunities(generic.ListView):
    model = Community

class JoinCommunity(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse("communities:single", kwargs={"slug":self.kwargs.get("slug")})
    def get(self, request,*args, **kwargs):
        community = get_object_or404(Community, slug=self.kwargs.get("slug"))

        try:
            CommunityMember.objects.create(user=self.request.user, community=community)
        except IntegrityError:
            messages.warning(self.request,"Warning, already a member!")
        else:
            message.success(self.request, "You are now a member!")
        return super().get(request, *args, **kwargs)


class LeaveCommunity(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse("communities:single", kwargs={"slug":self.kwargs.get("slug")})

    def get(self,request,*args,**kwargs):

        try:
            membership = models.objects.filter(
                user=self.request.user,
                community__slug=self.kwargs.get("slug")
            ).get()
        except models.ComunityMember.DoesNotExit:
            messages.warning(self.request, "Sorry, you aren't in this group!")
        else:
            membership.delete()
            messages.success(self.request, "You have left the group!")
        return super().get(request, *args,**kwargs)
