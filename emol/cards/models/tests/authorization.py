from django.test import TestCase

from cards.models.authorization import Authorization
from cards.models.discipline import Discipline


class AuthorizationTestCase(TestCase):
    def setUp(self):
        self.discipline = Discipline.objects.create(slug="sword")
        self.auth1 = Authorization.objects.create(
            name="Cut", discipline=self.discipline, is_primary=True
        )
        self.auth2 = Authorization.objects.create(
            name="Thrust", discipline=self.discipline
        )

    def test_find_authorization_by_slug(self):
        authorization = Authorization.find(self.discipline.slug, self.auth1.slug)
        self.assertEqual(authorization, self.auth1)

    def test_find_authorization_by_name(self):
        authorization = Authorization.find(self.discipline.slug, self.auth2.name)
        self.assertEqual(authorization, self.auth2)

    def test_find_authorization_with_invalid_discipline(self):
        with self.assertRaises(Discipline.DoesNotExist):
            Authorization.find("invalid_discipline", self.auth1.slug)

    def test_find_authorization_with_invalid_slug(self):
        with self.assertRaises(Authorization.DoesNotExist):
            Authorization.find(self.discipline.slug, "invalid_slug")

    def test_find_authorization_with_invalid_name(self):
        with self.assertRaises(Authorization.DoesNotExist):
            Authorization.find(self.discipline.slug, "invalid_name")
