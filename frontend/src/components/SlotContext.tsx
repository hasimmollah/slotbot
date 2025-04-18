import  { createContext, useContext, useState, ReactNode } from "react";

export interface Slot {
  company: string;
  date: string;
  start: string;
  end: string;
}


interface SlotContextType  {
  slots: Slot[]; // Replace `any` with your actual slot type if known
  setSlots: React.Dispatch<React.SetStateAction<Slot[]>>;
};

const SlotContext = createContext<SlotContextType | undefined>(undefined);

export const SlotProvider = ({ children }: { children: ReactNode })  => {
  const [slots, setSlots] = useState<Slot[]>([]);

  return (
    <SlotContext.Provider value={{ slots, setSlots }}>
      {children}
    </SlotContext.Provider>
  );
};

export const useSlotContext = () => {
  const context = useContext(SlotContext);
  if (!context) {
    throw new Error('useSlotContext must be used within a SlotProvider');
  }
  return context;
};