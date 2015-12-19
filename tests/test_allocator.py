# !/usr/bin/python
# title          :amity/alloc.py
# description    :An algorithm which randomly allocates
#                 persons to rooms in a building.
# author         :Jee Githinji
# email          :githinji.gikera@andela.com
# date           :20151218
# version        :0.0.1
# python_version :2.7.10
# ==============================================================================

import unittest
import nose

from random import randint
from employees.model import Person, Fellow, Staff
from rooms.models import LivingSpace, Office
from amity import Amity
""" file path to the input .txt file containing people """
file_path = 'input.txt'
persons = []
fellow_only = []

# a list of living space
livings = [
    'green', 'blue', 'yellow', 'lilac',
    'orange', 'white', 'brown',
    'turquoise', 'grey', 'purple'
]
# create the office list
livings_list = [
    LivingSpace(living_space_name)
    for living_space_name in livings
]

# a list of offices
offices = [
    "allegro", "boma", "valhalla",
    "hogwarts", "krypton", "oculus",
    "gondolla", "amitoid", "punta", "borabora"
]
# instantiate offices and store them in a list
offices_list = [Office(office_name) for office_name in offices]


class RoomPersonTestCase(unittest.TestCase):
    """ test the instantiation of rooms and people """

    def setup(self):
        self.office = Office()
        self.living = LivingSpace()
        self.office.populate_room_names()
        self.living.populate_room_names()
        self.f = Person.create(
            'Jee Gikera', 'fellow', wants_accomodation=True)
        self.staff = Person.create('Chidi Nnadi', 'staff')

    def test_room_creation(self):
        """ create rooms and test against their class instances """
        self.office = Office('Valhalla')
        self.living = LivingSpace('PeckingOrder')
        self.assertIsInstance(self.office, Office)
        self.assertIsInstance(self.living, LivingSpace)

    def test_fellow_staff_creation(self):
        """ create employees and test against their class instances """
        self.fellow = Person.create(
            'Jee Gikera', 'fellow', wants_accomodation=True)
        self.staff = Person.create('Chidi Nnadi', 'staff')
        self.assertIsInstance(self.fellow, Fellow)
        self.assertIsInstance(self.staff, Staff)


class AllocationTestCase(unittest.TestCase):
    """ tests the allocation of rooms to persons """

    def test_room_generation(self):
        """ generate rooms and test their specs """
        self.office = Office('TopOffice')
        self.living = LivingSpace('WoodWing')
        office_size = self.office.capacity
        living_size = self.living.capacity
        self.assertEquals(office_size, 6)
        self.assertEquals(living_size, 4)

    def test_allocation_to_rooms(self):
        """ tests the allocation of rooms """
        self.f = Person.create(
            'Jee Gikera', 'fellow', wants_accomodation='Y')
        self.s = Person.create('Chidi Nnadi', 'staff')
        persons.append(self.s)
        persons.append(self.f)
        fellow_only.append(self.f)
        self.office = Office('GreenHouse')
        self.living = LivingSpace('BlueMoon')
        self.a = Amity()

        fellows_l_space = self.a.allocate_office_space(offices_list, self.f)
        self.a.allocate_office_space(livings_list, self.s)
        un = self.office.unallocated_people(persons)
        unl = self.living.unallocated_people(fellow_only)
        self.assertEquals(un, [])
        self.assertEquals(unl, [])

        allocated = self.office.get_occupants()
        self.assertEquals(self.s.has_living_space(), False)
        self.assertEquals(self.f.has_living_space(), True)
        self.assertEquals(self.s.has_office(), True)
        self.assertEquals(self.f.has_office(), True)
        self.assertIsNotNone(allocated)
        self.assertIsNotNone(fellows_l_space)

    def test_finding_room_occupants(self):
        """ tests getting a given room's occupants """
        self.amity = Amity()
        o = self.amity.allocate_office_space(
            offices_list, file_path, is_a_file=True)
        l = self.amity.allocate_living_space(
            livings_list, file_path, is_a_file=True)
        office_roomies = o[0].get_occupants()
        living_roomies = l[0].get_occupants()
        self.assertIsInstance(office_roomies[0], Person)
        self.assertIsInstance(living_roomies[0], Person)


class FileInputTestCase(unittest.TestCase):
    """ tests file IO to the program """

    def test_can_parse_people_from_file(self):
        persons = Amity.get_people_from_file(file_path)
        self.assertEquals(len(persons), 43)
        self.assertIsInstance(persons[randint(0, 30)], Person)

if __name__ == '__main__':
    nose.run()
