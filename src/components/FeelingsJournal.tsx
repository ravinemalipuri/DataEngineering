
import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Language, getTranslation } from '@/translations';
import { format } from 'date-fns';

interface JournalEntry {
  id: string;
  feeling: string;
  comment: string;
  username: string;
  timestamp: string;
  language: Language;
}

interface FeelingsJournalProps {
  feeling: string;
  language: Language;
  children: React.ReactNode;
}

const FeelingsJournal: React.FC<FeelingsJournalProps> = ({ feeling, language, children }) => {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [newComment, setNewComment] = useState('');
  const [username, setUsername] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  // Load entries from localStorage on component mount
  useEffect(() => {
    const savedEntries = localStorage.getItem('feelingsJournalEntries');
    if (savedEntries) {
      setEntries(JSON.parse(savedEntries));
    }

    // Get or set username
    const savedUsername = localStorage.getItem('journalUsername');
    if (savedUsername) {
      setUsername(savedUsername);
    } else {
      const defaultUsername = `User${Math.floor(Math.random() * 1000)}`;
      setUsername(defaultUsername);
      localStorage.setItem('journalUsername', defaultUsername);
    }
  }, []);

  // Save entries to localStorage whenever entries change
  useEffect(() => {
    localStorage.setItem('feelingsJournalEntries', JSON.stringify(entries));
  }, [entries]);

  const validateLanguageInput = (text: string, lang: Language): boolean => {
    switch (lang) {
      case 'te':
        // Telugu Unicode range
        return /^[\u0C00-\u0C7F\s.,!?]*$/.test(text);
      case 'es':
        // Spanish characters
        return /^[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s.,!?]*$/.test(text);
      case 'ta':
        // Tamil Unicode range
        return /^[\u0B80-\u0BFF\s.,!?]*$/.test(text);
      default:
        // English only
        return /^[a-zA-Z\s.,!?]*$/.test(text);
    }
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    if (validateLanguageInput(value, language)) {
      setNewComment(value);
    }
  };

  const handleAddEntry = () => {
    if (newComment.trim()) {
      const newEntry: JournalEntry = {
        id: Date.now().toString(),
        feeling,
        comment: newComment.trim(),
        username,
        timestamp: format(new Date(), 'yyyy-MM-dd HH:mm:ss'),
        language
      };

      setEntries(prev => [newEntry, ...prev]);
      setNewComment('');
    }
  };

  const getFeelingEntries = () => {
    return entries.filter(entry => entry.feeling === feeling && entry.language === language);
  };

  const getPlaceholderText = () => {
    switch (language) {
      case 'te':
        return 'మీ భావనలను తెలుగులో వ్రాయండి...';
      case 'es':
        return 'Escribe tus sentimientos en español...';
      case 'ta':
        return 'உங்கள் உணர்வுகளை தமிழில் எழுதுங்கள்...';
      default:
        return 'Write your feelings in English...';
    }
  };

  const feelingEntries = getFeelingEntries();

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        {children}
      </DialogTrigger>
      <DialogContent className="max-w-md max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-lg font-semibold">
            {getTranslation('journal.feelingJournal', language)} - {feeling}
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4">
          {/* Add new entry form */}
          <div className="space-y-3">
            <Textarea
              value={newComment}
              onChange={handleTextChange}
              placeholder={getPlaceholderText()}
              className="min-h-[80px] resize-none"
              maxLength={500}
            />
            <Button 
              onClick={handleAddEntry}
              disabled={!newComment.trim()}
              className="w-full"
            >
              {getTranslation('journal.addEntry', language)}
            </Button>
          </div>

          {/* Display existing entries */}
          <div className="space-y-3 max-h-[300px] overflow-y-auto">
            <h4 className="font-semibold text-sm">
              {getTranslation('journal.previousEntries', language)} ({feelingEntries.length})
            </h4>
            
            {feelingEntries.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-4">
                {getTranslation('journal.noEntries', language)}
              </p>
            ) : (
              feelingEntries.map((entry) => (
                <div key={entry.id} className="bg-muted p-3 rounded-lg space-y-2">
                  <p className="text-sm">{entry.comment}</p>
                  <div className="flex justify-between items-center text-xs text-muted-foreground">
                    <span>{entry.username}</span>
                    <span>{entry.timestamp}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default FeelingsJournal;
