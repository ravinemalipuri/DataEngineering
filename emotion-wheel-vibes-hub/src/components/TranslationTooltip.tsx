
import React, { useState, useEffect } from 'react';
import { Language, getTranslation } from '@/translations';

interface TranslationTooltipProps {
  children: React.ReactNode;
  translationKey: string;
  currentLanguage: Language;
  className?: string;
}

const TranslationTooltip: React.FC<TranslationTooltipProps> = ({
  children,
  translationKey,
  currentLanguage,
  className = ""
}) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const [hoverTimer, setHoverTimer] = useState<NodeJS.Timeout | null>(null);

  const getTooltipText = () => {
    if (currentLanguage === 'en') {
      // Show Telugu translation
      return getTranslation(translationKey, 'te');
    } else {
      // Show English translation
      return getTranslation(translationKey, 'en');
    }
  };

  const handleMouseEnter = () => {
    const timer = setTimeout(() => {
      setShowTooltip(true);
    }, 2000);
    setHoverTimer(timer);
  };

  const handleMouseLeave = () => {
    if (hoverTimer) {
      clearTimeout(hoverTimer);
      setHoverTimer(null);
    }
    setShowTooltip(false);
  };

  useEffect(() => {
    return () => {
      if (hoverTimer) {
        clearTimeout(hoverTimer);
      }
    };
  }, [hoverTimer]);

  return (
    <div 
      className={`relative inline-block ${className}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {children}
      {showTooltip && (
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-800 text-white text-sm rounded-lg shadow-lg z-50 whitespace-nowrap animate-fade-in">
          {getTooltipText()}
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
        </div>
      )}
    </div>
  );
};

export default TranslationTooltip;
