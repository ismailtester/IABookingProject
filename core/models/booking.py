from typing import Optional
from pydantic import BaseModel
from datetime import date


class BookingDates(BaseModel):
    checkin: date
    checkout: date


class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None


class BookingResponse(BaseModel):
    bookingid: int #тип данных ключа bookingid
    booking: Booking #объект booking который содержит параметр указанный выше