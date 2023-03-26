from django.test import TestCase

from cards.models.discipline import Discipline


class DisciplineTestCase(TestCase):
    def setUp(self):
        Discipline.objects.create(name="Heavy Rapier", slug="heavy-rapier")
        Discipline.objects.create(name="Armored Combat", slug="armored-combat")

    def test_discipline_name(self):
        heavy_rapier = Discipline.objects.get(name="Heavy Rapier")
        armored_combat = Discipline.objects.get(name="Armored Combat")
        self.assertEqual(heavy_rapier.name, "Heavy Rapier")
        self.assertEqual(armored_combat.name, "Armored Combat")

    def test_discipline_slug(self):
        heavy_rapier = Discipline.objects.get(name="Heavy Rapier")
        armored_combat = Discipline.objects.get(name="Armored Combat")
        self.assertEqual(heavy_rapier.slug, "heavy-rapier")
        self.assertEqual(armored_combat.slug, "armored-combat")

    def test_discipline_string_representation(self):
        heavy_rapier = Discipline.objects.get(name="Heavy Rapier")
        armored_combat = Discipline.objects.get(name="Armored Combat")
        self.assertEqual(str(heavy_rapier), "Heavy Rapier")
        self.assertEqual(str(armored_combat), "Armored Combat")
