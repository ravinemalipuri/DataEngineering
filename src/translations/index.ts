
import { englishTranslations } from './english';
import { teluguTranslations } from './telugu';
import { spanishTranslations } from './spanish';
import { tamilTranslations } from './tamil';

export type Language = 'en' | 'te' | 'es' | 'ta';

export type TranslationKeys = {
  nav: {
    home: string;
    about: string;
    features: string;
    contact: string;
    emotionWheel: string;
  };
  main: {
    emotions: string;
    interactiveEmotionWheel: string;
    exploreSpectrum: string;
    understandingWheel: string;
    primaryEmotions: string;
    coreEmotionsInner: string;
    secondaryEmotions: string;
    emotionCategoriesMiddle: string;
    detailedEmotions: string;
    specificFeelingsOuter: string;
    viewFullscreen: string;
    fullscreenView: string;
    enhancedFullscreen: string;
    clickExplore: string;
    howToUse: string;
    howToUseIntro: string;
    howToUseSteps: string;
    howToUseConversation: string;
    howToUsePurpose: string;
    examples: string;
    example1Title: string;
    example1Text: string;
    example1Question: string;
    example1Using: string;
    example2Title: string;
    example2Text: string;
    example2Response: string;
    example2Try: string;
    exampleConclusion: string;
  };
  emotions: Record<string, string>;
};

export const translations: Record<Language, TranslationKeys> = {
  en: englishTranslations,
  te: teluguTranslations,
  es: spanishTranslations,
  ta: tamilTranslations
};

export const languageNames = {
  en: "English",
  te: "తెలుగు", // Telugu
  es: "Español", // Spanish
  ta: "தமிழ்"    // Tamil
};

export const getTranslation = (key: string, language: Language): string => {
  const keys = key.split('.');
  let result: any = translations[language];
  
  for (const k of keys) {
    if (result && result[k]) {
      result = result[k];
    } else {
      return key; // Fallback to key name if translation not found
    }
  }
  
  return typeof result === 'string' ? result : key;
};

// Helper for emotion wheel to get emotion names by type
export const getEmotionName = (emotion: any, language: Language): string => {
  if (!emotion) return '';
  
  // Try to get from translations first
  if (emotion.id) {
    const translatedName = translations[language].emotions[emotion.id];
    if (translatedName) return translatedName;
  }
  
  // Fallback to direct translation fields for backward compatibility
  if (language === 'en' && emotion.name) {
    return emotion.name;
  } else if (language === 'te' && emotion.nameTelugu) {
    return emotion.nameTelugu;
  } else if (language === 'es' && emotion.nameSpanish) {
    return emotion.nameSpanish || emotion.name || '???';
  } else if (language === 'ta' && emotion.nameTamil) {
    return emotion.nameTamil || emotion.name || '???';
  }
  
  return emotion.name || '???';
};
