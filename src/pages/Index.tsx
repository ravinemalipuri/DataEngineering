
import React, { useState } from 'react';
import Navigation from '@/components/Navigation';
import FeaturesSection from '@/components/FeaturesSection';

const Index = () => {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const handleLanguageChange = (lang: string) => {
    setCurrentLanguage(lang);
    document.documentElement.lang = lang;
  };

  return (
    <div className="min-h-screen bg-background font-inter">
      <Navigation 
        currentLanguage={currentLanguage} 
        onLanguageChange={handleLanguageChange} 
      />
      
      <main className="pt-16">
        <FeaturesSection language={currentLanguage} />
      </main>
    </div>
  );
};

export default Index;
