import  { useState } from "react";
import { useSlotContext, Slot } from "./SlotContext";

const ChatBox = () => {
    const [input, setInput] = useState("");
    const [chat, setChat] = useState<string[]>([]);
    const { setSlots } = useSlotContext();
    const handleSend = async () => {
        if (!input.trim()) return;
        setChat(prev => [...prev, `🧑: ${input}`]);
        const res = await fetch("http://localhost:8000/api/chat/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: input }),
        });
        const data = await res.json();

        if (data.response_type === "slots") {
          setSlots((prevSlots: Slot[]) => [...prevSlots, ...data.slots]);  // 👈 This updates global context
          setChat(prev => [
              ...prev,
              `🤖:\n` +
                (data.slots as { company: string, date: string; start: string; end: string }[])
                      .map((slot) => `🏢 ${slot.company}  📅 ${slot.date} 🕒 ${slot.start} - ${slot.end}`)
                      .join('\n')
          ]);
          setInput("");
        } else {
          setChat(prev => [...prev, `🤖: ${data.response}`]);
          setInput("");
        }
    };


    return (
        <div style={{ padding: "20px" }}>
          <h2>💬 Chat</h2>
          <div style={{ height: "60vh", overflowY: "auto", marginBottom: "10px" }}>
            {chat.map((line, i) => (
              <div key={i}>{line}</div>
            ))}
          </div>
          <input
            style={{ width: "80%" }}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button onClick={handleSend}>Send</button>
        </div>
    );
};
export default ChatBox;