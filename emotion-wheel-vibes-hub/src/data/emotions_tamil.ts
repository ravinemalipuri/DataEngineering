
export interface EmotionLevel3Tamil {
  id: string;
  nameTamil: string;
}

export interface EmotionLevel2Tamil {
  id: string;
  nameTamil: string;
  level3Emotions: EmotionLevel3Tamil[];
}

export interface EmotionLevel1Tamil {
  id: string;
  nameTamil: string;
  color: string;
  angle: number;
  level2Emotions: EmotionLevel2Tamil[];
}

export const emotionsDataTamil: EmotionLevel1Tamil[] = [
  {
    id: 'happy',
    nameTamil: 'மகிழ்ச்சி',
    color: '#FFD700',
    angle: 0,
    level2Emotions: [
      {
        id: 'playful',
        nameTamil: 'விளையாட்டுத்தனமான',
        level3Emotions: [
          { id: 'aroused', nameTamil: '???' },
          { id: 'cheeky', nameTamil: 'துணிச்சலான' }
        ]
      },
      {
        id: 'content',
        nameTamil: 'மகிழ்ச்சியான',
        level3Emotions: [
          { id: 'free', nameTamil: 'இலவச' },
          { id: 'joyful', nameTamil: 'மகிழ்ச்சியான' }
        ]
      },
      {
        id: 'interested',
        nameTamil: 'ஆர்வமுள்ள',
        level3Emotions: [
          { id: 'curious', nameTamil: 'ஆர்வமுள்ள' },
          { id: 'inquisitive', nameTamil: 'விசாரணை' }
        ]
      },
      {
        id: 'proud',
        nameTamil: 'பெருமைப்படுகிறேன்',
        level3Emotions: [
          { id: 'successful', nameTamil: 'வெற்றிகரமான' },
          { id: 'confident', nameTamil: 'தன்னம்பிக்கை' }
        ]
      },
      {
        id: 'accepted',
        nameTamil: 'ஏற்றுக்கொள்ளப்பட்டது',
        level3Emotions: [
          { id: 'respected', nameTamil: 'மதிக்கப்பட்ட' },
          { id: 'valued', nameTamil: 'மதிப்புமிக்க' }
        ]
      },
      {
        id: 'powerful',
        nameTamil: 'சக்திவாய்ந்த',
        level3Emotions: [
          { id: 'courageous', nameTamil: 'தைரியமான' },
          { id: 'creative', nameTamil: 'படைப்பாற்றல்' }
        ]
      },
      {
        id: 'peaceful',
        nameTamil: 'அமைதியான',
        level3Emotions: [
          { id: 'loving', nameTamil: 'அன்பான' },
          { id: 'thankful', nameTamil: 'நன்றியுள்ள' }
        ]
      },
      {
        id: 'trusting',
        nameTamil: 'நம்பும்',
        level3Emotions: [
          { id: 'sensitive', nameTamil: 'உணர்திறன்' },
          { id: 'intimate', nameTamil: 'நெருக்கமான' }
        ]
      },
      {
        id: 'optimistic',
        nameTamil: 'நம்பிக்கையான',
        level3Emotions: [
          { id: 'hopeful', nameTamil: 'நம்பிக்கையான' },
          { id: 'inspired', nameTamil: 'ஊக்கமளிக்கப்பட்ட' }
        ]
      }
    ]
  },
  {
    id: 'sad',
    nameTamil: 'சோகமான',
    color: '#4682B4',
    angle: 45,
    level2Emotions: [
      {
        id: 'lonely',
        nameTamil: 'தனிமையான',
        level3Emotions: [
          { id: 'isolated', nameTamil: 'தனிமைப்படுத்தப்பட்ட' },
          { id: 'abandoned', nameTamil: 'கைவிடப்பட்ட' }
        ]
      },
      {
        id: 'vulnerable',
        nameTamil: 'பாதிக்கப்படக்கூடிய',
        level3Emotions: [
          { id: 'victimised', nameTamil: 'பாதிக்கப்பட்ட' },
          { id: 'fragile', nameTamil: 'உடையக்கூடிய' }
        ]
      },
      {
        id: 'despair',
        nameTamil: 'நம்பிக்கையற்ற',
        level3Emotions: [
          { id: 'grief', nameTamil: 'துக்கம்' },
          { id: 'powerless', nameTamil: 'சக்தியற்ற' }
        ]
      },
      {
        id: 'guilty',
        nameTamil: 'குற்றவுணர்வு',
        level3Emotions: [
          { id: 'ashamed', nameTamil: 'வெட்கப்படுகிறேன்' },
          { id: 'remorseful', nameTamil: 'வருந்துகிறேன்' }
        ]
      },
      {
        id: 'depressed',
        nameTamil: 'மனச்சோர்வு',
        level3Emotions: [
          { id: 'inferior', nameTamil: 'தாழ்ந்த' },
          { id: 'empty', nameTamil: 'வெறுமையான' }
        ]
      },
      {
        id: 'hurt',
        nameTamil: 'காயம்',
        level3Emotions: [
          { id: 'embarrassed', nameTamil: 'சங்கடமாக' },
          { id: 'disappointed', nameTamil: 'ஏமாற்றமடைந்த' }
        ]
      }
    ]
  },
  {
    id: 'disgusted',
    nameTamil: 'வெறுப்பு',
    color: '#9ACD32',
    angle: 90,
    level2Emotions: [
      {
        id: 'disapproving',
        nameTamil: '???',
        level3Emotions: [
          { id: 'judgemental', nameTamil: '???' },
          { id: 'embarrassed-disgust', nameTamil: 'சங்கடமாக' }
        ]
      },
      {
        id: 'disappointed-disgust',
        nameTamil: 'ஏமாற்றமடைந்த',
        level3Emotions: [
          { id: 'appalled', nameTamil: '???' },
          { id: 'revolted', nameTamil: '???' }
        ]
      },
      {
        id: 'awful',
        nameTamil: 'மோசமான',
        level3Emotions: [
          { id: 'nauseated', nameTamil: '???' },
          { id: 'detestable', nameTamil: '???' }
        ]
      },
      {
        id: 'repelled',
        nameTamil: '???',
        level3Emotions: [
          { id: 'horrified', nameTamil: '???' },
          { id: 'hesitant', nameTamil: '???' }
        ]
      }
    ]
  },
  {
    id: 'angry',
    nameTamil: 'கோபமாக',
    color: '#DC143C',
    angle: 135,
    level2Emotions: [
      {
        id: 'let-down',
        nameTamil: 'ஏமாற்றம்',
        level3Emotions: [
          { id: 'betrayed', nameTamil: 'துரோகம்' },
          { id: 'resentful', nameTamil: '???' }
        ]
      },
      {
        id: 'humiliated',
        nameTamil: 'அவமானப்படுத்தப்பட்ட',
        level3Emotions: [
          { id: 'disrespected', nameTamil: '???' },
          { id: 'ridiculed', nameTamil: '???' }
        ]
      },
      {
        id: 'bitter',
        nameTamil: 'கசப்பான',
        level3Emotions: [
          { id: 'indignant', nameTamil: '???' },
          { id: 'violated', nameTamil: '???' }
        ]
      },
      {
        id: 'mad',
        nameTamil: 'பைத்தியம்',
        level3Emotions: [
          { id: 'furious', nameTamil: '???' },
          { id: 'jealous', nameTamil: 'பொறாமை' }
        ]
      },
      {
        id: 'aggressive',
        nameTamil: 'ஆக்கிரமிப்பு',
        level3Emotions: [
          { id: 'provoked', nameTamil: '???' },
          { id: 'hostile', nameTamil: '???' }
        ]
      },
      {
        id: 'frustrated',
        nameTamil: '???',
        level3Emotions: [
          { id: 'infuriated', nameTamil: '???' },
          { id: 'annoyed', nameTamil: '???' }
        ]
      },
      {
        id: 'distant',
        nameTamil: 'தொலைவில்',
        level3Emotions: [
          { id: 'withdrawn', nameTamil: '???' },
          { id: 'numb', nameTamil: '???' }
        ]
      },
      {
        id: 'critical',
        nameTamil: '???',
        level3Emotions: [
          { id: 'sceptical', nameTamil: '???' },
          { id: 'dismissive', nameTamil: '???' }
        ]
      }
    ]
  },
  {
    id: 'fearful',
    nameTamil: 'பயமுறுத்தும்',
    color: '#9370DB',
    angle: 180,
    level2Emotions: [
      {
        id: 'scared',
        nameTamil: 'பயந்த',
        level3Emotions: [
          { id: 'helpless', nameTamil: 'உதவியற்ற' },
          { id: 'frightened', nameTamil: 'பயந்த' }
        ]
      },
      {
        id: 'anxious',
        nameTamil: 'பதற்றமான',
        level3Emotions: [
          { id: 'overwhelmed-fear', nameTamil: '???' },
          { id: 'worried', nameTamil: 'கவலைப்படுகிறேன்' }
        ]
      },
      {
        id: 'insecure',
        nameTamil: 'பாதுகாப்பற்ற',
        level3Emotions: [
          { id: 'inadequate', nameTamil: '???' },
          { id: 'inferior-fear', nameTamil: 'தாழ்ந்த' }
        ]
      },
      {
        id: 'weak',
        nameTamil: 'பலவீனமான',
        level3Emotions: [
          { id: 'worthless', nameTamil: '???' },
          { id: 'insignificant', nameTamil: '???' }
        ]
      },
      {
        id: 'rejected',
        nameTamil: 'நிராகரிக்கப்பட்ட',
        level3Emotions: [
          { id: 'excluded', nameTamil: '???' },
          { id: 'persecuted', nameTamil: '???' }
        ]
      },
      {
        id: 'threatened',
        nameTamil: 'அச்சுறுத்தல்',
        level3Emotions: [
          { id: 'nervous', nameTamil: 'பதற்றமான' },
          { id: 'exposed', nameTamil: '???' }
        ]
      }
    ]
  },
  {
    id: 'bad',
    nameTamil: 'கெட்ட',
    color: '#808080',
    angle: 225,
    level2Emotions: [
      {
        id: 'bored',
        nameTamil: 'சலிப்பு',
        level3Emotions: [
          { id: 'indifferent', nameTamil: '???' },
          { id: 'apathetic', nameTamil: '???' }
        ]
      },
      {
        id: 'busy',
        nameTamil: 'பரபரப்பான',
        level3Emotions: [
          { id: 'pressured', nameTamil: '???' },
          { id: 'rushed', nameTamil: '???' }
        ]
      },
      {
        id: 'stressed',
        nameTamil: 'மன அழுத்தம்',
        level3Emotions: [
          { id: 'overwhelmed-bad', nameTamil: '???' },
          { id: 'out-of-control', nameTamil: '???' }
        ]
      },
      {
        id: 'tired',
        nameTamil: 'சோர்வாக',
        level3Emotions: [
          { id: 'sleepy', nameTamil: 'தூக்கமாக' },
          { id: 'unfocused', nameTamil: '???' }
        ]
      }
    ]
  },
  {
    id: 'surprised',
    nameTamil: 'ஆச்சரியப்பட்டேன்',
    color: '#FF6347',
    angle: 270,
    level2Emotions: [
      {
        id: 'startled',
        nameTamil: '???',
        level3Emotions: [
          { id: 'shocked', nameTamil: 'அதிர்ச்சி' },
          { id: 'dismayed', nameTamil: '???' }
        ]
      },
      {
        id: 'confused',
        nameTamil: 'குழப்பமான',
        level3Emotions: [
          { id: 'disillusioned', nameTamil: '???' },
          { id: 'perplexed', nameTamil: '???' }
        ]
      },
      {
        id: 'amazed',
        nameTamil: 'வியப்பு',
        level3Emotions: [
          { id: 'astonished', nameTamil: '???' },
          { id: 'awe', nameTamil: '???' }
        ]
      },
      {
        id: 'excited',
        nameTamil: 'உற்சாகமான',
        level3Emotions: [
          { id: 'eager', nameTamil: 'ஆவலுடன்' },
          { id: 'energetic', nameTamil: 'சுறுசுறுப்பான' }
        ]
      }
    ]
  }
];
