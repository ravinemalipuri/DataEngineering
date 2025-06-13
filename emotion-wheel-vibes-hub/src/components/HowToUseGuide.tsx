
import React from 'react';
import { Language, getTranslation } from '@/translations';
import { BookOpen, Users, Heart } from 'lucide-react';
import TranslationTooltip from './TranslationTooltip';

interface HowToUseGuideProps {
  language: Language;
}

const HowToUseGuide: React.FC<HowToUseGuideProps> = ({ language }) => {
  return (
    <div className="bg-card/50 backdrop-blur-sm border border-border rounded-xl p-8 mb-16">
      <div className="flex items-center justify-center mb-6">
        <BookOpen className="w-8 h-8 text-primary mr-3" />
        <TranslationTooltip translationKey="main.howToUse" currentLanguage={language}>
          <h3 className="text-2xl font-playfair font-semibold text-center">
            {getTranslation('main.howToUse', language)}
          </h3>
        </TranslationTooltip>
      </div>
      
      <div className="max-w-4xl mx-auto space-y-6">
        <TranslationTooltip translationKey="main.howToUseIntro" currentLanguage={language}>
          <p className="text-lg text-foreground leading-relaxed">
            {getTranslation('main.howToUseIntro', language)}
          </p>
        </TranslationTooltip>
        
        <TranslationTooltip translationKey="main.howToUseSteps" currentLanguage={language}>
          <p className="text-base text-foreground leading-relaxed">
            {getTranslation('main.howToUseSteps', language)}
          </p>
        </TranslationTooltip>
        
        <TranslationTooltip translationKey="main.howToUseConversation" currentLanguage={language}>
          <p className="text-base text-foreground leading-relaxed">
            {getTranslation('main.howToUseConversation', language)}
          </p>
        </TranslationTooltip>
        
        <TranslationTooltip translationKey="main.howToUsePurpose" currentLanguage={language}>
          <p className="text-base text-primary font-medium leading-relaxed">
            {getTranslation('main.howToUsePurpose', language)}
          </p>
        </TranslationTooltip>
        
        {/* Examples Section */}
        <div className="pt-6">
          <div className="flex items-center mb-6">
            <Users className="w-6 h-6 text-secondary mr-2" />
            <TranslationTooltip translationKey="main.examples" currentLanguage={language}>
              <h4 className="text-xl font-playfair font-semibold">
                {getTranslation('main.examples', language)}
              </h4>
            </TranslationTooltip>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Example 1 - Fixed readability */}
            <div className="bg-accent/20 border border-accent/30 rounded-lg p-6">
              <TranslationTooltip translationKey="main.example1Title" currentLanguage={language}>
                <h5 className="font-semibold text-lg mb-3 text-primary">
                  {getTranslation('main.example1Title', language)}
                </h5>
              </TranslationTooltip>
              <TranslationTooltip translationKey="main.example1Text" currentLanguage={language}>
                <p className="text-sm text-foreground mb-4 leading-relaxed">
                  {getTranslation('main.example1Text', language)}
                </p>
              </TranslationTooltip>
              <TranslationTooltip translationKey="main.example1Using" currentLanguage={language}>
                <p className="text-sm text-foreground mb-2 font-medium">
                  {getTranslation('main.example1Using', language)}
                </p>
              </TranslationTooltip>
              <TranslationTooltip translationKey="main.example1Question" currentLanguage={language}>
                <blockquote className="text-sm italic text-secondary border-l-4 border-secondary pl-3 font-medium">
                  {getTranslation('main.example1Question', language)}
                </blockquote>
              </TranslationTooltip>
            </div>
            
            {/* Example 2 - Fixed readability */}
            <div className="bg-accent/20 border border-accent/30 rounded-lg p-6">
              <TranslationTooltip translationKey="main.example2Title" currentLanguage={language}>
                <h5 className="font-semibold text-lg mb-3 text-primary">
                  {getTranslation('main.example2Title', language)}
                </h5>
              </TranslationTooltip>
              <TranslationTooltip translationKey="main.example2Text" currentLanguage={language}>
                <p className="text-sm text-foreground mb-4 leading-relaxed">
                  {getTranslation('main.example2Text', language)}
                </p>
              </TranslationTooltip>
              <TranslationTooltip translationKey="main.example2Try" currentLanguage={language}>
                <p className="text-sm text-foreground mb-2 font-medium">
                  {getTranslation('main.example2Try', language)}
                </p>
              </TranslationTooltip>
              <TranslationTooltip translationKey="main.example2Response" currentLanguage={language}>
                <blockquote className="text-sm italic text-secondary border-l-4 border-secondary pl-3 font-medium">
                  {getTranslation('main.example2Response', language)}
                </blockquote>
              </TranslationTooltip>
            </div>
          </div>
          
          <div className="mt-6 flex items-center justify-center">
            <Heart className="w-5 h-5 text-red-500 mr-2" />
            <TranslationTooltip translationKey="main.exampleConclusion" currentLanguage={language}>
              <p className="text-sm text-center text-foreground font-medium">
                {getTranslation('main.exampleConclusion', language)}
              </p>
            </TranslationTooltip>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HowToUseGuide;
