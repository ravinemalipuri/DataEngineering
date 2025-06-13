
export interface EmotionLevel3 {
  id: string;
  nameEnglish: string;
}

export interface EmotionLevel2 {
  id: string;
  nameEnglish: string;
  level3Emotions: EmotionLevel3[];
}

export interface EmotionLevel1 {
  id: string;
  nameEnglish: string;
  color: string;
  angle: number;
  level2Emotions: EmotionLevel2[];
}

export const emotionsDataEnglish: EmotionLevel1[] = [
  {
    id: 'happy',
    nameEnglish: 'Happy',
    color: '#FFD700',
    angle: 0,
    level2Emotions: [
      {
        id: 'playful',
        nameEnglish: 'Playful',
        level3Emotions: [
          { id: 'aroused', nameEnglish: 'Aroused' },
          { id: 'cheeky', nameEnglish: 'Cheeky' }
        ]
      },
      {
        id: 'content',
        nameEnglish: 'Content',
        level3Emotions: [
          { id: 'free', nameEnglish: 'Free' },
          { id: 'joyful', nameEnglish: 'Joyful' }
        ]
      },
      {
        id: 'interested',
        nameEnglish: 'Interested',
        level3Emotions: [
          { id: 'curious', nameEnglish: 'Curious' },
          { id: 'inquisitive', nameEnglish: 'Inquisitive' }
        ]
      },
      {
        id: 'proud',
        nameEnglish: 'Proud',
        level3Emotions: [
          { id: 'successful', nameEnglish: 'Successful' },
          { id: 'confident', nameEnglish: 'Confident' }
        ]
      },
      {
        id: 'accepted',
        nameEnglish: 'Accepted',
        level3Emotions: [
          { id: 'respected', nameEnglish: 'Respected' },
          { id: 'valued', nameEnglish: 'Valued' }
        ]
      },
      {
        id: 'powerful',
        nameEnglish: 'Powerful',
        level3Emotions: [
          { id: 'courageous', nameEnglish: 'Courageous' },
          { id: 'creative', nameEnglish: 'Creative' }
        ]
      },
      {
        id: 'peaceful',
        nameEnglish: 'Peaceful',
        level3Emotions: [
          { id: 'loving', nameEnglish: 'Loving' },
          { id: 'thankful', nameEnglish: 'Thankful' }
        ]
      },
      {
        id: 'trusting',
        nameEnglish: 'Trusting',
        level3Emotions: [
          { id: 'sensitive', nameEnglish: 'Sensitive' },
          { id: 'intimate', nameEnglish: 'Intimate' }
        ]
      },
      {
        id: 'optimistic',
        nameEnglish: 'Optimistic',
        level3Emotions: [
          { id: 'hopeful', nameEnglish: 'Hopeful' },
          { id: 'inspired', nameEnglish: 'Inspired' }
        ]
      }
    ]
  },
  {
    id: 'sad',
    nameEnglish: 'Sad',
    color: '#4682B4',
    angle: 45,
    level2Emotions: [
      {
        id: 'lonely',
        nameEnglish: 'Lonely',
        level3Emotions: [
          { id: 'isolated', nameEnglish: 'Isolated' },
          { id: 'abandoned', nameEnglish: 'Abandoned' }
        ]
      },
      {
        id: 'vulnerable',
        nameEnglish: 'Vulnerable',
        level3Emotions: [
          { id: 'victimised', nameEnglish: 'Victimised' },
          { id: 'fragile', nameEnglish: 'Fragile' }
        ]
      },
      {
        id: 'despair',
        nameEnglish: 'Despair',
        level3Emotions: [
          { id: 'grief', nameEnglish: 'Grief' },
          { id: 'powerless', nameEnglish: 'Powerless' }
        ]
      },
      {
        id: 'guilty',
        nameEnglish: 'Guilty',
        level3Emotions: [
          { id: 'ashamed', nameEnglish: 'Ashamed' },
          { id: 'remorseful', nameEnglish: 'Remorseful' }
        ]
      },
      {
        id: 'depressed',
        nameEnglish: 'Depressed',
        level3Emotions: [
          { id: 'inferior', nameEnglish: 'Inferior' },
          { id: 'empty', nameEnglish: 'Empty' }
        ]
      },
      {
        id: 'hurt',
        nameEnglish: 'Hurt',
        level3Emotions: [
          { id: 'embarrassed', nameEnglish: 'Embarrassed' },
          { id: 'disappointed', nameEnglish: 'Disappointed' }
        ]
      }
    ]
  },
  {
    id: 'disgusted',
    nameEnglish: 'Disgusted',
    color: '#9ACD32',
    angle: 90,
    level2Emotions: [
      {
        id: 'disapproving',
        nameEnglish: 'Disapproving',
        level3Emotions: [
          { id: 'judgemental', nameEnglish: 'Judgemental' },
          { id: 'embarrassed-disgust', nameEnglish: 'Embarrassed' }
        ]
      },
      {
        id: 'disappointed-disgust',
        nameEnglish: 'Disappointed',
        level3Emotions: [
          { id: 'appalled', nameEnglish: 'Appalled' },
          { id: 'revolted', nameEnglish: 'Revolted' }
        ]
      },
      {
        id: 'awful',
        nameEnglish: 'Awful',
        level3Emotions: [
          { id: 'nauseated', nameEnglish: 'Nauseated' },
          { id: 'detestable', nameEnglish: 'Detestable' }
        ]
      },
      {
        id: 'repelled',
        nameEnglish: 'Repelled',
        level3Emotions: [
          { id: 'horrified', nameEnglish: 'Horrified' },
          { id: 'hesitant', nameEnglish: 'Hesitant' }
        ]
      }
    ]
  },
  {
    id: 'angry',
    nameEnglish: 'Angry',
    color: '#DC143C',
    angle: 135,
    level2Emotions: [
      {
        id: 'let-down',
        nameEnglish: 'Let Down',
        level3Emotions: [
          { id: 'betrayed', nameEnglish: 'Betrayed' },
          { id: 'resentful', nameEnglish: 'Resentful' }
        ]
      },
      {
        id: 'humiliated',
        nameEnglish: 'Humiliated',
        level3Emotions: [
          { id: 'disrespected', nameEnglish: 'Disrespected' },
          { id: 'ridiculed', nameEnglish: 'Ridiculed' }
        ]
      },
      {
        id: 'bitter',
        nameEnglish: 'Bitter',
        level3Emotions: [
          { id: 'indignant', nameEnglish: 'Indignant' },
          { id: 'violated', nameEnglish: 'Violated' }
        ]
      },
      {
        id: 'mad',
        nameEnglish: 'Mad',
        level3Emotions: [
          { id: 'furious', nameEnglish: 'Furious' },
          { id: 'jealous', nameEnglish: 'Jealous' }
        ]
      },
      {
        id: 'aggressive',
        nameEnglish: 'Aggressive',
        level3Emotions: [
          { id: 'provoked', nameEnglish: 'Provoked' },
          { id: 'hostile', nameEnglish: 'Hostile' }
        ]
      },
      {
        id: 'frustrated',
        nameEnglish: 'Frustrated',
        level3Emotions: [
          { id: 'infuriated', nameEnglish: 'Infuriated' },
          { id: 'annoyed', nameEnglish: 'Annoyed' }
        ]
      },
      {
        id: 'distant',
        nameEnglish: 'Distant',
        level3Emotions: [
          { id: 'withdrawn', nameEnglish: 'Withdrawn' },
          { id: 'numb', nameEnglish: 'Numb' }
        ]
      },
      {
        id: 'critical',
        nameEnglish: 'Critical',
        level3Emotions: [
          { id: 'sceptical', nameEnglish: 'Sceptical' },
          { id: 'dismissive', nameEnglish: 'Dismissive' }
        ]
      }
    ]
  },
  {
    id: 'fearful',
    nameEnglish: 'Fearful',
    color: '#9370DB',
    angle: 180,
    level2Emotions: [
      {
        id: 'scared',
        nameEnglish: 'Scared',
        level3Emotions: [
          { id: 'helpless', nameEnglish: 'Helpless' },
          { id: 'frightened', nameEnglish: 'Frightened' }
        ]
      },
      {
        id: 'anxious',
        nameEnglish: 'Anxious',
        level3Emotions: [
          { id: 'overwhelmed-fear', nameEnglish: 'Overwhelmed' },
          { id: 'worried', nameEnglish: 'Worried' }
        ]
      },
      {
        id: 'insecure',
        nameEnglish: 'Insecure',
        level3Emotions: [
          { id: 'inadequate', nameEnglish: 'Inadequate' },
          { id: 'inferior-fear', nameEnglish: 'Inferior' }
        ]
      },
      {
        id: 'weak',
        nameEnglish: 'Weak',
        level3Emotions: [
          { id: 'worthless', nameEnglish: 'Worthless' },
          { id: 'insignificant', nameEnglish: 'Insignificant' }
        ]
      },
      {
        id: 'rejected',
        nameEnglish: 'Rejected',
        level3Emotions: [
          { id: 'excluded', nameEnglish: 'Excluded' },
          { id: 'persecuted', nameEnglish: 'Persecuted' }
        ]
      },
      {
        id: 'threatened',
        nameEnglish: 'Threatened',
        level3Emotions: [
          { id: 'nervous', nameEnglish: 'Nervous' },
          { id: 'exposed', nameEnglish: 'Exposed' }
        ]
      }
    ]
  },
  {
    id: 'bad',
    nameEnglish: 'Bad',
    color: '#808080',
    angle: 225,
    level2Emotions: [
      {
        id: 'bored',
        nameEnglish: 'Bored',
        level3Emotions: [
          { id: 'indifferent', nameEnglish: 'Indifferent' },
          { id: 'apathetic', nameEnglish: 'Apathetic' }
        ]
      },
      {
        id: 'busy',
        nameEnglish: 'Busy',
        level3Emotions: [
          { id: 'pressured', nameEnglish: 'Pressured' },
          { id: 'rushed', nameEnglish: 'Rushed' }
        ]
      },
      {
        id: 'stressed',
        nameEnglish: 'Stressed',
        level3Emotions: [
          { id: 'overwhelmed-bad', nameEnglish: 'Overwhelmed' },
          { id: 'out-of-control', nameEnglish: 'Out of Control' }
        ]
      },
      {
        id: 'tired',
        nameEnglish: 'Tired',
        level3Emotions: [
          { id: 'sleepy', nameEnglish: 'Sleepy' },
          { id: 'unfocused', nameEnglish: 'Unfocused' }
        ]
      }
    ]
  },
  {
    id: 'surprised',
    nameEnglish: 'Surprised',
    color: '#FF6347',
    angle: 270,
    level2Emotions: [
      {
        id: 'startled',
        nameEnglish: 'Startled',
        level3Emotions: [
          { id: 'shocked', nameEnglish: 'Shocked' },
          { id: 'dismayed', nameEnglish: 'Dismayed' }
        ]
      },
      {
        id: 'confused',
        nameEnglish: 'Confused',
        level3Emotions: [
          { id: 'disillusioned', nameEnglish: 'Disillusioned' },
          { id: 'perplexed', nameEnglish: 'Perplexed' }
        ]
      },
      {
        id: 'amazed',
        nameEnglish: 'Amazed',
        level3Emotions: [
          { id: 'astonished', nameEnglish: 'Astonished' },
          { id: 'awe', nameEnglish: 'Awe' }
        ]
      },
      {
        id: 'excited',
        nameEnglish: 'Excited',
        level3Emotions: [
          { id: 'eager', nameEnglish: 'Eager' },
          { id: 'energetic', nameEnglish: 'Energetic' }
        ]
      }
    ]
  }
];
