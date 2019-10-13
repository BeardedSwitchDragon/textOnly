from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import *
from django.contrib import messages
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import models
from . import forms
from django.db import IntegrityError
from django.contrib.auth import get_user_model
User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ("user", "community")

class UserPost(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post.user = User.object.prefetch_related("posts").get(username__iexact=self.kwargs.get("username"))
        except User.DoesNotExit:
            raise Http404
        else:
            return self.post_user.posts.all()
    def get_contextdata(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "community")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get("username"))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):

    fields = ("message", "community")
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        try:
            self.object.save()
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, "It looks like something went wrong. Is this post a duplicate?")

        return render(self.request, "posts/post_form.html", {"form": form})






class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "community")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args,**kwargs)
