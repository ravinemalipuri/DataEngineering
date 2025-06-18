
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Language, getTranslation } from '@/translations';
import { format } from 'date-fns';
import { getEmotionsData } from '@/data/emotions';
import { BookOpen, Plus } from 'lucide-react';

interface JournalEntry {
  id: string;
  feeling: string;
  comment: string;
  username: string;
  timestamp: string;
  language: Language;
}

interface StandaloneFeelingsJournalProps {
  language: Language;
}

const StandaloneFeelingsJournal: React.FC<StandaloneFeelingsJournalProps> = ({ language }) => {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [newComment, setNewComment] = useState('');
  const [selectedFeeling, setSelectedFeeling] = useState<string>('');
  const [username, setUsername] = useState('');
  const [showEntries, setShowEntries] = useState(false);

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
    if (newComment.trim() && selectedFeeling) {
      const newEntry: JournalEntry = {
        id: Date.now().toString(),
        feeling: selectedFeeling,
        comment: newComment.trim(),
        username,
        timestamp: format(new Date(), 'yyyy-MM-dd HH:mm:ss'),
        language
      };

      setEntries(prev => [newEntry, ...prev]);
      setNewComment('');
      setSelectedFeeling('');
    }
  };

  const getFilteredEntries = () => {
    return entries.filter(entry => entry.language === language);
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

  const getAllEmotionsWithTranslations = () => {
    const emotionsData = getEmotionsData(language);
    const allEmotions: Array<{value: string, display: string}> = [];
    
    emotionsData.forEach(level1 => {
      // Add level 1 emotions
      const translatedName = getTranslation(`emotions.${level1.id}`, language);
      const englishName = getTranslation(`emotions.${level1.id}`, 'en');
      const displayText = language === 'en' ? englishName : `${translatedName} (${englishName})`;
      allEmotions.push({
        value: translatedName,
        display: displayText
      });
      
      // Add level 2 emotions
      level1.level2Emotions.forEach(level2 => {
        const translatedName = getTranslation(`emotions.${level2.id}`, language);
        const englishName = getTranslation(`emotions.${level2.id}`, 'en');
        const displayText = language === 'en' ? englishName : `${translatedName} (${englishName})`;
        allEmotions.push({
          value: translatedName,
          display: displayText
        });
        
        // Add level 3 emotions
        level2.level3Emotions.forEach(level3 => {
          const translatedName = getTranslation(`emotions.${level3.id}`, language);
          const englishName = getTranslation(`emotions.${level3.id}`, 'en');
          const displayText = language === 'en' ? englishName : `${translatedName} (${englishName})`;
          allEmotions.push({
            value: translatedName,
            display: displayText
          });
        });
      });
    });
    
    // Remove duplicates and sort
    const uniqueEmotions = allEmotions.filter((emotion, index, self) => 
      index === self.findIndex(e => e.value === emotion.value)
    );
    
    return uniqueEmotions.sort((a, b) => a.display.localeCompare(b.display));
  };

  const filteredEntries = getFilteredEntries();

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold">
          {getTranslation('journal.feelingJournal', language)}
        </h2>
        <p className="text-muted-foreground">
          {language === 'en' ? 'Select a feeling and write about it in your language' :
           language === 'es' ? 'Selecciona un sentimiento y escribe sobre él en tu idioma' :
           language === 'te' ? 'ఒక భావనను ఎంచుకుని దాని గురించి మీ భాషలో వ్రాయండి' :
           'ஒரு உணர்வைத் தேர்ந்தெடுத்து உங்கள் மொழியில் அதைப் பற்றி எழுதுங்கள்'}
        </p>
      </div>

      {/* Add new entry form */}
      <div className="bg-card p-6 rounded-lg border space-y-4">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Plus size={20} />
          {getTranslation('journal.addEntry', language)}
        </h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              {language === 'en' ? 'Select Feeling' :
               language === 'es' ? 'Seleccionar Sentimiento' :
               language === 'te' ? 'భావనను ఎంచుకోండి' :
               'உணர்வைத் தேர்ந்தெடுக்கவும்'}
            </label>
            <Select value={selectedFeeling} onValueChange={setSelectedFeeling}>
              <SelectTrigger>
                <SelectValue placeholder={
                  language === 'en' ? 'Choose a feeling...' :
                  language === 'es' ? 'Elige un sentimiento...' :
                  language === 'te' ? 'ఒక భావనను ఎంచుకోండి...' :
                  'ஒரு உணர்வைத் தேர்ந்தெடுக்கவும்...'
                } />
              </SelectTrigger>
              <SelectContent>
                {getAllEmotionsWithTranslations().map((emotion) => (
                  <SelectItem key={emotion.value} value={emotion.value}>
                    {emotion.display}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              {language === 'en' ? 'Your Thoughts' :
               language === 'es' ? 'Tus Pensamientos' :
               language === 'te' ? 'మీ ఆలోచనలు' :
               'உங்கள் எண்ணங்கள்'}
            </label>
            <Textarea
              value={newComment}
              onChange={handleTextChange}
              placeholder={getPlaceholderText()}
              className="min-h-[100px] resize-none"
              maxLength={500}
            />
            <p className="text-xs text-muted-foreground mt-1">
              {newComment.length}/500 characters
            </p>
          </div>

          <Button 
            onClick={handleAddEntry}
            disabled={!newComment.trim() || !selectedFeeling}
            className="w-full"
          >
            {getTranslation('journal.addEntry', language)}
          </Button>
        </div>
      </div>

      {/* View entries section */}
      <div className="bg-card p-6 rounded-lg border space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <BookOpen size={20} />
            {getTranslation('journal.previousEntries', language)} ({filteredEntries.length})
          </h3>
          <Button 
            variant="outline" 
            onClick={() => setShowEntries(!showEntries)}
            size="sm"
          >
            {showEntries ? 
              (language === 'en' ? 'Hide' :
               language === 'es' ? 'Ocultar' :
               language === 'te' ? 'దాచు' :
               'மறை') :
              (language === 'en' ? 'Show' :
               language === 'es' ? 'Mostrar' :
               language === 'te' ? 'చూపించు' :
               'காட்டு')
            }
          </Button>
        </div>
        
        {showEntries && (
          <div className="space-y-3 max-h-[400px] overflow-y-auto">
            {filteredEntries.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">
                {getTranslation('journal.noEntries', language)}
              </p>
            ) : (
              filteredEntries.map((entry) => (
                <div key={entry.id} className="bg-muted p-4 rounded-lg space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-sm text-primary">{entry.feeling}</span>
                    <span className="text-xs text-muted-foreground">{entry.timestamp}</span>
                  </div>
                  <p className="text-sm">{entry.comment}</p>
                  <div className="text-xs text-muted-foreground">
                    - {entry.username}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default StandaloneFeelingsJournal;
