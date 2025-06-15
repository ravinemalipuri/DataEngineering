
import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface FeelingEntry {
  id: string;
  text: string;
  date: string; // ISO string
}

const LOCAL_STORAGE_KEY = "feeling_journal_entries_v1";

const loadFromLocalStorage = (): FeelingEntry[] => {
  try {
    const data = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (!data) return [];
    return JSON.parse(data);
  } catch {
    return [];
  }
};

const saveToLocalStorage = (entries: FeelingEntry[]) => {
  localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(entries));
};

const downloadFile = (entries: FeelingEntry[]) => {
  const blob = new Blob([JSON.stringify(entries, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = window.URL.createObjectURL(blob);
  link.download = "feelings.json";
  link.click();
};

const importFile = (setter: (entries: FeelingEntry[]) => void) => {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".json,application/json";
  input.onchange = (e: any) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const entries = JSON.parse(event.target?.result as string);
        if (Array.isArray(entries)) {
          setter(entries.filter(x => x.id && x.text && x.date));
        }
      } catch {
        alert("Invalid file. Please select a valid feelings JSON file.");
      }
    };
    reader.readAsText(file);
  };
  input.click();
};

export default function FeelingsJournal() {
  const [entries, setEntries] = useState<FeelingEntry[]>([]);
  const [draft, setDraft] = useState("");

  useEffect(() => {
    setEntries(loadFromLocalStorage());
  }, []);

  useEffect(() => {
    saveToLocalStorage(entries);
  }, [entries]);

  const handleAdd = () => {
    if (!draft.trim()) return;
    setEntries([
      {
        id: Date.now() + Math.random().toString(16),
        text: draft.trim(),
        date: new Date().toISOString(),
      },
      ...entries,
    ]);
    setDraft("");
  };

  return (
    <section id="journal" className="mt-12 bg-card rounded-2xl p-6 border border-border shadow-lg max-w-xl mx-auto">
      <h3 className="text-2xl font-bold mb-2 text-center">Your Feelings Journal</h3>
      <p className="text-muted-foreground mb-4 text-center">Write and save your feelings privately on this device.</p>
      <Textarea
        className="mb-2 min-h-[80px]"
        placeholder="How are you feeling today? Write your thoughts..."
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={(e) => { if(e.ctrlKey && e.key === "Enter"){ handleAdd(); } }}
      />
      <div className="flex gap-2 mb-4">
        <Button onClick={handleAdd} disabled={!draft.trim()}>Add Entry</Button>
        <Button variant="secondary" onClick={() => downloadFile(entries)} disabled={entries.length === 0}>
          Download My Feelings
        </Button>
        <Button variant="outline" onClick={() => importFile(setEntries)}>
          Import Feelings
        </Button>
      </div>
      <div>
        {entries.length === 0 ? (
          <div className="p-4 text-center text-muted-foreground">No feelings saved yet.</div>
        ) : (
          <ul className="space-y-3 max-h-72 overflow-y-auto">
            {entries.map((entry) => (
              <li key={entry.id} className="rounded-xl bg-background border p-3 shadow-sm">
                <div className="mb-1 text-xs text-muted-foreground">{new Date(entry.date).toLocaleString()}</div>
                <div>{entry.text}</div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
