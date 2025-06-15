
import React from 'react';
import { Button } from '@/components/ui/button';
import { Language, languageNames } from '@/translations';

interface NavigationProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentLanguage, onLanguageChange }) => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="text-xl font-bold">Emotion Wheel</div>
        
        <div className="flex items-center space-x-4">
          <select 
            value={currentLanguage} 
            onChange={(e) => onLanguageChange(e.target.value as Language)}
            className="px-3 py-1 border rounded"
          >
            {Object.entries(languageNames).map(([code, name]) => (
              <option key={code} value={code}>{name}</option>
            ))}
          </select>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
