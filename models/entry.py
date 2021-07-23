from os import name, times


class Entry():
    def __init__(self, id, time, concepts, entry, mood_id):
        self.id = id
        self.time = time
        self.concepts = concepts
        self.entry = entry
        self.mood_id = mood_id
        self.mood = None
