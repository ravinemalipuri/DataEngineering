
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Menu, X, Globe } from 'lucide-react';
import { Language, languageNames, getTranslation } from '@/translations';

interface NavigationProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentLanguage, onLanguageChange }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setIsMobileMenuOpen(false);
    }
  };

  const navItems = [
    { id: 'hero', label: 'nav.home' },
    { id: 'about', label: 'nav.about' },
    { id: 'features', label: 'nav.features' },
    { id: 'contact', label: 'nav.contact' }
  ];
  
  const availableLanguages: Language[] = ['en', 'te', 'es', 'ta'];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emotion-joy to-emotion-anger"></div>
            <span className="font-playfair font-bold text-xl text-foreground">
              {getTranslation('nav.emotionWheel', currentLanguage)}
            </span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => scrollToSection(item.id)}
                className="text-foreground hover:text-primary transition-colors duration-200 font-medium"
              >
                {getTranslation(item.label, currentLanguage)}
              </button>
            ))}
            
            {/* Language Selector */}
            <div className="flex items-center space-x-2">
              <Globe className="w-4 h-4 text-muted-foreground" />
              <Select value={currentLanguage} onValueChange={(value) => onLanguageChange(value as Language)}>
                <SelectTrigger className="w-24 h-8">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {availableLanguages.map(lang => (
                    <SelectItem key={lang} value={lang}>
                      {languageNames[lang]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center space-x-2">
            <Select value={currentLanguage} onValueChange={(value) => onLanguageChange(value as Language)}>
              <SelectTrigger className="w-20 h-8">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {availableLanguages.map(lang => (
                  <SelectItem key={lang} value={lang}>
                    {languageNames[lang]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="p-2"
            >
              {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-border">
            <div className="flex flex-col space-y-3">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => scrollToSection(item.id)}
                  className="text-left text-foreground hover:text-primary transition-colors duration-200 font-medium py-2"
                >
                  {getTranslation(item.label, currentLanguage)}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
