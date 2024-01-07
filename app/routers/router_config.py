from ..models import models
from ..models.schemas.appointment_schema import *
from ..models.schemas.barber_schema import BarberCreate, BarberUpdate
from ..models.schemas.inventory_schema import *
from ..models.schemas.location_schema import *
from ..models.schemas.promotion_schema import *
from ..models.schemas.review_schema import *
from ..models.schemas.role_schema import RoleOut, RoleCreate
from ..models.schemas.service_schema import *
from ..models.schemas.time_slot_schema import *

router_configs = [
    ("barbers", BarberOut, BarberCreate, BarberUpdate, models.Barber, "barber_id"),
    ("roles", RoleOut, RoleCreate, RoleCreate, models.Role, "role_id"),
    ("location", LocationOut, LocationCreate, LocationCreate, models.Location, "location_id"),
    ("services", ServiceOut, ServiceCreate, ServiceCreate, models.Service, "service_id"),
    ("inventory", InventoryOut, InventoryCreate, InventoryCreate, models.Inventory, "inventory_id"),
    ("appointments", AppointmentsOut, AppointmentsCreate, AppointmentsCreate, models.Appointment, "appointment_id"),
    ("review", ReviewOut, ReviewCreate, ReviewCreate, models.Review, "review_id"),
    ("promotion", PromotionOut, PromotionCreate, PromotionCreate, models.Promotion, "promotion_id"),
    ("timeSlot", TimeSlotOut, TimeSlotCreate, TimeSlotCreate, models.TimeSlot, "slot_id"),
]