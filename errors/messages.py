class ErrorMessage:
    message = None

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.message == other:
            return True
        return False


class FieldError:
    field = None


class NonNullableField(ErrorMessage, FieldError):
    def __init__(self, field):
        self.field = field
        self.message = self.field + " is mandatory"


class ImmutableField(ErrorMessage, FieldError):
    def __init__(self, field):
        self.field = field
        self.message = self.field + " cannot be set"


class UniqueField(ErrorMessage, FieldError):
    def __init__(self, field):
        self.field = field
        self.message = self.field + " cannot be duplicated"


class AttendeeMessages(ErrorMessage):
    NON_NULLABLE_NAME = NonNullableField("Name").message
    IMMUTABLE_ID = ImmutableField("ID").message
    IMMUTABLE_CREATION_DATE = ImmutableField("Creation Date").message
    UNIQUE_NAME = UniqueField("Name").message
