from pydantic import BaseModel


class ApplicationPostSchema(BaseModel):
    name: str
    chain: str

    class Config:
        orm_mode = True


class ApplicationListSchema(BaseModel):
    name: str
    chain: str
    application_id: str

    class Config:
        orm_mode = True


class ApplicationDetailSchema(BaseModel):
    name: str
    chain: str
    application_id: str
    application_secret: str

    class Config:
        orm_mode = True
