
import React, { useState } from 'react';
import Navigation from '@/components/Navigation';
import HeroSection from '@/components/HeroSection';
import AboutSection from '@/components/AboutSection';
import FeaturesSection from '@/components/FeaturesSection';
import ContactSection from '@/components/ContactSection';

const Index = () => {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const handleLanguageChange = (lang: string) => {
    setCurrentLanguage(lang);
    // Update document language for accessibility
    document.documentElement.lang = lang;
  };

  return (
    <div className="min-h-screen bg-background font-inter">
      <Navigation 
        currentLanguage={currentLanguage} 
        onLanguageChange={handleLanguageChange} 
      />
      
      <main>
        <HeroSection language={currentLanguage} />
        <AboutSection language={currentLanguage} />
        <FeaturesSection language={currentLanguage} />
        <ContactSection language={currentLanguage} />
      </main>

      <footer className="bg-card border-t border-border py-8">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center mb-4">
            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-emotion-joy to-emotion-anger mr-2"></div>
            <span className="font-playfair font-semibold">
              {currentLanguage === 'en' ? 'Emotion Wheel' : 'భావోద్వేగ చక్రం'}
            </span>
          </div>
          <p className="text-sm text-muted-foreground">
            {currentLanguage === 'en' 
              ? '© 2024 Emotion Wheel. Built with modern web technologies and love for emotional well-being.'
              : '© 2024 భావోద్వేగ చక్రం. ఆధునిక వెబ్ టెక్నాలజీలు మరియు భావోద్వేగ సంక్షేమం కోసం ప్రేమతో నిర్మించబడింది.'
            }
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
