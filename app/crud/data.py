from app.models import Data

from .base import CrudBase

data_crud = CrudBase[Data](Data)
