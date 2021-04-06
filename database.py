"""NEODatabase
An Object that holds all neos and approaches sorted by designation to
create the object fast"""


class NEODatabase:

    def __init__(self, neos, approaches):
        designation_dict = dict()
        for neo in neos:
            if neo.designation in designation_dict:
                # attach a neo to key: designation
                designation_dict[neo.designation] = neo

        self._designations = designation_dict
        self._neos = neos
        self._approaches = approaches
        for approach in approaches:
            # all approaches lookup the designation_dict for a neo
            # if there is a designation like that we modify that neo and
            # approach
            if approach.designation in designation_dict:
                # append to a neo object this approach
                designation_dict[approach.designation].append(approach)
                # attach the neo object to this approach
                approach.attach(designation_dict[approach.designation])

    def get_neo_by_designation(self, designation):
        if designation in self._designations:
            # this will return a neo by designation
            return self._designations[designation]
        else:
            return None

    def get_neo_by_name(self, name):
        # return a neo by name or None
        for neo in self._neos:
            if neo.neo_name == name:
                return neo
        return None

    def query(self, filters=()):
        # for each approach we have to check the filters
        for approach in self._approaches:
            # mapped returns something like [True, False, True] for filters
            mapped = map(lambda x: x(approach), filters)
            # if all flags are True like [True, True, True]
            if all(flag is True for flag in mapped):
                # we can yield that approach, because it matches all
                # filter criteriums
                yield approach
