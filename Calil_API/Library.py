import dataclasses
from typing import Any, Tuple


@dataclasses.dataclass
class Library:
    category: str
    city: str
    short: str
    libkey: str
    pref: str
    primary: bool
    faid: Any
    geocode:str
    geocode_tuple:Tuple[float,float] = dataclasses.field(init=False)
    systemid: str
    address: str
    libid: str
    tel: str
    systemname: str
    isil: Any
    post: str
    url_pc: str
    formal: str

    def __post_init__(self):
        self.geocode_tuple = tuple(map(float,self.geocode.split(",",1)))

    def asdict(self):
        return dataclasses.asdict(self)

    def astuple(self):
        return dataclasses.astuple(self)
