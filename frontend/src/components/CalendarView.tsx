import { Calendar, dateFnsLocalizer } from "react-big-calendar";
import "react-big-calendar/lib/css/react-big-calendar.css";
import { useEffect, useMemo } from "react";
import { useSlotContext, Slot } from "./SlotContext";
import { format, parse, startOfWeek, getDay } from "date-fns";


import { enUS } from 'date-fns/locale';

const locales = {
  "en-US": enUS,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const CalendarView = () => {
    const { slots, setSlots } = useSlotContext();

    useEffect(() => {
        console.log("New slots length:", slots.length);
        if (slots.length > 0) {
          console.log("New slots available:", slots);
          // Update calendar events here!
        }
        const fetchExistingSlots = async () => {
          try {
            const res = await fetch("http://localhost:8000/api/slots"); // Adjust endpoint if needed
            const data = await res.json();
            setSlots((prevSlots: Slot[]) => [...prevSlots, ...data.slots]);
          } catch (err) {
            console.error("Failed to load existing slots:", err);
          }
          };
          fetchExistingSlots();

    }, []);

    const events = useMemo(() => {
        return slots.map((slot: { company: string, date: string; start: string; end: string }) => {
          const start = new Date(`${slot.date}T${slot.start}`);
          const end = new Date(`${slot.date}T${slot.end}`);
          const companyName = `${slot.company}`;
          return {
            title: companyName,
            start,
            end,
            allDay: false,
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
        />
    </div>
  );
};

export default CalendarView;
