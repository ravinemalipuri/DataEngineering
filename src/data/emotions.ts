
export interface EmotionLevel3 {
  id: string;
  name: string;
  nameTelugu: string;
}

export interface EmotionLevel2 {
  id: string;
  name: string;
  nameTelugu: string;
  level3Emotions: EmotionLevel3[];
}

export interface EmotionLevel1 {
  id: string;
  name: string;
  nameTelugu: string;
  color: string;
  angle: number;
  level2Emotions: EmotionLevel2[];
}

export const emotionsData: EmotionLevel1[] = [
  {
    id: 'happy',
    name: 'Happy',
    nameTelugu: 'సంతోషం',
    color: '#FFD700',
    angle: 0,
    level2Emotions: [
      {
        id: 'playful',
        name: 'Playful',
        nameTelugu: 'ఉల్లాసభరితమైన',
        level3Emotions: [
          { id: 'aroused', name: 'Aroused', nameTelugu: 'రెచ్చిపోయింది' },
          { id: 'cheeky', name: 'Cheeky', nameTelugu: 'కొంటెయైన?' }
        ]
      },
      {
        id: 'content',
        name: 'Content',
        nameTelugu: 'నిమ్మళముగా, తొణకకుండా',
        level3Emotions: [
          { id: 'free', name: 'Free', nameTelugu: 'ఉచిత' },
          { id: 'joyful', name: 'Joyful', nameTelugu: 'సంతోషకరమైన' }
        ]
      },
      {
        id: 'interested',
        name: 'Interested',
        nameTelugu: 'ఆసక్తి',
        level3Emotions: [
          { id: 'curious', name: 'Curious', nameTelugu: 'ఉత్సుకత' },
          { id: 'inquisitive', name: 'InQuisitive', nameTelugu: 'ఆసక్తిగల' }
        ]
      },
      {
        id: 'proud',
        name: 'Proud',
        nameTelugu: 'గర్వంగా ఉంది',
        level3Emotions: [
          { id: 'successful', name: 'Successful', nameTelugu: 'విజయవంతమైంది' },
          { id: 'confident', name: 'Confident', nameTelugu: 'నమ్మకంగా' }
        ]
      },
      {
        id: 'accepted',
        name: 'Accepted',
        nameTelugu: 'అంగీకరించబడింది',
        level3Emotions: [
          { id: 'respected', name: 'Respected', nameTelugu: 'గౌరవించారు' },
          { id: 'valued', name: 'Valued', nameTelugu: 'విలువైనది' }
        ]
      },
      {
        id: 'powerful',
        name: 'Powerful',
        nameTelugu: 'శక్తివంతమైన',
        level3Emotions: [
          { id: 'courageous', name: 'Courageous', nameTelugu: 'ధైర్యవంతుడు' },
          { id: 'creative', name: 'Creative', nameTelugu: 'సృజనాత్మకమైనది' }
        ]
      },
      {
        id: 'peaceful',
        name: 'Peaceful',
        nameTelugu: 'శాంతియుతమైనది',
        level3Emotions: [
          { id: 'loving', name: 'Loving', nameTelugu: 'ప్రేమించే' },
          { id: 'thankful', name: 'Thankful', nameTelugu: 'ధన్యవాదములు' }
        ]
      },
      {
        id: 'trusting',
        name: 'Trusting',
        nameTelugu: 'విశ్వసించడం',
        level3Emotions: [
          { id: 'sensitive', name: 'Sensitive', nameTelugu: 'సున్నితమైన' },
          { id: 'intimate', name: 'Intimate', nameTelugu: 'సన్నిహితుడు' }
        ]
      },
      {
        id: 'optimistic',
        name: 'Optimistic',
        nameTelugu: 'ఆశావాది',
        level3Emotions: [
          { id: 'hopeful', name: 'Hopeful', nameTelugu: 'ఆశాజనకంగా' },
          { id: 'inspired', name: 'Inspired', nameTelugu: 'ప్రేరణ పొందింది' }
        ]
      }
    ]
  },
  {
    id: 'sad',
    name: 'Sad',
    nameTelugu: 'విచారకరం',
    color: '#4682B4',
    angle: 45,
    level2Emotions: [
      {
        id: 'lonely',
        name: 'Lonely',
        nameTelugu: 'ఒంటరి',
        level3Emotions: [
          { id: 'isolated', name: 'Isolated', nameTelugu: 'ఒంటరిగా' },
          { id: 'abandoned', name: 'Abandoned', nameTelugu: 'విడిచిపెట్టారు' }
        ]
      },
      {
        id: 'vulnerable',
        name: 'Vulnerable',
        nameTelugu: 'దుర్బలమైనది',
        level3Emotions: [
          { id: 'victimised', name: 'Victimised', nameTelugu: 'బాధితులయ్యారు' },
          { id: 'fragile', name: 'Fragile', nameTelugu: 'పెళుసుగా' }
        ]
      },
      {
        id: 'despair',
        name: 'Despair',
        nameTelugu: 'నిరాశ',
        level3Emotions: [
          { id: 'grief', name: 'Grief', nameTelugu: 'దుఃఖం' },
          { id: 'powerless', name: 'Powerless', nameTelugu: 'శక్తిలేని' }
        ]
      },
      {
        id: 'guilty',
        name: 'Guilty',
        nameTelugu: 'దోషి',
        level3Emotions: [
          { id: 'ashamed', name: 'Ashamed', nameTelugu: 'సిగ్గుపడింది' },
          { id: 'remorseful', name: 'Remorseful', nameTelugu: 'పశ్చాత్తాపపడుతుంది' }
        ]
      },
      {
        id: 'depressed',
        name: 'Depressed',
        nameTelugu: 'అణగారిన',
        level3Emotions: [
          { id: 'inferior', name: 'Inferior', nameTelugu: 'నాసిరకం' },
          { id: 'empty', name: 'Empty', nameTelugu: 'ఖాళీ' }
        ]
      },
      {
        id: 'hurt',
        name: 'Hurt',
        nameTelugu: 'హర్ట్',
        level3Emotions: [
          { id: 'embarrassed', name: 'Embarrassed', nameTelugu: 'సంకటపడే' },
          { id: 'disappointed', name: 'Disappointed', nameTelugu: 'నిరాశ చెందారు' }
        ]
      }
    ]
  },
  {
    id: 'disgusted',
    name: 'Disgusted',
    nameTelugu: 'అసహ్యం',
    color: '#9ACD32',
    angle: 90,
    level2Emotions: [
      {
        id: 'disapproving',
        name: 'Disapproving',
        nameTelugu: 'నిరాకరించడం',
        level3Emotions: [
          { id: 'judgemental', name: 'Judgemental', nameTelugu: 'జడ్జిమెంటల్' },
          { id: 'embarrassed-disgust', name: 'Embarrassed', nameTelugu: 'సిగ్గుపడింది' }
        ]
      },
      {
        id: 'disappointed-disgust',
        name: 'Disappointed',
        nameTelugu: 'నిరాశ చెందారు',
        level3Emotions: [
          { id: 'appalled', name: 'Appalled', nameTelugu: 'దిగ్భ్రాంతి చెందాడు' },
          { id: 'revolted', name: 'Revolted', nameTelugu: 'తిరుగుబాటు చేశారు' }
        ]
      },
      {
        id: 'awful',
        name: 'Awful',
        nameTelugu: 'భయంకరం',
        level3Emotions: [
          { id: 'nauseated', name: 'Nauseated', nameTelugu: 'వికారం' },
          { id: 'detestable', name: 'Detestable', nameTelugu: 'అసహ్యకరమైన' }
        ]
      },
      {
        id: 'repelled',
        name: 'Repelled',
        nameTelugu: 'తిప్పికొట్టారు',
        level3Emotions: [
          { id: 'horrified', name: 'Horrified', nameTelugu: 'భీతిల్లింది' },
          { id: 'hesitant', name: 'Hesitant', nameTelugu: 'సంశయం' }
        ]
      }
    ]
  },
  {
    id: 'angry',
    name: 'Angry',
    nameTelugu: 'కోపంగా',
    color: '#DC143C',
    angle: 135,
    level2Emotions: [
      {
        id: 'let-down',
        name: 'Let Down',
        nameTelugu: 'లెట్ డౌన్',
        level3Emotions: [
          { id: 'betrayed', name: 'Betrayed', nameTelugu: 'ద్రోహం చేశారు' },
          { id: 'resentful', name: 'Resentful', nameTelugu: 'ఆగ్రహంతో' }
        ]
      },
      {
        id: 'humiliated',
        name: 'Humiliated',
        nameTelugu: 'అవమానపరిచారు',
        level3Emotions: [
          { id: 'disrespected', name: 'Disrespected', nameTelugu: 'అగౌరవపరిచారు' },
          { id: 'ridiculed', name: 'Ridiculed', nameTelugu: 'ఎగతాళి చేశారు' }
        ]
      },
      {
        id: 'bitter',
        name: 'Bitter',
        nameTelugu: 'చేదు',
        level3Emotions: [
          { id: 'indignant', name: 'Indignant', nameTelugu: 'ఆగ్రహంతో' },
          { id: 'violated', name: 'Violated', nameTelugu: 'ఉల్లంఘించారు' }
        ]
      },
      {
        id: 'mad',
        name: 'Mad',
        nameTelugu: 'పిచ్చి',
        level3Emotions: [
          { id: 'furious', name: 'Furious', nameTelugu: 'కోపంతో' },
          { id: 'jealous', name: 'Jealous', nameTelugu: 'అసూయ' }
        ]
      },
      {
        id: 'aggressive',
        name: 'Aggressive',
        nameTelugu: 'దూకుడు',
        level3Emotions: [
          { id: 'provoked', name: 'Provoked', nameTelugu: 'రెచ్చిపోయారు' },
          { id: 'hostile', name: 'Hostile', nameTelugu: 'శత్రుత్వం' }
        ]
      },
      {
        id: 'frustrated',
        name: 'Frustrated',
        nameTelugu: 'విసుగు చెందారు',
        level3Emotions: [
          { id: 'infuriated', name: 'Infuriated', nameTelugu: 'చిరచిరలాడడ' },
          { id: 'annoyed', name: 'Annoyed', nameTelugu: 'చిరాకు' }
        ]
      },
      {
        id: 'distant',
        name: 'Distant',
        nameTelugu: 'దూరం',
        level3Emotions: [
          { id: 'withdrawn', name: 'Withdrawn', nameTelugu: 'ఉపసంహరించుకున్నారు' },
          { id: 'numb', name: 'Numb', nameTelugu: 'తిమ్మిరి' }
        ]
      },
      {
        id: 'critical',
        name: 'Critical',
        nameTelugu: 'క్లిష్టమైన',
        level3Emotions: [
          { id: 'sceptical', name: 'Sceptical', nameTelugu: 'సందేహాస్పదమైనది' },
          { id: 'dismissive', name: 'Dismissive', nameTelugu: 'నిరాకరణ' }
        ]
      }
    ]
  },
  {
    id: 'fearful',
    name: 'Fearful',
    nameTelugu: 'భయంగా',
    color: '#9370DB',
    angle: 180,
    level2Emotions: [
      {
        id: 'scared',
        name: 'Scared',
        nameTelugu: 'భయపడ్డాను',
        level3Emotions: [
          { id: 'helpless', name: 'Helpless', nameTelugu: 'నిస్సహాయుడు' },
          { id: 'frightened', name: 'Frightened', nameTelugu: 'భయపడ్డాను' }
        ]
      },
      {
        id: 'anxious',
        name: 'Anxious',
        nameTelugu: 'ఆత్రుత',
        level3Emotions: [
          { id: 'overwhelmed-fear', name: 'Overwhelmed', nameTelugu: 'పొంగిపోయింది' },
          { id: 'worried', name: 'Worried', nameTelugu: 'ఆందోళన చెందారు' }
        ]
      },
      {
        id: 'insecure',
        name: 'Insecure',
        nameTelugu: 'అభద్రత',
        level3Emotions: [
          { id: 'inadequate', name: 'Inadequate', nameTelugu: 'సరిపోదు' },
          { id: 'inferior-fear', name: 'Inferior', nameTelugu: 'నాసిరకం' }
        ]
      },
      {
        id: 'weak',
        name: 'Weak',
        nameTelugu: 'బలహీనమైనది',
        level3Emotions: [
          { id: 'worthless', name: 'Worthless', nameTelugu: 'విలువలేనిది' },
          { id: 'insignificant', name: 'Insignificant', nameTelugu: 'అప్రధానమైనది' }
        ]
      },
      {
        id: 'rejected',
        name: 'Rejected',
        nameTelugu: 'తిరస్కరించబడింది',
        level3Emotions: [
          { id: 'excluded', name: 'Excluded', nameTelugu: 'మినహాయించబడింది' },
          { id: 'persecuted', name: 'Persecuted', nameTelugu: 'పీడించబడ్డాడు' }
        ]
      },
      {
        id: 'threatened',
        name: 'Threatened',
        nameTelugu: 'బెదిరించారు',
        level3Emotions: [
          { id: 'nervous', name: 'Nervous', nameTelugu: 'నాడీ' },
          { id: 'exposed', name: 'Exposed', nameTelugu: 'బహిర్గతమైంది' }
        ]
      }
    ]
  },
  {
    id: 'bad',
    name: 'Bad',
    nameTelugu: 'చెడ్డది',
    color: '#808080',
    angle: 225,
    level2Emotions: [
      {
        id: 'bored',
        name: 'Bored',
        nameTelugu: 'బోర్ కొట్టింది',
        level3Emotions: [
          { id: 'indifferent', name: 'Indifferent', nameTelugu: 'ఉదాసీనం' },
          { id: 'apathetic', name: 'Apathetic', nameTelugu: 'విరక్తి' }
        ]
      },
      {
        id: 'busy',
        name: 'Busy',
        nameTelugu: 'బిజీ',
        level3Emotions: [
          { id: 'pressured', name: 'Pressured', nameTelugu: 'ఒత్తిడి చేశారు' },
          { id: 'rushed', name: 'Rushed', nameTelugu: 'పరుగెత్తింది' }
        ]
      },
      {
        id: 'stressed',
        name: 'Stressed',
        nameTelugu: 'ఒత్తిడికి లోనయ్యారు',
        level3Emotions: [
          { id: 'overwhelmed-bad', name: 'Overwhelmed', nameTelugu: 'పొంగిపోయింది' },
          { id: 'out-of-control', name: 'Out of Control', nameTelugu: 'అదుపు తప్పింది' }
        ]
      },
      {
        id: 'tired',
        name: 'Tired',
        nameTelugu: 'అలసిపోయింది',
        level3Emotions: [
          { id: 'sleepy', name: 'Sleepy', nameTelugu: 'నిద్ర పోతున్నది' },
          { id: 'unfocused', name: 'Unfocused', nameTelugu: 'దృష్టి పెట్టలేదు' }
        ]
      }
    ]
  },
  {
    id: 'surprised',
    name: 'Surprised',
    nameTelugu: 'ఆశ్చర్యపోయాను',
    color: '#FF6347',
    angle: 270,
    level2Emotions: [
      {
        id: 'startled',
        name: 'Startled',
        nameTelugu: 'స్టార్డ్',
        level3Emotions: [
          { id: 'shocked', name: 'Shocked', nameTelugu: 'షాక్ అయ్యాను' },
          { id: 'dismayed', name: 'Dismayed', nameTelugu: 'విస్తుపోయారు' }
        ]
      },
      {
        id: 'confused',
        name: 'Confused',
        nameTelugu: 'అయోమయంలో పడ్డారు',
        level3Emotions: [
          { id: 'disillusioned', name: 'Disillusioned', nameTelugu: 'భ్రమపడ్డాడు' },
          { id: 'perplexed', name: 'Perplexed', nameTelugu: 'ప్రీప్లెక్స్డ్' }
        ]
      },
      {
        id: 'amazed',
        name: 'Amazed',
        nameTelugu: 'ఆశ్చర్యపోయాడు',
        level3Emotions: [
          { id: 'astonished', name: 'Astonished', nameTelugu: 'ఆశ్చర్యపోయాడు' },
          { id: 'awe', name: 'Awe', nameTelugu: 'విస్మయం' }
        ]
      },
      {
        id: 'excited',
        name: 'Excited',
        nameTelugu: 'నిష్క్రమించారు',
        level3Emotions: [
          { id: 'eager', name: 'Eager', nameTelugu: 'ఆత్రుత' },
          { id: 'energetic', name: 'Energetic', nameTelugu: 'ఎనర్జిటిక్' }
        ]
      }
    ]
  }
];

export const getEmotionName = (emotion: EmotionLevel1 | EmotionLevel2 | EmotionLevel3, language: 'en' | 'te'): string => {
  if (language === 'en') {
    return emotion.name;
  }
  return emotion.nameTelugu;
};

export const getAllLevel3Emotions = (primaryEmotion: EmotionLevel1): EmotionLevel3[] => {
  return primaryEmotion.level2Emotions.flatMap(level2 => level2.level3Emotions);
};

export const getAllLevel2Emotions = (primaryEmotion: EmotionLevel1): EmotionLevel2[] => {
  return primaryEmotion.level2Emotions;
};
