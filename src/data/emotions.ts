
export interface Emotion {
  id: string;
  name: string;
  color: string;
  intensity: 'primary' | 'secondary' | 'tertiary';
  category: string;
  description?: string;
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
