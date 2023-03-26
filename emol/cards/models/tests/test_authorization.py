from django.test import TestCase

from cards.models.authorization import Authorization
from cards.models.discipline import Discipline


class AuthorizationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        discipline = Discipline.objects.create(name="Heavy Rapier", slug="heavy-rapier")
        Authorization.objects.create(
            name="Armored Combat", slug="armored-combat", discipline=discipline
        )

    def test_name_label(self):
        authorization = Authorization.objects.get(id=1)
        field_label = authorization._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_slug_label(self):
        authorization = Authorization.objects.get(id=1)
        field_label = authorization._meta.get_field("slug").verbose_name
        self.assertEquals(field_label, "slug")

    def test_discipline_label(self):
        authorization = Authorization.objects.get(id=1)
        field_label = authorization._meta.get_field("discipline").verbose_name
        self.assertEquals(field_label, "discipline")

    def test_name_max_length(self):
        authorization = Authorization.objects.get(id=1)
        max_length = authorization._meta.get_field("name").max_length
        self.assertEquals(max_length, 100)

    def test_slug_max_length(self):
        authorization = Authorization.objects.get(id=1)
        max_length = authorization._meta.get_field("slug").max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_name(self):
        authorization = Authorization.objects.get(id=1)
        expected_object_name = authorization.name
        self.assertEquals(expected_object_name, str(authorization))
