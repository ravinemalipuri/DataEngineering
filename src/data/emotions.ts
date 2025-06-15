
export interface Emotion {
  id: string;
  name: string;
  color: string;
  intensity: 'primary' | 'secondary' | 'tertiary';
  category: string;
  description?: string;
}

export interface EmotionLevel1 extends Emotion {
  intensity: 'primary';
}

export interface EmotionLevel2 extends Emotion {
  intensity: 'secondary';
}

export interface EmotionLevel3 extends Emotion {
  intensity: 'tertiary';
}

export const emotionsData: Emotion[] = [
  // Primary emotions (inner circle)
  { id: 'joy', name: 'Joy', color: '#FFD700', intensity: 'primary', category: 'positive' },
  { id: 'trust', name: 'Trust', color: '#87CEEB', intensity: 'primary', category: 'positive' },
  { id: 'fear', name: 'Fear', color: '#9370DB', intensity: 'primary', category: 'negative' },
  { id: 'surprise', name: 'Surprise', color: '#FF6347', intensity: 'primary', category: 'neutral' },
  { id: 'sadness', name: 'Sadness', color: '#4682B4', intensity: 'primary', category: 'negative' },
  { id: 'disgust', name: 'Disgust', color: '#9ACD32', intensity: 'primary', category: 'negative' },
  { id: 'anger', name: 'Anger', color: '#DC143C', intensity: 'primary', category: 'negative' },
  { id: 'anticipation', name: 'Anticipation', color: '#FF8C00', intensity: 'primary', category: 'positive' },
];

export const getEmotionsData = () => emotionsData;

export const getAllLevel2Emotions = (): EmotionLevel2[] => {
  return emotionsData.filter(emotion => emotion.intensity === 'secondary') as EmotionLevel2[];
};

export const getAllLevel3Emotions = (): EmotionLevel3[] => {
  return emotionsData.filter(emotion => emotion.intensity === 'tertiary') as EmotionLevel3[];
};

export const getEmotionName = (emotion: any, language: string): string => {
  if (!emotion) return '';
  return emotion.name || '???';
};
