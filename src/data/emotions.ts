
export interface Emotion {
  id: string;
  primary: string;
  secondary: string[];
  tertiary: string[];
  color: string;
  angle: number;
}

export interface EmotionTranslations {
  [key: string]: {
    primary: string;
    secondary: string[];
    tertiary: string[];
  }
}

export const emotionsData: Emotion[] = [
  {
    id: 'joy',
    primary: 'Joy',
    secondary: ['Serenity', 'Ecstasy'],
    tertiary: ['Love', 'Optimism'],
    color: '#FFD700',
    angle: 0
  },
  {
    id: 'trust',
    primary: 'Trust',
    secondary: ['Acceptance', 'Admiration'],
    tertiary: ['Submission', 'Love'],
    color: '#87CEEB',
    angle: 45
  },
  {
    id: 'fear',
    primary: 'Fear',
    secondary: ['Apprehension', 'Terror'],
    tertiary: ['Awe', 'Submission'],
    color: '#9370DB',
    angle: 90
  },
  {
    id: 'surprise',
    primary: 'Surprise',
    secondary: ['Distraction', 'Amazement'],
    tertiary: ['Disapproval', 'Awe'],
    color: '#FF6347',
    angle: 135
  },
  {
    id: 'sadness',
    primary: 'Sadness',
    secondary: ['Pensiveness', 'Grief'],
    tertiary: ['Remorse', 'Disapproval'],
    color: '#4682B4',
    angle: 180
  },
  {
    id: 'disgust',
    primary: 'Disgust',
    secondary: ['Boredom', 'Loathing'],
    tertiary: ['Contempt', 'Remorse'],
    color: '#9ACD32',
    angle: 225
  },
  {
    id: 'anger',
    primary: 'Anger',
    secondary: ['Annoyance', 'Rage'],
    tertiary: ['Aggressiveness', 'Contempt'],
    color: '#DC143C',
    angle: 270
  },
  {
    id: 'anticipation',
    primary: 'Anticipation',
    secondary: ['Interest', 'Vigilance'],
    tertiary: ['Optimism', 'Aggressiveness'],
    color: '#FF8C00',
    angle: 315
  }
];

export const translations: { [lang: string]: EmotionTranslations } = {
  en: {
    joy: {
      primary: 'Joy',
      secondary: ['Serenity', 'Ecstasy'],
      tertiary: ['Love', 'Optimism']
    },
    trust: {
      primary: 'Trust',
      secondary: ['Acceptance', 'Admiration'],
      tertiary: ['Submission', 'Love']
    },
    fear: {
      primary: 'Fear',
      secondary: ['Apprehension', 'Terror'],
      tertiary: ['Awe', 'Submission']
    },
    surprise: {
      primary: 'Surprise',
      secondary: ['Distraction', 'Amazement'],
      tertiary: ['Disapproval', 'Awe']
    },
    sadness: {
      primary: 'Sadness',
      secondary: ['Pensiveness', 'Grief'],
      tertiary: ['Remorse', 'Disapproval']
    },
    disgust: {
      primary: 'Disgust',
      secondary: ['Boredom', 'Loathing'],
      tertiary: ['Contempt', 'Remorse']
    },
    anger: {
      primary: 'Anger',
      secondary: ['Annoyance', 'Rage'],
      tertiary: ['Aggressiveness', 'Contempt']
    },
    anticipation: {
      primary: 'Anticipation',
      secondary: ['Interest', 'Vigilance'],
      tertiary: ['Optimism', 'Aggressiveness']
    }
  },
  te: {
    joy: {
      primary: 'ఆనందం',
      secondary: ['ప్రశాంతత', 'పరవశం'],
      tertiary: ['ప్రేమ', 'ఆశావాదం']
    },
    trust: {
      primary: 'నమ్మకం',
      secondary: ['అంగీకారం', 'ప్రశంస'],
      tertiary: ['లొంగిపోవడం', 'ప్రేమ']
    },
    fear: {
      primary: 'భయం',
      secondary: ['ఆందోళన', 'భీతి'],
      tertiary: ['విస్మయం', 'లొంగిపోవడం']
    },
    surprise: {
      primary: 'ఆశ్చర్యం',
      secondary: ['దృష్టి మళ్లింపు', 'అద్భుతం'],
      tertiary: ['అసంతృప్తి', 'విస్మయం']
    },
    sadness: {
      primary: 'దుఃఖం',
      secondary: ['ఆలోచన', 'శోకం'],
      tertiary: ['పశ్చాత్తాపం', 'అసంతృప్తి']
    },
    disgust: {
      primary: 'అసహ్యం',
      secondary: ['విసుగు', 'అసహ్యం'],
      tertiary: ['తృణీకరణ', 'పశ్చాత్తాపం']
    },
    anger: {
      primary: 'కోపం',
      secondary: ['చిరాకు', 'కోపం'],
      tertiary: ['దూకుడు', 'తృణీకరణ']
    },
    anticipation: {
      primary: 'ఎదురుచూపు',
      secondary: ['ఆసక్తి', 'అప్రమత్తత'],
      tertiary: ['ఆశావాదం', 'దూకుడు']
    }
  }
};
