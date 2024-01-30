from pydantic import BaseModel, Field


class ChooseAGoodName(BaseModel):
    class_member1: str
    class_member2: float
    class_member3: list = Field(default_factory=list)

    def useful_function(self):
        True

    def another_useful_function(self):
        True
