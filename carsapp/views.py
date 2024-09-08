from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import classonlymethod
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .forms import CustomUserCreationForm
from .models import Car, Comment
from .permissions import IsCarOwner
from .sirealizers import CarModelSerializer, CommentModelSerializer


class CarModelViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = CarModelSerializer
    queryset = Car.objects.select_related("owner").prefetch_related("comments")

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ("DELETE", "PUT"):
            return [IsAuthenticated(), IsCarOwner()]
        elif self.request.method == "POST":
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.pk)

    @action(
        detail=True,
        methods=["GET", "POST"],
        url_path="comments",
        url_name="car-comments",
        serializer_class=CommentModelSerializer,
    )
    def comments(self, request: Request, pk=None):
        car = self.get_object()
        if request.method == "GET":
            return Response(
                CommentModelSerializer(car.comments, many=True).data,
                status=status.HTTP_200_OK,
            )
        elif request.method == "POST":
            serializer = CommentModelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(car=car, author=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "carsapp/register.html"
    success_url = reverse_lazy("carsapp:index")

    @classonlymethod
    def as_view(cls, **initkwargs):
        return login_not_required(super().as_view(**initkwargs))

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def index(request: HttpRequest):
    return render(request, "carsapp/index.html")


class CarListView(ListView):
    queryset = Car.objects.select_related("owner").prefetch_related("comments")


class CarDetailView(DetailView):
    queryset = Car.objects.select_related("owner").prefetch_related("comments")
    start_total_comments = 0
    more_comments_per_push = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(car=self.get_object())
        current_total_comments = int(
            self.request.GET.get("total_comments", self.start_total_comments)
        )
        if current_total_comments > 0:
            paginator = Paginator(comments, current_total_comments)
            context["page_obj"] = paginator.get_page(1)
        context["current_total_comments"] = current_total_comments
        context["start_total_comments"] = self.start_total_comments
        context["more_comments_per_push"] = self.more_comments_per_push
        return context

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("Not auth")

        car = get_object_or_404(Car, pk=kwargs["pk"])
        content = self.request.POST["content"]
        error = None

        if not content:
            error = "Комментарий не может быть пустым"
        elif len(content) > 255:
            error = "Максимальная длина комментария 255 символов"

        if error is None:
            Comment.objects.create(author=self.request.user, car=car, content=content)
            return redirect(
                reverse("carsapp:car_detail", args=(self.kwargs["pk"],))
                + f"?total_comments={self.request.GET.get("total_comments")}"
            )
        else:
            context = self.get_context_data()
            context.update(
                {
                    "user": self.request.user,
                    "car": car,
                    "error": error,
                    "current_total_comments": self.request.GET.get("total_comments"),
                }
            )
            return render(request, "carsapp/car_detail.html", context=context)


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    fields = "make", "model", "year", "description"

    def get_initial(self):
        initial = super().get_initial()
        initial["year"] = datetime.now().year - 5
        return initial

    def get_success_url(self):
        return reverse("carsapp:car_detail", args=(self.object.pk,))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.owner = self.request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CarUprateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    queryset = Car.objects.select_related("owner").prefetch_related("comments")
    template_name_suffix = "_update_form"
    context_object_name = "car"
    model = Car
    fields = "make", "model", "year", "description"

    def get_success_url(self):
        return (
            reverse("carsapp:car_detail", args=(self.object.pk,))
            + f"?total_comments={self.request.GET.get("total_comments")}"
        )

    def test_func(self):
        return self.request.user.pk == self.get_object().owner.pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_total_comments"] = self.request.GET.get("total_comments", 0)
        return context


class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    queryset = Car.objects.select_related("owner").prefetch_related("comments")
    context_object_name = "car"
    model = Car
    success_url = reverse_lazy("carsapp:car_list")

    def test_func(self):
        return self.request.user.pk == self.get_object().owner.pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_total_comments"] = self.request.GET.get("total_comments", 0)
        return context


# def latinize(sym):
# 	return unicodedata.normalize('NFKD', sym).encode('ascii', 'ignore').decode('ascii')
#
# for carset in data:
# 	word = ""
# 	for s in carset["brand"]:
# 		word += latinize(s)
# 	carset["brand"] = word
# 	for i, model in enumerate(carset["models"]):
# 		word = ""
# 		for s in model:
# 			word += latinize(s)
# 		carset["models"][i] = word
