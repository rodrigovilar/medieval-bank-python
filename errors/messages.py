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
        self.message = f"{self.field} is mandatory"


class ImmutableField(ErrorMessage, FieldError):
    def __init__(self, field):
        self.field = field
        self.message = f"{self.field} cannot be set"


class WrongRegexField(ErrorMessage, FieldError):
    def __init__(self, field):
        self.field = field
        self.message = f"{self.field} format is invalid"


class UniqueField(ErrorMessage, FieldError):
    def __init__(self, field):
        self.field = field
        self.message = f"{self.field} cannot be duplicated"


class UnknownField(ErrorMessage, FieldError):
    def __init__(self, field, _class, field_value):
        self.field = field
        self.message = f"Unknown {_class} with {field}: {field_value}"


class NullInstance(ErrorMessage):
    def __init__(self, _class):
        self.message = f"Null {_class}"


class AttendeeMessages(ErrorMessage):
    attendee_id = None

    def __init__(self, attendee_id=None):
        self.attendee_id = attendee_id

    NON_NULLABLE_NAME = NonNullableField("Name").message
    IMMUTABLE_ID = ImmutableField("ID").message
    IMMUTABLE_CREATION_DATE = ImmutableField("Creation Date").message
    UNIQUE_NAME = UniqueField("Name").message
    WRONG_FORMAT_EMAIL = WrongRegexField("E-mail").message
    UNKNOWN_ID = UnknownField("ID", "Attendee", attendee_id).message
    NULL_ATTENDEE = NullInstance("attendee").message
