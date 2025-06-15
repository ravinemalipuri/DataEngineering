
import { englishTranslations } from './english';
import { spanishTranslations } from './spanish';

export type Language = 'en' | 'es' | 'te' | 'ta';

export const languageNames: Record<Language, string> = {
  en: 'English',
  es: 'Español',
  te: 'తెలుగు',
  ta: 'தமிழ்'
};

const translations = {
  en: englishTranslations,
  es: spanishTranslations,
  te: englishTranslations, // Fallback to English for now
  ta: englishTranslations  // Fallback to English for now
};

export const getTranslation = (key: string, language: Language = 'en'): string => {
  const keys = key.split('.');
  let result: any = translations[language] || translations.en;
  
  for (const k of keys) {
    if (result && typeof result === 'object' && k in result) {
      result = result[k];
    } else {
      // Fallback to English if key not found
      result = translations.en;
      for (const fallbackKey of keys) {
        if (result && typeof result === 'object' && fallbackKey in result) {
          result = result[fallbackKey];
        } else {
          return key; // Return the key itself if not found
        }
      }
      break;
    }
  }
  
  return typeof result === 'string' ? result : key;
};
