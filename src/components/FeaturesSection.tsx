
import React from 'react';
import EmotionWheel from './EmotionWheel';
import EmotionWheelFullscreen from './EmotionWheelFullscreen';
import HowToUseGuide from './HowToUseGuide';
import MediaBar from './MediaBar';
import { Language, getTranslation } from '@/translations';

interface FeaturesSectionProps {
  language: Language;
}

const FeaturesSection: React.FC<FeaturesSectionProps> = ({ language }) => {
  return (
    <section id="features" className="min-h-screen py-16 px-4">
      <div className="container mx-auto max-w-6xl">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-playfair font-bold mb-6 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            {getTranslation('main.interactiveEmotionWheel', language)}
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            {getTranslation('main.exploreSpectrum', language)}
          </p>
        </div>

        {/* How to Use Guide */}
        <HowToUseGuide language={language} />

        {/* Main Emotion Wheel */}
        <div className="bg-card/50 backdrop-blur-sm border border-border rounded-2xl p-8 mb-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-playfair font-bold mb-4">
              {getTranslation('main.interactiveEmotionWheel', language)}
            </h2>
            <p className="text-muted-foreground">
              Click on different emotions to explore them
            </p>
          </div>
          
          <div className="flex justify-center">
            <EmotionWheel language={language} />
          </div>
          
          <div className="flex justify-center mt-6">
            <EmotionWheelFullscreen language={language} />
          </div>
        </div>

        {/* Understanding the Wheel */}
        <div className="bg-card/30 border border-border rounded-xl p-8 mb-8">
          <h3 className="text-2xl font-playfair font-semibold mb-6 text-center">
            {getTranslation('main.understandingWheel', language)}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <div className="w-8 h-8 bg-primary rounded-full"></div>
              </div>
              <h4 className="font-semibold mb-2">{getTranslation('main.primaryEmotions', language)}</h4>
              <p className="text-sm text-muted-foreground">{getTranslation('main.coreEmotionsInner', language)}</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-secondary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <div className="w-8 h-8 bg-secondary rounded-full"></div>
              </div>
              <h4 className="font-semibold mb-2">{getTranslation('main.secondaryEmotions', language)}</h4>
              <p className="text-sm text-muted-foreground">{getTranslation('main.emotionCategoriesMiddle', language)}</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <div className="w-8 h-8 bg-accent rounded-full"></div>
              </div>
              <h4 className="font-semibold mb-2">{getTranslation('main.detailedEmotions', language)}</h4>
              <p className="text-sm text-muted-foreground">{getTranslation('main.specificFeelingsOuter', language)}</p>
            </div>
          </div>
        </div>

        {/* Media Bar */}
        <MediaBar />
      </div>
    </section>
  );
};

export default FeaturesSection;
