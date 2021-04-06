from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    _all_objects = dict()
    _counter = 0

    def __init__(self, designation, name, diameter, hazardous='N'):
        self._designation = designation
        if name:
            self.name = name
        else:
            self.name = None
        if diameter:
            self.diameter = float(diameter)
        else:
            self.diameter = float('nan')
        if hazardous == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False
        self.approaches = list()

        # private attributes to define obj_id
        self._object_id = NearEarthObject._counter

        # Increment so the next object has an incremented ID
        NearEarthObject._counter += 1
        # create a class list for all instances of NEO
        NearEarthObject._all_objects[self._object_id] = self

    def serialize(self):
        return {'designation': self.designation,
                'name': self.name,
                'diameter_km': self.diameter,
                'potentially_hazarous': self.hazardous}

    # let's make it an iterable class
    def __getitem__(self, index):
        return self[index]

    def __next__(self):
        try:
            result = self._all_objects[self._object_id]
        except IndexError:
            raise StopIteration
        self._object_id += 1
        return result

    def show_approaches(self, limit=5):
        if self.approaches:
            count = 0
            for approach in self.approaches:
                if count < limit:
                    print(approach)
                    count += 1
                else:
                    break

    def append(self, item):
        if type(item) == CloseApproach:
            self.approaches.append(item)

    @property
    def object_id(self):
        return self._object_id

    @property
    def designation(self):
        return self._designation

    @property
    def neo_name(self):
        return self.name

    # return full name of the NEO
    @property
    def fullname(self):
        # if name is not empty return long fullname else short
        if self.name:
            return f"{self.designation} - {self.name}"
        else:
            return f"{self.designation}"

    # return the string representation of the NEO
    def __str__(self):
        hazard = ''
        if self.hazardous:
            hazard = 'a hazardous NEO'
        else:
            hazard = 'is not a hazardous NEO'

        return(f'A NearEarthObject {self.fullname} has a diameter of {self.diameter:.3f} km and is {hazard}')


    # return repr representation of the NEO
    def __repr__(self):
        return (f"NearEarthObject({self.fullname}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r}, "
                f"approaches={self.approaches}")


class CloseApproach:
    def __init__(self, designation, time, distance, velocity, neo=None):
        self._designation = designation
        if type(time) == str:
            self.time = cd_to_datetime(time)

        if type(distance) == float:
            self.distance = distance
        else:
            self.distance = float(distance)

        if type(velocity) == float:
            self.velocity = velocity
        else:
            self.velocity = float(velocity)

        if neo:
            self.neo = neo
        else:
            self.neo = None

    def serialize(self):
        return {'datetime_utc': datetime_to_str(self.time),
                'distance_au': self.distance,
                'velocity_km_s': self.velocity}

    def __getitem__(self, index):
        return self[index]

    @property
    def designation(self):
        return self._designation

    @property
    def time_str(self):
        return datetime_to_str(self.time)

    def attach(self, neo):
        if type(neo) == NearEarthObject:
            self.neo = neo

    def __str__(self):
        return (f"At {self.time_str}, '{self.designation}' approaches Earth at"
                f"a distance of {self.distance:.2f} au and a velocity of "
                f"{self.velocity:.2f} km/s. Hazardous: {self.neo.hazardous}")

    def __repr__(self):
        return (f"CloseApproach(time={self.time_str!r},"
                f"distance={self.distance:.2f},"
                f"velocity={self.velocity:.2f})")
