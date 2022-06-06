import uuid
from dataclasses import field

class Model(object):
    id: uuid.UUID = field(hash=True)
    @classmethod
    def next_id(cls) -> uuid:
        return uuid.uuid4()
    pass

class AggregateReferenceModel(object):
    pass

class ValueObject(object):
    pass

class Entity(Model):
    pass

class Factory(AggregateReferenceModel):
    pass

class Repository(AggregateReferenceModel):
    pass

class Service(AggregateReferenceModel):
    pass