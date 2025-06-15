
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Maximize } from 'lucide-react';
import EmotionWheel from './EmotionWheel';
import { getTranslation, Language } from '@/translations';

interface EmotionWheelFullscreenProps {
  language: string;
}

const EmotionWheelFullscreen: React.FC<EmotionWheelFullscreenProps> = ({ language }) => {
  const [isFullscreen, setIsFullscreen] = useState(false);

  return (
    <>
      <Button 
        onClick={() => setIsFullscreen(true)}
        variant="outline"
        className="mt-4"
      >
        <Maximize className="w-4 h-4 mr-2" />
        {getTranslation('main.viewFullscreen', language as Language)}
      </Button>

      {isFullscreen && (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-8 rounded-lg max-w-4xl max-h-screen overflow-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">
                {getTranslation('main.fullscreenView', language as Language)}
              </h2>
              <Button onClick={() => setIsFullscreen(false)}>Close</Button>
            </div>
            <EmotionWheel language={language} />
          </div>
        </div>
      )}
    </>
  );
};

export default EmotionWheelFullscreen;
