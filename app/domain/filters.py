from pydantic import BaseModel


class BaseFilter(BaseModel):
    size: int | None = 10
    page: int | None = 0
    entity_id_eq: str | None = None
    order_by: str | None = None

    @property
    def offset(self):
        return (self.page) * self.size

    @property
    def limit(self):
        return self.size


class TaskFilter(BaseFilter):
    pass
