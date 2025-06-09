
import React from 'react';
import { Button } from '@/components/ui/button';
import { ArrowDown, Heart, Brain } from 'lucide-react';

interface HeroSectionProps {
  language: string;
}

const HeroSection: React.FC<HeroSectionProps> = ({ language }) => {
  const scrollToWheel = () => {
    const element = document.getElementById('features');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="hero" className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-accent/10 to-primary/10 pt-16">
      <div className="container mx-auto px-4 text-center">
        <div className="max-w-4xl mx-auto">
          {/* Hero Content */}
          <div className="mb-8 animate-fade-in">
            <div className="flex justify-center mb-6">
              <div className="relative">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-emotion-joy via-emotion-trust to-emotion-anticipation animate-pulse-glow"></div>
                <Heart className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-8 h-8 text-white" />
              </div>
            </div>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-playfair font-bold mb-6 text-foreground leading-tight">
              {language === 'en' ? (
                <>
                  Explore Your <br />
                  <span className="bg-gradient-to-r from-emotion-joy via-emotion-trust to-emotion-anticipation bg-clip-text text-transparent">
                    Emotional Universe
                  </span>
                </>
              ) : (
                <>
                  మీ <br />
                  <span className="bg-gradient-to-r from-emotion-joy via-emotion-trust to-emotion-anticipation bg-clip-text text-transparent">
                    భావోద్వేగ విశ్వాన్ని
                  </span>
                  <br />
                  అన్వేషించండి
                </>
              )}
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
              {language === 'en' 
                ? 'Discover the intricate world of human emotions through our interactive wheel. Understanding emotions is the first step toward emotional intelligence and well-being.'
                : 'మా ఇంటరాక్టివ్ చక్రం ద్వారా మానవ భావోద్వేగాల సంక్లిష్ట ప్రపంచాన్ని కనుగొనండి. భావోద్వేగాలను అర్థం చేసుకోవడం భావోద్వేగ మేధస్సు మరియు సంక్షేమానికి మొదటి అడుగు.'
              }
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button
                onClick={scrollToWheel}
                size="lg"
                className="bg-gradient-to-r from-emotion-joy to-emotion-anticipation hover:from-emotion-trust hover:to-emotion-joy transition-all duration-300 px-8 py-3 text-lg font-semibold"
              >
                {language === 'en' ? 'Explore Emotions' : 'భావోద్వేగాలను అన్వేషించండి'}
                <ArrowDown className="ml-2 w-5 h-5" />
              </Button>
              
              <div className="flex items-center space-x-2 text-muted-foreground">
                <Brain className="w-5 h-5" />
                <span className="text-sm">
                  {language === 'en' ? 'Science-based approach' : 'శాస్త్రీయ దృష్టికోణం'}
                </span>
              </div>
            </div>
          </div>
          
          {/* Features Preview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
            {[
              {
                icon: '🎯',
                title: language === 'en' ? 'Interactive' : 'ఇంటరాక్టివ్',
                desc: language === 'en' ? 'Click and explore' : 'క్లిక్ చేసి అన్వేషించండి'
              },
              {
                icon: '🌍',
                title: language === 'en' ? 'Multilingual' : 'బహుభాషా',
                desc: language === 'en' ? 'English & Telugu' : 'ఇంగ్లీష్ & తెలుగు'
              },
              {
                icon: '📱',
                title: language === 'en' ? 'Responsive' : 'రెస్పాన్సివ్',
                desc: language === 'en' ? 'Works everywhere' : 'ప్రతిచోటా పనిచేస్తుంది'
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="bg-card/50 backdrop-blur-sm border border-border rounded-lg p-6 hover:bg-card/70 transition-all duration-300 hover:scale-105"
              >
                <div className="text-3xl mb-3">{feature.icon}</div>
                <h3 className="font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
