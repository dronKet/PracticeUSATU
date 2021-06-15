from django.http import Http404


class Well:
    wells = [
        {
            'id': 1,
            'name': 'First Well',
            'Coordinate': [
                {
                    'x': 10,
                    'y': 10,
                    'z': 10,
                },
                {
                    'x': 20,
                    'y': 20,
                    'z': 20,
                },
                {
                    'x': 30,
                    'y': 30,
                    'z': 30,
                },
            ]
        },
        {
            'id': 2,
            'name': 'Second Well',
            'Coordinate': [
                {
                    'x': 11,
                    'y': 11,
                    'z': 11,
                },
                {
                    'x': 21,
                    'y': 21,
                    'z': 21,
                },
                {
                    'x': 31,
                    'y': 31,
                    'z': 31,
                },
            ]
        },
        {
            'id': 3,
            'name': 'Third Well',
            'Coordinate': [
                {
                    'x': 12,
                    'y': 12,
                    'z': 12,
                },
                {
                    'x': 22,
                    'y': 22,
                    'z': 22,
                },
                {
                    'x': 32,
                    'y': 32,
                    'z': 32,
                },
            ]
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
            raise Http404('Error 404')
