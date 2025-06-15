
import { englishTranslations } from './english';
import { spanishTranslations } from './spanish';

export type Language = 'en' | 'te' | 'es' | 'ta';

export const translations = {
  en: englishTranslations,
  es: spanishTranslations,
  te: englishTranslations, // Fallback to English for now
  ta: englishTranslations, // Fallback to English for now
};

export const getTranslation = (key: string, language: Language = 'en'): string => {
  const keys = key.split('.');
  let value: any = translations[language] || translations.en;
  
  for (const k of keys) {
    value = value?.[k];
    if (!value) break;
  }
  
  return value || key;
};
