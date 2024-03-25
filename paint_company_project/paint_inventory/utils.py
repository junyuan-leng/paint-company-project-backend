from django.urls import reverse
from hashid_field import BigHashidAutoField
from rest_framework.test import force_authenticate, APITestCase, APIRequestFactory


class CustomBigHashidAutoField(BigHashidAutoField):
    def __init__(self, prefix="", salt="my_salt", *args, **kwargs):
        salt = prefix + salt
        super().__init__(prefix=prefix, salt=salt, *args, **kwargs)


class ViewSetTestCase(APITestCase):
    # this is a helper class which simplifies view set tests
    request_factory = APIRequestFactory()
    viewset_cls = None
    view_cls = None
    view_fnc = None
    base_url = None
    url_name = None
    default_auth_user_cls = None

    def assertStatusCode(self, response, status_code):
        if response.status_code != status_code:
            try:
                response.render()
                print(response.content)
            except AttributeError:
                pass
        self.assertEqual(response.status_code, status_code)

    def post(self, *args, **kwargs):
        return self._get_response(method="post", *args, **kwargs)

    def get(self, *args, **kwargs):
        return self._get_response(method="get", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._get_response(method="delete", *args, **kwargs)

    def create(self, *args, **kwargs):
        return self._get_response(action="create", *args, **kwargs)

    def update(self, *args, **kwargs):
        return self._get_response(action="update", *args, **kwargs)

    def partial_update(self, *args, **kwargs):
        return self._get_response(action="partial_update", *args, **kwargs)

    def list(self, *args, **kwargs):
        return self._get_response(action="list", *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        return self._get_response(action="retrieve", *args, **kwargs)

    def destroy(self, *args, **kwargs):
        return self._get_response(action="destroy", *args, **kwargs)

    def custom_action(self, method, action, *args, **kwargs):
        return self._get_response(method=method, action=action, *args, **kwargs)

    def get_auth_user(self):
        return None

    def get_kwargs(self):
        return {}

    def _get_response(
        self,
        action=None,
        method=None,
        auth_user=None,
        url_type=None,
        data=None,
        query_params=None,
        skip_authentication=False,
        headers=None,
        **kwargs,
    ):
        """A general purpose helper for testing view sets.
        Using DRF's request factory a request is built to hit the appropriate
        url and viewset based on the class attributes `viewset_cls` and `base_url`.

        A method or action must be provided.

        Args:
            action (str): one of (list, retreive, create, destroy, update or a custom_action)
                used to use the correct method
            method (str): on of (get, post, patch, delete)
            auth_user (AllayUser): the user that will be used for authenticating
                (Defaults to OrgAdmin)
            url_type (str): one of (list, detail) which is used in finding the
                correct reversed url
            data (dict): data that will be sent in the request
            query_params (list): a list of query parameters to append to the url
            skip_authentication (bool): if true no request user will be sent
            **kwargs: extra key words to pass into the request

        Returns:
            HTTPResponse
        """
        if self.base_url is None and self.url_name is None:
            raise ValueError("base_url or url_name must be set")
        if self.viewset_cls is None and self.view_cls is None and self.view_fnc is None:
            raise ValueError("One of viewset_cls or view_cls or view_fnc must be set")

        if auth_user is None and not skip_authentication:
            auth_user = self.get_auth_user()
            if auth_user is None and self.default_auth_user_cls is not None:
                auth_user = self.default_auth_user_cls()

        method_map = {
            "create": "post",
            "partial_update": "patch",
            "update": "put",
            "list": "get",
            "retrieve": "get",
            "destroy": "delete",
        }

        if not kwargs:
            kwargs = self.get_kwargs()

        if data is None:
            data = {}

        if method is None:
            method = method_map[action]

        headers = headers or {}

        if url_type is None and action:
            if action.lower() in ("create", "list"):
                url = reverse(r"{}-list".format(self.base_url), kwargs=kwargs)
            elif action.lower() in ("partial_update", "update", "retrieve", "destroy"):
                url = reverse(r"{}-detail".format(self.base_url), kwargs=kwargs)
            else:
                url = reverse(f"{self.base_url}-{'-'.join(action.split('_'))}", kwargs=kwargs)
        elif url_type:
            url = reverse(f"{self.base_url}-{url_type}", kwargs=kwargs)
        elif self.url_name:
            url = reverse(self.url_name, kwargs=kwargs)
        else:
            url = self.base_url

        if query_params:
            if isinstance(query_params, dict):
                qs = ""
                for key, value in query_params.items():
                    qs += f"{key}={value}&"
                qs = qs.strip("&")
            else:
                qs = "&".join([p for p in query_params])

            url = "?".join((url, qs))

        if action:
            view = self.viewset_cls.as_view({method: action})
        else:
            if self.view_fnc:
                view = self.__class__.view_fnc
            elif self.viewset_cls:
                view = self.viewset_cls.as_view()
            elif self.view_cls:
                if hasattr(self.view_cls, "as_view"):
                    view = self.view_cls.as_view()
                else:
                    view = self.view_cls.view_class.as_view()
        http_method = getattr(self.request_factory, method)
        request = http_method(url, data=data, format="json", **headers)
        if not skip_authentication:
            force_authenticate(request, user=auth_user)
        response = view(request, **kwargs)
        return response
