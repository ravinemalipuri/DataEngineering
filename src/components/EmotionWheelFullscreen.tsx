
import React, { useState } from 'react';
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Maximize2, X } from "lucide-react";
import EmotionWheel from './EmotionWheel';

interface EmotionWheelFullscreenProps {
  language: string;
}

const EmotionWheelFullscreen: React.FC<EmotionWheelFullscreenProps> = ({ language }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button 
          variant="outline" 
          size="lg"
          className="mt-6 flex items-center gap-2 bg-card hover:bg-accent border-2 border-primary/20 hover:border-primary/40 transition-all duration-300"
        >
          <Maximize2 className="w-5 h-5" />
          {language === 'en' ? 'View Fullscreen' : 'పూర్తి స్క్రీన్‌లో చూడండి'}
        </Button>
      </DialogTrigger>
      
      <DialogContent className="max-w-6xl w-[95vw] h-[95vh] p-6 bg-background">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-playfair font-bold">
            {language === 'en' ? 'Interactive Emotion Wheel - Fullscreen View' : 'ఇంటరాక్టివ్ భావోద్వేగ చక్రం - పూర్తి స్క్రీన్ వీక్షణ'}
          </h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsOpen(false)}
            className="h-8 w-8"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
        
        <div className="flex-1 overflow-auto">
          <div className="h-full flex items-center justify-center">
            <div className="w-full max-w-4xl">
              <EmotionWheel language={language} />
            </div>
          </div>
        </div>
        
        <div className="mt-4 text-center">
          <p className="text-sm text-muted-foreground">
            {language === 'en' 
              ? 'Enhanced fullscreen view for better emotion exploration and understanding'
              : 'మెరుగైన భావోద్వేగ అన్వేషణ మరియు అవగాహన కోసం మెరుగైన పూర్తి స్క్రీన్ వీక్షణ'
            }
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default EmotionWheelFullscreen;
