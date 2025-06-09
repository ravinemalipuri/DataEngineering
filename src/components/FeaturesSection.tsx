
import React from 'react';
import EmotionWheel from './EmotionWheel';

interface FeaturesSectionProps {
  language: string;
}

const FeaturesSection: React.FC<FeaturesSectionProps> = ({ language }) => {
  return (
    <section id="features" className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-playfair font-bold mb-6">
            {language === 'en' ? 'Interactive Emotion Wheel' : 'ఇంటరాక్టివ్ భావోద్వేగ చక్రం'}
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            {language === 'en'
              ? 'Explore the complete spectrum of human emotions. Click on any segment to discover related feelings and understand emotional connections.'
              : 'మానవ భావోద్వేగాల పూర్తి వర్ణపటాన్ని అన్వేషించండి. సంబంధిత భావాలను కనుగొనడానికి మరియు భావోద్వేగ కనెక్షన్లను అర్థం చేసుకోవడానికి ఏదైనా విభాగంపై క్లిక్ చేయండి.'
            }
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <EmotionWheel language={language} />
        </div>

        {/* Legend */}
        <div className="mt-16 bg-card rounded-xl p-8 border border-border">
          <h3 className="text-xl font-playfair font-semibold mb-6 text-center">
            {language === 'en' ? 'Understanding the Wheel' : 'చక్రాన్ని అర్థం చేసుకోవడం'}
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-emotion-joy to-emotion-anticipation mx-auto mb-3 opacity-100"></div>
              <h4 className="font-semibold mb-2">
                {language === 'en' ? 'Primary Emotions' : 'ప్రాథమిక భావోద్వేగాలు'}
              </h4>
              <p className="text-sm text-muted-foreground">
                {language === 'en' ? 'Core emotions - outer ring' : 'ప్రధాన భావోద్వేగాలు - బాహ్య వలయం'}
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-emotion-trust to-emotion-fear mx-auto mb-3 opacity-70"></div>
              <h4 className="font-semibold mb-2">
                {language === 'en' ? 'Secondary Emotions' : 'ద్వితీయ భావోద్వేగాలు'}
              </h4>
              <p className="text-sm text-muted-foreground">
                {language === 'en' ? 'Variations in intensity - middle ring' : 'తీవ్రతలో వైవిధ్యాలు - మధ్య వలయం'}
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-emotion-sadness to-emotion-disgust mx-auto mb-3 opacity-40"></div>
              <h4 className="font-semibold mb-2">
                {language === 'en' ? 'Related Emotions' : 'సంబంధిత భావోద్వేగాలు'}
              </h4>
              <p className="text-sm text-muted-foreground">
                {language === 'en' ? 'Connected feelings - inner ring' : 'అనుసంధానించబడిన భావాలు - అంతర్గత వలయం'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
