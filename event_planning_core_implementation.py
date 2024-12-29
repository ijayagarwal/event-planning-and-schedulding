# models.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid

class EventStatus(Enum):
    DRAFT = "draft"
    PLANNED = "planned"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User:
    def __init__(self, name: str, email: str, role: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = role  # organizer, client, vendor

class Event:
    def __init__(self, title: str, client_id: str, organizer_id: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.client_id = client_id
        self.organizer_id = organizer_id
        self.status = EventStatus.DRAFT
        self.start_date = None
        self.end_date = None
        self.budget = 0
        self.actual_cost = 0
        self.vendors = []
        self.notifications = []

class Vendor:
    def __init__(self, name: str, service_type: str, rate: float):
        self.id = str(uuid.uuid4())
        self.name = name
        self.service_type = service_type
        self.rate = rate
        self.availability = []

# services.py
class SchedulingService:
    def __init__(self):
        self.events = []

    def check_availability(self, start_date: datetime, end_date: datetime) -> bool:
        for event in self.events:
            if (event.start_date <= start_date <= event.end_date or
                event.start_date <= end_date <= event.end_date):
                return False
        return True

    def schedule_event(self, event: Event, start_date: datetime, end_date: datetime) -> bool:
        if self.check_availability(start_date, end_date):
            event.start_date = start_date
            event.end_date = end_date
            self.events.append(event)
            return True
        return False

class BudgetService:
    @staticmethod
    def update_budget(event: Event, amount: float) -> None:
        event.budget = amount

    @staticmethod
    def track_expense(event: Event, amount: float, description: str) -> None:
        event.actual_cost += amount
        if event.actual_cost > event.budget:
            NotificationService.send_notification(
                event,
                f"Budget warning: Expenses exceeded budget by {event.actual_cost - event.budget}"
            )

class VendorManagementService:
    def __init__(self):
        self.vendors = []

    def add_vendor(self, vendor: Vendor) -> None:
        self.vendors.append(vendor)

    def find_available_vendors(self, service_type: str, date: datetime) -> List[Vendor]:
        return [
            vendor for vendor in self.vendors
            if vendor.service_type == service_type and date not in vendor.availability
        ]

class NotificationService:
    @staticmethod
    def send_notification(event: Event, message: str) -> None:
        event.notifications.append({
            'timestamp': datetime.now(),
            'message': message
        })
        # In a real implementation, this would send emails, push notifications, etc.

# main.py
class EventPlanningSystem:
    def __init__(self):
        self.scheduling_service = SchedulingService()
        self.vendor_service = VendorManagementService()
        self.users = []

    def create_event(self, title: str, client_id: str, organizer_id: str) -> Event:
        event = Event(title, client_id, organizer_id)
        return event

    def update_event_status(self, event: Event, status: EventStatus) -> None:
        event.status = status
        NotificationService.send_notification(
            event,
            f"Event status updated to {status.value}"
        )

# Example usage
def main():
    # Initialize the system
    system = EventPlanningSystem()

    # Create users
    organizer = User("John Doe", "john@example.com", "organizer")
    client = User("Jane Smith", "jane@example.com", "client")
    system.users.extend([organizer, client])

    # Create an event
    event = system.create_event("Annual Conference 2024", client.id, organizer.id)

    # Set budget
    BudgetService.update_budget(event, 50000.0)

    # Schedule the event
    start_date = datetime(2024, 6, 1, 9, 0)
    end_date = datetime(2024, 6, 3, 17, 0)
    if system.scheduling_service.schedule_event(event, start_date, end_date):
        print("Event scheduled successfully")

    # Add vendors
    vendor = Vendor("ABC Catering", "catering", 1000.0)
    system.vendor_service.add_vendor(vendor)

    # Track expenses
    BudgetService.track_expense(event, 5000.0, "Venue booking")
    BudgetService.track_expense(event, 3000.0, "Catering advance")

    # Update status
    system.update_event_status(event, EventStatus.CONFIRMED)

if __name__ == "__main__":
    main()


## This is the main core implementation of the given problem