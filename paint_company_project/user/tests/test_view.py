from paint_company_project.paint_inventory.utils import ViewSetTestCase
from paint_company_project.user.views import UserViewSet
from paint_company_project.user.tests.factory import UserFactory


class UserViewSetTest(ViewSetTestCase):
    viewset_cls = UserViewSet
    base_url = "user"

    def setUp(self):
        self.user = UserFactory(
            email="user@test.com",
            is_head_office_staff=True,
            can_view_paint_list=True,
            can_edit_paint_status=True,
            can_edit_paint_inventory=True,
        )

    def test_me(self):
        response = self.custom_action(
            method="get",
            action="me",
            auth_user=self.user
        )
        self.assertStatusCode(response, 200)
        self.assertEqual(response.data["is_head_office_staff"], self.user.is_head_office_staff)
        self.assertEqual(response.data["can_view_paint_list"], self.user.can_view_paint_list)
        self.assertEqual(response.data["can_edit_paint_status"], self.user.can_edit_paint_status)
        self.assertEqual(response.data["can_edit_paint_inventory"], self.user.can_edit_paint_inventory)