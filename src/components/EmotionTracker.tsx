import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/integrations/supabase/client';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { useToast } from '@/hooks/use-toast';
import { Heart, Save, RotateCcw } from 'lucide-react';

interface Emotion {
  id: string;
  name: string;
  category: string;
  color_hex: string;
}

interface EmotionEntry {
  id: string;
  emotion_ids: string[];
  intensity: number;
  note: string;
  recorded_at: string;
  emotions?: Emotion[];
}

const EmotionTracker = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  
  const [emotions, setEmotions] = useState<Emotion[]>([]);
  const [selectedEmotions, setSelectedEmotions] = useState<string[]>([]);
  const [intensity, setIntensity] = useState([5]);
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [recentEntries, setRecentEntries] = useState<EmotionEntry[]>([]);

  useEffect(() => {
    if (user) {
      fetchEmotions();
      fetchRecentEntries();
    }
  }, [user]);

  const fetchEmotions = async () => {
    const { data, error } = await supabase
      .from('emotions')
      .select('*')
      .order('category', { ascending: true });

    if (error) {
      toast({
        title: "Error",
        description: "Failed to load emotions",
        variant: "destructive"
      });
    } else {
      setEmotions(data || []);
    }
  };

  const fetchRecentEntries = async () => {
    if (!user) return;

    const { data, error } = await supabase
      .from('emotion_entries')
      .select(`
        *,
        emotions:emotion_ids (*)
      `)
      .eq('user_id', user.id)
      .order('recorded_at', { ascending: false })
      .limit(5);

    if (error) {
      console.error('Error fetching recent entries:', error);
    } else {
      // Transform the data to include emotion details
      const entriesWithEmotions = await Promise.all(
        (data || []).map(async (entry) => {
          const { data: emotionData } = await supabase
            .from('emotions')
            .select('*')
            .in('id', entry.emotion_ids);
          
          return {
            ...entry,
            emotions: emotionData || []
          };
        })
      );
      setRecentEntries(entriesWithEmotions);
    }
  };

  const handleEmotionToggle = (emotionId: string) => {
    setSelectedEmotions(prev => 
      prev.includes(emotionId)
        ? prev.filter(id => id !== emotionId)
        : [...prev, emotionId]
    );
  };

  const handleSave = async () => {
    if (!user || selectedEmotions.length === 0) {
      toast({
        title: "Selection Required",
        description: "Please select at least one emotion",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    
    const { error } = await supabase
      .from('emotion_entries')
      .insert({
        user_id: user.id,
        emotion_ids: selectedEmotions,
        intensity: intensity[0],
        note: note.trim() || null,
        recorded_at: new Date().toISOString()
      });

    setLoading(false);

    if (error) {
      toast({
        title: "Error",
        description: "Failed to save emotion entry",
        variant: "destructive"
      });
    } else {
      toast({
        title: "Saved!",
        description: "Your emotions have been recorded"
      });
      
      // Reset form
      setSelectedEmotions([]);
      setIntensity([5]);
      setNote('');
      
      // Refresh recent entries
      fetchRecentEntries();
    }
  };

  const handleReset = () => {
    setSelectedEmotions([]);
    setIntensity([5]);
    setNote('');
  };

  const getEmotionsByCategory = () => {
    return emotions.reduce((acc, emotion) => {
      if (!acc[emotion.category]) {
        acc[emotion.category] = [];
      }
      acc[emotion.category].push(emotion);
      return acc;
    }, {} as Record<string, Emotion[]>);
  };

  if (!user) {
    return (
      <Card>
        <CardContent className="p-6">
          <p className="text-center text-muted-foreground">
            Please sign in to track your emotions
          </p>
        </CardContent>
      </Card>
    );
  }

  const emotionsByCategory = getEmotionsByCategory();

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Heart className="h-5 w-5 text-primary" />
            How are you feeling right now?
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Emotion Selection */}
          <div className="space-y-4">
            {Object.entries(emotionsByCategory).map(([category, categoryEmotions]) => (
              <div key={category} className="space-y-2">
                <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
                  {category}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {categoryEmotions.map((emotion) => (
                    <Badge
                      key={emotion.id}
                      variant={selectedEmotions.includes(emotion.id) ? "default" : "outline"}
                      className="cursor-pointer hover:scale-105 transition-transform"
                      style={{
                        backgroundColor: selectedEmotions.includes(emotion.id) 
                          ? emotion.color_hex 
                          : 'transparent',
                        borderColor: emotion.color_hex,
                        color: selectedEmotions.includes(emotion.id) ? 'white' : emotion.color_hex
                      }}
                      onClick={() => handleEmotionToggle(emotion.id)}
                    >
                      {emotion.name}
                    </Badge>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Intensity Slider */}
          <div className="space-y-2">
            <label className="text-sm font-medium">
              Intensity: {intensity[0]}/10
            </label>
            <Slider
              value={intensity}
              onValueChange={setIntensity}
              max={10}
              min={1}
              step={1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Low</span>
              <span>High</span>
            </div>
          </div>

          {/* Note */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Notes (optional)</label>
            <Textarea
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="What's on your mind? Any context about these emotions..."
              rows={3}
            />
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            <Button onClick={handleSave} disabled={loading || selectedEmotions.length === 0}>
              <Save className="mr-2 h-4 w-4" />
              Save Entry
            </Button>
            <Button variant="outline" onClick={handleReset}>
              <RotateCcw className="mr-2 h-4 w-4" />
              Reset
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Recent Entries */}
      {recentEntries.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recent Entries</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentEntries.map((entry) => (
                <div key={entry.id} className="border-l-4 border-primary/20 pl-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex flex-wrap gap-1">
                      {entry.emotions?.map((emotion) => (
                        <Badge
                          key={emotion.id}
                          variant="outline"
                          style={{ borderColor: emotion.color_hex, color: emotion.color_hex }}
                        >
                          {emotion.name}
                        </Badge>
                      ))}
                    </div>
                    <span className="text-xs text-muted-foreground">
                      Intensity: {entry.intensity}/10
                    </span>
                  </div>
                  {entry.note && (
                    <p className="text-sm text-muted-foreground italic">"{entry.note}"</p>
                  )}
                  <p className="text-xs text-muted-foreground">
                    {new Date(entry.recorded_at).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default EmotionTracker;