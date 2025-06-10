
export interface EmotionLevel3 {
  id: string;
  name: string;
  nameTeluguPlaceholder: string; // Using ??? as placeholder for Telugu translations
}

export interface EmotionLevel2 {
  id: string;
  name: string;
  nameTeluguPlaceholder: string;
  level3Emotions: EmotionLevel3[];
}

export interface EmotionLevel1 {
  id: string;
  name: string;
  nameTeluguPlaceholder: string;
  color: string;
  angle: number;
  level2Emotions: EmotionLevel2[];
}

export const emotionsData: EmotionLevel1[] = [
  {
    id: 'happy',
    name: 'Happy',
    nameTeluguPlaceholder: '???',
    color: '#FFD700',
    angle: 0,
    level2Emotions: [
      {
        id: 'playful',
        name: 'Playful',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'aroused', name: 'Aroused', nameTeluguPlaceholder: '???' },
          { id: 'cheeky', name: 'Cheeky', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'content',
        name: 'Content',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'free', name: 'Free', nameTeluguPlaceholder: '???' },
          { id: 'joyful', name: 'Joyful', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'interested',
        name: 'Interested',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'curious', name: 'Curious', nameTeluguPlaceholder: '???' },
          { id: 'inquisitive', name: 'Inquisitive', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'proud',
        name: 'Proud',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'successful', name: 'Successful', nameTeluguPlaceholder: '???' },
          { id: 'confident', name: 'Confident', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'accepted',
        name: 'Accepted',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'respected', name: 'Respected', nameTeluguPlaceholder: '???' },
          { id: 'valued', name: 'Valued', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'powerful',
        name: 'Powerful',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'courageous', name: 'Courageous', nameTeluguPlaceholder: '???' },
          { id: 'creative', name: 'Creative', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'peaceful',
        name: 'Peaceful',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'loving', name: 'Loving', nameTeluguPlaceholder: '???' },
          { id: 'thankful', name: 'Thankful', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'trusting',
        name: 'Trusting',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'sensitive', name: 'Sensitive', nameTeluguPlaceholder: '???' },
          { id: 'intimate', name: 'Intimate', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'optimistic',
        name: 'Optimistic',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'hopeful', name: 'Hopeful', nameTeluguPlaceholder: '???' },
          { id: 'inspired', name: 'Inspired', nameTeluguPlaceholder: '???' }
        ]
      }
    ]
  },
  {
    id: 'sad',
    name: 'Sad',
    nameTeluguPlaceholder: '???',
    color: '#4682B4',
    angle: 51.4,
    level2Emotions: [
      {
        id: 'lonely',
        name: 'Lonely',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'isolated', name: 'Isolated', nameTeluguPlaceholder: '???' },
          { id: 'abandoned', name: 'Abandoned', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'vulnerable',
        name: 'Vulnerable',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'victimised', name: 'Victimised', nameTeluguPlaceholder: '???' },
          { id: 'fragile', name: 'Fragile', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'despair',
        name: 'Despair',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'grief', name: 'Grief', nameTeluguPlaceholder: '???' },
          { id: 'powerless', name: 'Powerless', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'guilty',
        name: 'Guilty',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'ashamed', name: 'Ashamed', nameTeluguPlaceholder: '???' },
          { id: 'remorseful', name: 'Remorseful', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'depressed',
        name: 'Depressed',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'inferior', name: 'Inferior', nameTeluguPlaceholder: '???' },
          { id: 'empty', name: 'Empty', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'hurt',
        name: 'Hurt',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'embarrassed', name: 'Embarrassed', nameTeluguPlaceholder: '???' },
          { id: 'disappointed', name: 'Disappointed', nameTeluguPlaceholder: '???' }
        ]
      }
    ]
  },
  {
    id: 'disgusted',
    name: 'Disgusted',
    nameTeluguPlaceholder: '???',
    color: '#9ACD32',
    angle: 102.8,
    level2Emotions: [
      {
        id: 'disapproving',
        name: 'Disapproving',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'judgemental', name: 'Judgemental', nameTeluguPlaceholder: '???' },
          { id: 'embarrassed-disgust', name: 'Embarrassed', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'disappointed-disgust',
        name: 'Disappointed',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'appalled', name: 'Appalled', nameTeluguPlaceholder: '???' },
          { id: 'revolted', name: 'Revolted', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'awful',
        name: 'Awful',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'nauseated', name: 'Nauseated', nameTeluguPlaceholder: '???' },
          { id: 'detestable', name: 'Detestable', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'repelled',
        name: 'Repelled',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'horrified', name: 'Horrified', nameTeluguPlaceholder: '???' },
          { id: 'hesitant', name: 'Hesitant', nameTeluguPlaceholder: '???' }
        ]
      }
    ]
  },
  {
    id: 'angry',
    name: 'Angry',
    nameTeluguPlaceholder: '???',
    color: '#DC143C',
    angle: 154.2,
    level2Emotions: [
      {
        id: 'let-down',
        name: 'Let Down',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'betrayed', name: 'Betrayed', nameTeluguPlaceholder: '???' },
          { id: 'resentful', name: 'Resentful', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'humiliated',
        name: 'Humiliated',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'disrespected', name: 'Disrespected', nameTeluguPlaceholder: '???' },
          { id: 'ridiculed', name: 'Ridiculed', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'bitter',
        name: 'Bitter',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'indignant', name: 'Indignant', nameTeluguPlaceholder: '???' },
          { id: 'violated', name: 'Violated', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'mad',
        name: 'Mad',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'furious', name: 'Furious', nameTeluguPlaceholder: '???' },
          { id: 'jealous', name: 'Jealous', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'aggressive',
        name: 'Aggressive',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'provoked', name: 'Provoked', nameTeluguPlaceholder: '???' },
          { id: 'hostile', name: 'Hostile', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'frustrated',
        name: 'Frustrated',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'infuriated', name: 'Infuriated', nameTeluguPlaceholder: '???' },
          { id: 'annoyed', name: 'Annoyed', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'distant',
        name: 'Distant',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'withdrawn', name: 'Withdrawn', nameTeluguPlaceholder: '???' },
          { id: 'numb', name: 'Numb', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'critical',
        name: 'Critical',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'sceptical', name: 'Sceptical', nameTeluguPlaceholder: '???' },
          { id: 'dismissive', name: 'Dismissive', nameTeluguPlaceholder: '???' }
        ]
      }
    ]
  },
  {
    id: 'fearful',
    name: 'Fearful',
    nameTeluguPlaceholder: '???',
    color: '#9370DB',
    angle: 205.6,
    level2Emotions: [
      {
        id: 'scared',
        name: 'Scared',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'helpless', name: 'Helpless', nameTeluguPlaceholder: '???' },
          { id: 'frightened', name: 'Frightened', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'anxious',
        name: 'Anxious',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'overwhelmed-fear', name: 'Overwhelmed', nameTeluguPlaceholder: '???' },
          { id: 'worried', name: 'Worried', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'insecure',
        name: 'Insecure',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'inadequate', name: 'Inadequate', nameTeluguPlaceholder: '???' },
          { id: 'inferior-fear', name: 'Inferior', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'weak',
        name: 'Weak',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'worthless', name: 'Worthless', nameTeluguPlaceholder: '???' },
          { id: 'insignificant', name: 'Insignificant', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'rejected',
        name: 'Rejected',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'excluded', name: 'Excluded', nameTeluguPlaceholder: '???' },
          { id: 'persecuted', name: 'Persecuted', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'threatened',
        name: 'Threatened',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'nervous', name: 'Nervous', nameTeluguPlaceholder: '???' },
          { id: 'exposed', name: 'Exposed', nameTeluguPlaceholder: '???' }
        ]
      }
    ]
  },
  {
    id: 'bad',
    name: 'Bad',
    nameTeluguPlaceholder: '???',
    color: '#808080',
    angle: 257,
    level2Emotions: [
      {
        id: 'bored',
        name: 'Bored',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'indifferent', name: 'Indifferent', nameTeluguPlaceholder: '???' },
          { id: 'apathetic', name: 'Apathetic', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'busy',
        name: 'Busy',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'pressured', name: 'Pressured', nameTeluguPlaceholder: '???' },
          { id: 'rushed', name: 'Rushed', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'stressed',
        name: 'Stressed',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'overwhelmed-bad', name: 'Overwhelmed', nameTeluguPlaceholder: '???' },
          { id: 'out-of-control', name: 'Out of Control', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'tired',
        name: 'Tired',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'sleepy', name: 'Sleepy', nameTeluguPlaceholder: '???' },
          { id: 'unfocused', name: 'Unfocused', nameTeluguPlaceholder: '???' }
        ]
      }
    ]
  },
  {
    id: 'surprised',
    name: 'Surprised',
    nameTeluguPlaceholder: '???',
    color: '#FF6347',
    angle: 308.4,
    level2Emotions: [
      {
        id: 'startled',
        name: 'Startled',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'shocked', name: 'Shocked', nameTeluguPlaceholder: '???' },
          { id: 'dismayed', name: 'Dismayed', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'confused',
        name: 'Confused',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'disillusioned', name: 'Disillusioned', nameTeluguPlaceholder: '???' },
          { id: 'perplexed', name: 'Perplexed', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'amazed',
        name: 'Amazed',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'astonished', name: 'Astonished', nameTeluguPlaceholder: '???' },
          { id: 'awe', name: 'Awe', nameTeluguPlaceholder: '???' }
        ]
      },
      {
        id: 'excited',
        name: 'Excited',
        nameTeluguPlaceholder: '???',
        level3Emotions: [
          { id: 'eager', name: 'Eager', nameTeluguPlaceholder: '???' },
          { id: 'energetic', name: 'Energetic', nameTeluguPlaceholder: '???' }
        ]
      }
    ]
  }
];

export const getEmotionName = (emotion: EmotionLevel1 | EmotionLevel2 | EmotionLevel3, language: 'en' | 'te'): string => {
  if (language === 'en') {
    return emotion.name;
  }
  return emotion.nameTeluguPlaceholder;
};

export const getAllLevel3Emotions = (primaryEmotion: EmotionLevel1): EmotionLevel3[] => {
  return primaryEmotion.level2Emotions.flatMap(level2 => level2.level3Emotions);
};

export const getAllLevel2Emotions = (primaryEmotion: EmotionLevel1): EmotionLevel2[] => {
  return primaryEmotion.level2Emotions;
};
