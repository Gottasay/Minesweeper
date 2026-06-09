class InvalidModeError(Exception):
    """Raised when trying to choose a non-existent mode."""
    pass

class InvalidInputError(ValueError):
    """Raised when trying to enter the mode and coordinates in incorrect format."""
    pass

class InvalidCoordinatesError(Exception):
    """Raised when trying to open or set flag on a cell with invalid coordinates."""
    pass

class FlaggedCellError(Exception):
    """Raised when trying to open or set flag on a cell that has a flag on it."""
    pass

class CellAlreadyOpenedError(Exception):
    """Raised when trying to open a cell that is already opened."""
    pass