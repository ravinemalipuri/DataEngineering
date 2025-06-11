
import React from 'react';
import { Language, getTranslation } from '@/translations';
import { BookOpen, Users, Heart } from 'lucide-react';

interface HowToUseGuideProps {
  language: Language;
}

const HowToUseGuide: React.FC<HowToUseGuideProps> = ({ language }) => {
  return (
    <div className="bg-card/50 backdrop-blur-sm border border-border rounded-xl p-8 mb-16">
      <div className="flex items-center justify-center mb-6">
        <BookOpen className="w-8 h-8 text-primary mr-3" />
        <h3 className="text-2xl font-playfair font-semibold text-center">
          {getTranslation('main.howToUse', language)}
        </h3>
      </div>
      
      <div className="max-w-4xl mx-auto space-y-6">
        <p className="text-lg text-muted-foreground leading-relaxed">
          {getTranslation('main.howToUseIntro', language)}
        </p>
        
        <p className="text-base text-foreground leading-relaxed">
          {getTranslation('main.howToUseSteps', language)}
        </p>
        
        <p className="text-base text-foreground leading-relaxed">
          {getTranslation('main.howToUseConversation', language)}
        </p>
        
        <p className="text-base text-primary font-medium leading-relaxed">
          {getTranslation('main.howToUsePurpose', language)}
        </p>
        
        {/* Examples Section */}
        <div className="pt-6">
          <div className="flex items-center mb-6">
            <Users className="w-6 h-6 text-secondary mr-2" />
            <h4 className="text-xl font-playfair font-semibold">
              {getTranslation('main.examples', language)}
            </h4>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Example 1 */}
            <div className="bg-accent/10 rounded-lg p-6">
              <h5 className="font-semibold text-lg mb-3 text-primary">
                {getTranslation('main.example1Title', language)}
              </h5>
              <p className="text-sm text-foreground mb-4 leading-relaxed">
                {getTranslation('main.example1Text', language)}
              </p>
              <p className="text-sm text-muted-foreground mb-2">
                {getTranslation('main.example1Using', language)}
              </p>
              <blockquote className="text-sm italic text-secondary border-l-4 border-secondary pl-3">
                {getTranslation('main.example1Question', language)}
              </blockquote>
            </div>
            
            {/* Example 2 */}
            <div className="bg-accent/10 rounded-lg p-6">
              <h5 className="font-semibold text-lg mb-3 text-primary">
                {getTranslation('main.example2Title', language)}
              </h5>
              <p className="text-sm text-foreground mb-4 leading-relaxed">
                {getTranslation('main.example2Text', language)}
              </p>
              <p className="text-sm text-muted-foreground mb-2">
                {getTranslation('main.example2Try', language)}
              </p>
              <blockquote className="text-sm italic text-secondary border-l-4 border-secondary pl-3">
                {getTranslation('main.example2Response', language)}
              </blockquote>
            </div>
          </div>
          
          <div className="mt-6 flex items-center justify-center">
            <Heart className="w-5 h-5 text-red-500 mr-2" />
            <p className="text-sm text-center text-muted-foreground italic">
              {getTranslation('main.exampleConclusion', language)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HowToUseGuide;
