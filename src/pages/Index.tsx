
import React, { useState, useEffect } from 'react';
import Navigation from '@/components/Navigation';
import FeaturesSection from '@/components/FeaturesSection';
import StandaloneFeelingsJournal from '@/components/StandaloneFeelingsJournal';
import { Language } from '@/translations';

const Index = () => {
  const [currentLanguage, setCurrentLanguage] = useState<Language>('en');

  useEffect(() => {
    // Get browser language or use saved preference if available
    const savedLanguage = localStorage.getItem('preferred-language');
    if (savedLanguage && ['en', 'te', 'es', 'ta'].includes(savedLanguage)) {
      setCurrentLanguage(savedLanguage as Language);
    } else {
      // Try to detect browser language
      const browserLang = navigator.language.split('-')[0];
      if (['en', 'te', 'es', 'ta'].includes(browserLang)) {
        setCurrentLanguage(browserLang as Language);
      }
    }
    
    document.documentElement.lang = currentLanguage;
  }, []);

  const handleLanguageChange = (lang: Language) => {
    setCurrentLanguage(lang);
    document.documentElement.lang = lang;
    // Save preference
    localStorage.setItem('preferred-language', lang);
  };

  return (
    <div className="min-h-screen bg-background font-inter">
      <Navigation 
        currentLanguage={currentLanguage} 
        onLanguageChange={handleLanguageChange} 
      />
      
      <main className="pt-16">
        <FeaturesSection language={currentLanguage} />
        
        {/* Standalone Feelings Journal Section */}
        <section className="py-16 bg-muted/50">
          <div className="container mx-auto px-4">
            <StandaloneFeelingsJournal language={currentLanguage} />
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;
