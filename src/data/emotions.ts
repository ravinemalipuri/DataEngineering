
import { emotionsDataEnglish, EmotionLevel1 as EmotionLevel1English, EmotionLevel2 as EmotionLevel2English, EmotionLevel3 as EmotionLevel3English } from './emotions_english';
import { emotionsDataTelugu, EmotionLevel1Telugu, EmotionLevel2Telugu, EmotionLevel3Telugu } from './emotions_telugu';
import { emotionsDataSpanish, EmotionLevel1Spanish, EmotionLevel2Spanish, EmotionLevel3Spanish } from './emotions_spanish';
import { emotionsDataTamil, EmotionLevel1Tamil, EmotionLevel2Tamil, EmotionLevel3Tamil } from './emotions_tamil';
import { Language } from '@/translations';

// Union types for all emotion levels
export type EmotionLevel3 = EmotionLevel3English | EmotionLevel3Telugu | EmotionLevel3Spanish | EmotionLevel3Tamil;
export type EmotionLevel2 = EmotionLevel2English | EmotionLevel2Telugu | EmotionLevel2Spanish | EmotionLevel2Tamil;
export type EmotionLevel1 = EmotionLevel1English | EmotionLevel1Telugu | EmotionLevel1Spanish | EmotionLevel1Tamil;

// Function to get emotions data based on language
export const getEmotionsData = (language: Language): EmotionLevel1[] => {
  switch (language) {
    case 'en':
      return emotionsDataEnglish as EmotionLevel1[];
    case 'te':
      return emotionsDataTelugu as EmotionLevel1[];
    case 'es':
      return emotionsDataSpanish as EmotionLevel1[];
    case 'ta':
      return emotionsDataTamil as EmotionLevel1[];
    default:
      return emotionsDataEnglish as EmotionLevel1[];
  }
};

// Default export for backward compatibility
export const emotionsData = emotionsDataEnglish as EmotionLevel1[];

// Helper function to get emotion name based on language
export const getEmotionName = (emotion: any, language: Language): string => {
  if (!emotion) return '';
  
  switch (language) {
    case 'en':
      return emotion.nameEnglish || emotion.name || '???';
    case 'te':
      return emotion.nameTelugu || emotion.name || '???';
    case 'es':
      return emotion.nameSpanish || emotion.name || '???';
    case 'ta':
      return emotion.nameTamil || emotion.name || '???';
    default:
      return emotion.nameEnglish || emotion.name || '???';
  }
};

export const getAllLevel3Emotions = (primaryEmotion: EmotionLevel1): EmotionLevel3[] => {
  return primaryEmotion.level2Emotions.flatMap(level2 => level2.level3Emotions);
};

export const getAllLevel2Emotions = (primaryEmotion: EmotionLevel1): EmotionLevel2[] => {
  return primaryEmotion.level2Emotions;
};
