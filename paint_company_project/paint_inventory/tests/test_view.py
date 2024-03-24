from paint_company_project.paint_inventory.models import Paint
from paint_company_project.paint_inventory.utils import ViewSetTestCase
from paint_company_project.paint_inventory.views import PaintViewSet
from paint_company_project.user.tests.factory import UserFactory

class PaintViewSetTest(ViewSetTestCase):
    viewset_cls = PaintViewSet
    base_url = "paints"

    def setUp(self):
        self.user = UserFactory(
            email="user@test.com",
            can_view_paint_list=True,
            can_edit_paint_status=True,
            can_edit_paint_inventory=True,
        )

    def test_list_paints(self):
        blue_paint = Paint.objects.create(
            color=Paint.BLUE,
            status=Paint.AVAILABLE,
            inventory=1,
        )
        response = self.list(auth_user=self.user)
        self.assertStatusCode(response, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(blue_paint.id))
        self.assertEqual(response.data[0]["color"], blue_paint.color)
        self.assertEqual(response.data[0]["status"], blue_paint.status)
        self.assertEqual(response.data[0]["inventory"], blue_paint.inventory)

    def test_list_multiple_paints(self):
        blue_paint = Paint.objects.create(
            color=Paint.BLUE,
            status=Paint.AVAILABLE,
            inventory=3,
        )
        grey_paint = Paint.objects.create(
            color=Paint.GREY,
            status=Paint.RUNNING_LOW,
            inventory=2,
        )
        white_paint = Paint.objects.create(
            color=Paint.WHITE,
            status=Paint.OUT_OF_STOCK,
            inventory=0,
        )
        response = self.list(auth_user=self.user)
        self.assertStatusCode(response, 200)
        self.assertEqual(len(response.data), 3)
    
    def test_edit_paint_status(self):
        blue_paint = Paint.objects.create(
            color=Paint.BLUE,
            status=Paint.AVAILABLE,
            inventory=3,
        )
        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=self.user)
        self.assertStatusCode(retrieve_response, 200)
        self.assertEqual(retrieve_response.data["status"], blue_paint.status)

        data = {"status": Paint.RUNNING_LOW}
        edit_status_response = self.custom_action(
            method="put",
            action="status",
            auth_user=self.user,
            pk=blue_paint.id,
            data=data,
        )
        self.assertStatusCode(edit_status_response, 200)

        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=self.user)
        self.assertStatusCode(retrieve_response, 200)
        self.assertEqual(retrieve_response.data["status"], Paint.RUNNING_LOW)
    
    def test_edit_paint_inventory(self):
        blue_paint = Paint.objects.create(
            color=Paint.BLUE,
            status=Paint.AVAILABLE,
            inventory=3,
        )
        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=self.user)
        self.assertStatusCode(retrieve_response, 200)
        self.assertEqual(retrieve_response.data["inventory"], blue_paint.inventory)

        data = {"inventory": 0}
        edit_inventory_response = self.custom_action(
            method="put",
            action="inventory",
            auth_user=self.user,
            pk=blue_paint.id,
            data=data,
        )
        self.assertStatusCode(edit_inventory_response, 200)

        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=self.user)
        self.assertStatusCode(retrieve_response, 200)
        self.assertEqual(retrieve_response.data["inventory"], 0)


class PaintViewSetPermissionTest(ViewSetTestCase):
    viewset_cls = PaintViewSet
    base_url = "paints"

    def test_list_paints_permission(self):
        user = UserFactory(
            email="user@test.com",
            can_view_paint_list=False,
            can_edit_paint_status=False,
            can_edit_paint_inventory=False,
        )

        blue_paint = Paint.objects.create(
            color=Paint.BLUE,
            status=Paint.AVAILABLE,
            inventory=1,
        )
        response = self.list(auth_user=user)
        self.assertStatusCode(response, 403)

        user.can_view_paint_list = True
        user.save()
        response = self.list(auth_user=user)
        self.assertStatusCode(response, 200)
        user.delete()
    
    def test_edit_paint_status_permission(self):
        user = UserFactory(
            email="user@test.com",
            can_view_paint_list=False,
            can_edit_paint_status=False,
            can_edit_paint_inventory=False,
        )

        blue_paint = Paint.objects.create(
            color=Paint.BLUE,
            status=Paint.AVAILABLE,
            inventory=1,
        )

        # user has no permission to retrieve paint details
        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=user)
        self.assertStatusCode(retrieve_response, 403)
        
        # user has permission to retrieve paint details
        user.can_view_paint_list = True
        user.save()
        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=user)
        self.assertStatusCode(retrieve_response, 200)

        data = {"status": Paint.RUNNING_LOW}
        edit_status_response = self.custom_action(
            method="put",
            action="status",
            auth_user=user,
            pk=blue_paint.id,
            data=data,
        )
        # user has no permission to edit paint status
        self.assertStatusCode(edit_status_response, 403)

        user.can_edit_paint_status = True
        user.save()
        edit_status_response = self.custom_action(
            method="put",
            action="status",
            auth_user=user,
            pk=blue_paint.id,
            data=data,
        )
        # user has permission to edit paint status
        self.assertStatusCode(edit_status_response, 200)

        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=user)
        self.assertStatusCode(retrieve_response, 200)
        self.assertEqual(retrieve_response.data["status"], Paint.RUNNING_LOW)

        user.delete()
    
    def test_edit_paint_inventory_permission(self):
        user = UserFactory(
            email="user@test.com",
            can_view_paint_list=False,
            can_edit_paint_status=False,
            can_edit_paint_inventory=False,
        )

        blue_paint = Paint.objects.create(
            color=Paint.BLUE,
            status=Paint.AVAILABLE,
            inventory=1,
        )

        # user has no permission to retrieve paint details
        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=user)
        self.assertStatusCode(retrieve_response, 403)
        
        # user has permission to retrieve paint details
        user.can_view_paint_list = True
        user.save()
        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=user)
        self.assertStatusCode(retrieve_response, 200)

        data = {"inventory": 0}
        edit_status_response = self.custom_action(
            method="put",
            action="inventory",
            auth_user=user,
            pk=blue_paint.id,
            data=data,
        )
        # user has no permission to edit paint inventory
        self.assertStatusCode(edit_status_response, 403)

        user.can_edit_paint_inventory = True
        user.save()
        edit_status_response = self.custom_action(
            method="put",
            action="inventory",
            auth_user=user,
            pk=blue_paint.id,
            data=data,
        )
        # user has permission to edit paint inventory
        self.assertStatusCode(edit_status_response, 200)

        retrieve_response = self.retrieve(pk=blue_paint.id, auth_user=user)
        self.assertStatusCode(retrieve_response, 200)
        self.assertEqual(retrieve_response.data["inventory"], 0)

        user.delete()