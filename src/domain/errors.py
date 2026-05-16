class DomainError(ValueError):
    """Base class for domain invariant violations."""


class ValidationError(DomainError):
    pass


class NotFoundError(DomainError):
    pass


class InvalidMoneyAmountError(DomainError):
    pass


class DefaultOfferConflictError(DomainError):
    pass


class InactiveDefaultOfferError(DomainError):
    pass


class EmptyBundleError(DomainError):
    pass


class InvalidBundleComponentError(DomainError):
    pass
