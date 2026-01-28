import psycopg2.errors as errors


def _short_db_error(e: Exception) -> str:
    if isinstance(e, errors.RaiseException) and getattr(e, "diag", None) and e.diag.message_primary:
        return str(e.diag.message_primary)

    if isinstance(e, errors.UniqueViolation):
        return "Taki rekord już istnieje."
    if isinstance(e, errors.ForeignKeyViolation):
        return "Nie można wykonać operacji, ponieważ rekord jest powiązany z innymi danymi."
    if isinstance(e, errors.NotNullViolation):
        return "Wymagane pole nie może być puste."
    if isinstance(e, errors.CheckViolation):
        return "Wartość nie spełnia wymagań (reguła CHECK)."
    if isinstance(e, errors.InvalidTextRepresentation):
        return "Nieprawidłowy format danych."
    if isinstance(e, errors.DatatypeMismatch):
        return "Nieprawidłowy typ danych."
    if isinstance(e, errors.StringDataRightTruncation):
        return "Wprowadzony tekst jest za długi."
    if isinstance(e, errors.NumericValueOutOfRange):
        return "Wartość liczbowa jest poza zakresem."
    if isinstance(e, errors.DatetimeFieldOverflow):
        return "Nieprawidłowa data."

    return "Wystąpił błąd bazy danych."