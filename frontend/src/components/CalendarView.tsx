import React from 'react';
import { Calendar, dateFnsLocalizer, Event as CalendarEvent  } from "react-big-calendar";
import "react-big-calendar/lib/css/react-big-calendar.css";
import { useEffect, useMemo } from "react";
import { useSlotContext, Slot } from "./SlotContext";
import { format, parse, startOfWeek, getDay } from "date-fns";
import './CalendarView.css';

import { enUS } from 'date-fns/locale';

const locales = {
  "en-US": enUS,
};

interface CustomEvent extends CalendarEvent {
  id: string; // Add 'id' property explicitly
}

interface CustomEventProps {
  event: CustomEvent;  // Correctly type the event prop as a CalendarEvent
  onDelete: (eventId: string) => void;
}



const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const CustomEvent: React.FC<CustomEventProps> = ({ event, onDelete }) => (
    <span
       onClick={(e) => {
        e.stopPropagation(); // Prevent calendar event click from firing
        onDelete(event.id as string); // Cast to number if event.id is a string
      }}
      className="delete-icon"
    >
      ✖
    </span>
);

const CalendarView: React.FC = () => {
    const { slots, setSlots } = useSlotContext();

    const handleDeleteSlot = (slotId: string) => {
        alert(`Delete event with ID: ${slotId}`);
        console.log(`Delete event with ID: ${slotId}`)
        const deleteSlot = async (slotId: string) => {
          try {
            const res = await fetch(`/api/slots/${slotId}/`, {
              method: "DELETE",
            });

            if (res.status === 204) {
              console.log("Slot deleted successfully");
              setSlots((prevSlots) => prevSlots.filter((slot) => String(slot.id) !== slotId));
              // Optionally update your state to remove the deleted slot
            } else {
              console.error("Failed to delete slot");
            }
          } catch (error) {
            console.error("Error deleting slot:", error);
          }
        };
          deleteSlot(slotId);

        // Implement your logic to delete the event, such as making a request to your API
    };

    useEffect(() => {
        console.log("New slots length:", slots.length);
        if (slots.length > 0) {
          console.log("New slots available:", slots);
          // Update calendar events here!
        }
        const fetchExistingSlots = async () => {
          try {
            const res = await fetch("/api/slots"); // Adjust endpoint if needed
            const data = await res.json();
            setSlots((prevSlots: Slot[]) => [...prevSlots, ...data.slots]);
          } catch (err) {
            console.error("Failed to load existing slots:", err);
          }
          };
          fetchExistingSlots();

    }, []);

    const events = useMemo(() => {
        return slots.map((slot: {id: string, company: string, date: string; start: string; end: string }) => {
          const start = new Date(`${slot.date}T${slot.start}`);
          const end = new Date(`${slot.date}T${slot.end}`);
          const companyName = `${slot.company}`;
          const id = `${slot.id}`;

          return {
            title: companyName,
            start,
            end,
            allDay: false,
            id,
          };
        });
    }, [slots]);

  return (
    <div style={{ padding: "20px", height: "90vh" }}>
      <h2>📅 Calendar</h2>
      <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{ height: "80vh" }}
          selectable={true}  // Allow selecting events
          onSelectEvent={(event) => {
            alert(`Selected event: ${event.title}`); // Handle event click or selection
          }}
          components={{
              event: (props) => <CustomEvent  {...props} onDelete={handleDeleteSlot} />,
          }}
        />
    </div>
  );
};

export default CalendarView;
