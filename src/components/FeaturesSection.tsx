import React from 'react';
import EmotionWheel from './EmotionWheel';
import EmotionWheelFullscreen from './EmotionWheelFullscreen';
import HowToUseGuide from './HowToUseGuide';
import MediaBar from './MediaBar';
import FeelingsJournal from "./FeelingsJournal";
import { Language, getTranslation } from '@/translations';

interface FeaturesSectionProps {
  language: string;
}

const FeaturesSection: React.FC<FeaturesSectionProps> = ({ language }) => {
  return (
    <section id="features" className="py-12 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h2 className="text-3xl md:text-4xl font-playfair font-bold mb-6">
            {getTranslation('main.interactiveEmotionWheel', language as Language)}
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            {getTranslation('main.exploreSpectrum', language as Language)}
          </p>
        </div>

        <div className="max-w-6xl mx-auto mb-8">
          <EmotionWheel language={language} />
          
          {/* Fullscreen Button */}
          <div className="flex justify-center">
            <EmotionWheelFullscreen language={language} />
          </div>
        </div>

        {/* How to Use Guide */}
        <HowToUseGuide language={language as Language} />

        {/* Understanding the Wheel */}
        <div className="bg-card rounded-xl p-8 border border-border">
          <h3 className="text-xl font-playfair font-semibold mb-6 text-center">
            {getTranslation('main.understandingWheel', language as Language)}
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#FFD700] to-[#DC143C] mx-auto mb-3 opacity-100"></div>
              <h4 className="font-semibold mb-2">
                {getTranslation('main.primaryEmotions', language as Language)}
              </h4>
              <p className="text-sm text-muted-foreground">
                {getTranslation('main.coreEmotionsInner', language as Language)}
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#4682B4] to-[#9370DB] mx-auto mb-3 opacity-70"></div>
              <h4 className="font-semibold mb-2">
                {getTranslation('main.secondaryEmotions', language as Language)}
              </h4>
              <p className="text-sm text-muted-foreground">
                {getTranslation('main.emotionCategoriesMiddle', language as Language)}
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#9ACD32] to-[#FF6347] mx-auto mb-3 opacity-40"></div>
              <h4 className="font-semibold mb-2">
                {getTranslation('main.detailedEmotions', language as Language)}
              </h4>
              <p className="text-sm text-muted-foreground">
                {getTranslation('main.specificFeelingsOuter', language as Language)}
              </p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Media Bar at the bottom */}
      <MediaBar />

      {/* Feelings Journal */}
      <FeelingsJournal />
    </section>
  );
};

export default FeaturesSection;
