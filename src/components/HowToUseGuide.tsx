
import React from 'react';
import { Language, getTranslation } from '@/translations';

interface HowToUseGuideProps {
  language: Language;
}

const HowToUseGuide: React.FC<HowToUseGuideProps> = ({ language }) => {
  return (
    <div className="bg-card rounded-xl p-6 mb-8 border border-border">
      <h3 className="text-xl font-playfair font-semibold mb-4 text-center">
        How to Use the Emotion Wheel
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <h4 className="font-semibold mb-2">1. Explore</h4>
          <p className="text-muted-foreground">Click on different emotion segments to learn about them</p>
        </div>
        <div>
          <h4 className="font-semibold mb-2">2. Identify</h4>
          <p className="text-muted-foreground">Find emotions that match how you're currently feeling</p>
        </div>
        <div>
          <h4 className="font-semibold mb-2">3. Understand</h4>
          <p className="text-muted-foreground">Read descriptions to better understand your emotions</p>
        </div>
        <div>
          <h4 className="font-semibold mb-2">4. Journal</h4>
          <p className="text-muted-foreground">Write about your feelings in the journal below</p>
        </div>
      </div>
    </div>
  );
};

export default HowToUseGuide;
