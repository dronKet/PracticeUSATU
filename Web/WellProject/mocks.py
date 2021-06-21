from django.http import Http404
from numpy import random


class Well:
    wells = [
        {
            'id': 1,
            'name': 'First Well',
            'Coordinate':
                {
                    'x': random.randint(10, size=10),
                    'y': random.randint(10, size=10),
                    'z': random.randint(10, size=10),
                }
        },
        {
            'id': 2,
            'name': 'Second Well',
            'Coordinate':
                {
                    'x': random.randint(10, size=10),
                    'y': random.randint(10, size=10),
                    'z': random.randint(10, size=10),
                },
        },
        {
            'id': 3,
            'name': 'Third Well',
            'Coordinate':
                {
                    'x': random.randint(10, size=10),
                    'y': random.randint(10, size=10),
                    'z': random.randint(10, size=10),
                },
        },
    ]

    @classmethod
    def all(cls):
        return cls.wells

    @classmethod
    def find(cls, id):
        try:
            return cls.wells[int(id) - 1]
        except:
            raise Http404('Sorry, information about well #{} not found'.format(id))
