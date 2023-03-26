from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from datetime import datetime

from cards.models.authorization import Authorization
from cards.models.discipline import Discipline
from cards.models.combatant import Combatant


class CombatantModelTestCase(TestCase):
    def setUp(self):
        self.discipline = Discipline.objects.create(name="Rapier", slug="rapier")
        self.authorization = Authorization.objects.create(
            name="Duke", slug="duke", discipline=self.discipline
        )
        self.combatant = Combatant.objects.create(
            sca_name="John", legal_name="John Smith"
        )

    def test_combatant_string_representation(self):
        self.assertEqual(str(self.combatant), "John Smith (John)")

    def test_combatant_with_no_sca_name(self):
        self.combatant.sca_name = None
        with self.assertRaises(ValidationError):
            self.combatant.save()

    def test_combatant_with_no_legal_name(self):
        self.combatant.legal_name = None
        with self.assertRaises(ValidationError):
            self.combatant.save()

    def test_combatant_can_have_multiple_authorizations(self):
        self.combatant.authorizations.add(self.authorization)
        self.combatant.authorizations.add(
            Authorization.objects.create(
                name="Master", slug="master", discipline=self.discipline
            )
        )
        self.assertEqual(self.combatant.authorizations.count(), 2)

    def test_combatant_authorizations_must_belong_to_discipline(self):
        with self.assertRaises(IntegrityError):
            self.combatant.authorizations.add(
                Authorization.objects.create(
                    name="Baron", slug="baron", discipline=None
                )
            )

    def test_combatant_can_have_multiple_warrants(self):
        self.combatant.warrants.add(self.authorization)
        self.combatant.warrants.add(
            Authorization.objects.create(
                name="Viscount", slug="viscount", discipline=self.discipline
            )
        )
        self.assertEqual(self.combatant.warrants.count(), 2)

    def test_combatant_warrants_must_belong_to_discipline(self):
        with self.assertRaises(IntegrityError):
            self.combatant.warrants.add(
                Authorization.objects.create(
                    name="Count", slug="count", discipline=None
                )
            )

    def test_combatant_can_have_valid_waiver(self):
        today = datetime.today().date()
        self.combatant.waiver.date_signed = today
        self.combatant.waiver.expiration_date = today.replace(year=today.year + 1)
        self.combatant.waiver.save()
        self.assertTrue(self.combatant.waiver.is_valid())

    def test_combatant_with_no_waiver_is_not_valid(self):
        self.assertFalse(self.combatant.waiver.is_valid())
