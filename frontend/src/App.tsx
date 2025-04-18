
import './App.css'
import CalendarView from "./components/CalendarView";
import ChatBox from "./components/ChatBox";
import { SlotProvider } from "./components/SlotContext";

const App = () => {
  return (
      <SlotProvider>
        <div style={{ display: "flex", height: "100vh" }}>
          <div style={{ flex: 3, borderRight: "1px solid #ddd" }}>
            <CalendarView />
          </div>
          <div style={{ flex: 1 }}>
            <ChatBox />
          </div>
        </div>
      </SlotProvider>
  );
};

export default App;
