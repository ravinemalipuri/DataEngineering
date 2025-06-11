
export interface EmotionLevel3Telugu {
  id: string;
  nameTelugu: string;
}

export interface EmotionLevel2Telugu {
  id: string;
  nameTelugu: string;
  level3Emotions: EmotionLevel3Telugu[];
}

export interface EmotionLevel1Telugu {
  id: string;
  nameTelugu: string;
  color: string;
  angle: number;
  level2Emotions: EmotionLevel2Telugu[];
}

export const emotionsDataTelugu: EmotionLevel1Telugu[] = [
  {
    id: 'happy',
    nameTelugu: 'సంతోషం',
    color: '#FFD700',
    angle: 0,
    level2Emotions: [
      {
        id: 'playful',
        nameTelugu: 'ఉల్లాసభరితమైన',
        level3Emotions: [
          { id: 'aroused', nameTelugu: 'రెచ్చిపోయింది' },
          { id: 'cheeky', nameTelugu: 'కొంటెయైన' }
        ]
      },
      {
        id: 'content',
        nameTelugu: 'నిమ్మళముగా',
        level3Emotions: [
          { id: 'free', nameTelugu: 'ఉచిత' },
          { id: 'joyful', nameTelugu: 'సంతోషకరమైన' }
        ]
      },
      {
        id: 'interested',
        nameTelugu: 'ఆసక్తి',
        level3Emotions: [
          { id: 'curious', nameTelugu: 'ఉత్సుకత' },
          { id: 'inquisitive', nameTelugu: 'ఆసక్తిగల' }
        ]
      },
      {
        id: 'proud',
        nameTelugu: 'గర్వంగా ఉంది',
        level3Emotions: [
          { id: 'successful', nameTelugu: 'విజయవంతమైంది' },
          { id: 'confident', nameTelugu: 'నమ్మకంగా' }
        ]
      },
      {
        id: 'accepted',
        nameTelugu: 'అంగీకరించబడింది',
        level3Emotions: [
          { id: 'respected', nameTelugu: 'గౌరవించారు' },
          { id: 'valued', nameTelugu: 'విలువైనది' }
        ]
      },
      {
        id: 'powerful',
        nameTelugu: 'శక్తివంతమైన',
        level3Emotions: [
          { id: 'courageous', nameTelugu: 'ధైర్యవంతుడు' },
          { id: 'creative', nameTelugu: 'సృజనాత్మకమైనది' }
        ]
      },
      {
        id: 'peaceful',
        nameTelugu: 'శాంతియుతమైనది',
        level3Emotions: [
          { id: 'loving', nameTelugu: 'ప్రేమించే' },
          { id: 'thankful', nameTelugu: 'ధన్యవాదములు' }
        ]
      },
      {
        id: 'trusting',
        nameTelugu: 'విశ్వసించడం',
        level3Emotions: [
          { id: 'sensitive', nameTelugu: 'సున్నితమైన' },
          { id: 'intimate', nameTelugu: 'సన్నిహితుడు' }
        ]
      },
      {
        id: 'optimistic',
        nameTelugu: 'ఆశావాది',
        level3Emotions: [
          { id: 'hopeful', nameTelugu: 'ఆశాజనకంగా' },
          { id: 'inspired', nameTelugu: 'ప్రేరణ పొందింది' }
        ]
      }
    ]
  },
  {
    id: 'sad',
    nameTelugu: 'విచారకరం',
    color: '#4682B4',
    angle: 45,
    level2Emotions: [
      {
        id: 'lonely',
        nameTelugu: 'ఒంటరి',
        level3Emotions: [
          { id: 'isolated', nameTelugu: 'ఒంటరిగా' },
          { id: 'abandoned', nameTelugu: 'విడిచిపెట్టారు' }
        ]
      },
      {
        id: 'vulnerable',
        nameTelugu: 'దుర్బలమైనది',
        level3Emotions: [
          { id: 'victimised', nameTelugu: 'బాధితులయ్యారు' },
          { id: 'fragile', nameTelugu: 'పెళుసుగా' }
        ]
      },
      {
        id: 'despair',
        nameTelugu: 'నిరాశ',
        level3Emotions: [
          { id: 'grief', nameTelugu: 'దుఃఖం' },
          { id: 'powerless', nameTelugu: 'శక్తిలేని' }
        ]
      },
      {
        id: 'guilty',
        nameTelugu: 'దోషి',
        level3Emotions: [
          { id: 'ashamed', nameTelugu: 'సిగ్గుపడింది' },
          { id: 'remorseful', nameTelugu: 'పశ్చాత్తాపపడుతుంది' }
        ]
      },
      {
        id: 'depressed',
        nameTelugu: 'అణగారిన',
        level3Emotions: [
          { id: 'inferior', nameTelugu: 'నాసిరకం' },
          { id: 'empty', nameTelugu: 'ఖాళీ' }
        ]
      },
      {
        id: 'hurt',
        nameTelugu: 'హర్ట్',
        level3Emotions: [
          { id: 'embarrassed', nameTelugu: 'సంకటపడే' },
          { id: 'disappointed', nameTelugu: 'నిరాశ చెందారు' }
        ]
      }
    ]
  },
  {
    id: 'disgusted',
    nameTelugu: 'అసహ్యం',
    color: '#9ACD32',
    angle: 90,
    level2Emotions: [
      {
        id: 'disapproving',
        nameTelugu: 'నిరాకరించడం',
        level3Emotions: [
          { id: 'judgemental', nameTelugu: 'జడ్జిమెంటల్' },
          { id: 'embarrassed-disgust', nameTelugu: 'సిగ్గుపడింది' }
        ]
      },
      {
        id: 'disappointed-disgust',
        nameTelugu: 'నిరాశ చెందారు',
        level3Emotions: [
          { id: 'appalled', nameTelugu: 'దిగ్భ్రాంతి చెందాడు' },
          { id: 'revolted', nameTelugu: 'తిరుగుబాటు చేశారు' }
        ]
      },
      {
        id: 'awful',
        nameTelugu: 'భయంకరం',
        level3Emotions: [
          { id: 'nauseated', nameTelugu: 'వికారం' },
          { id: 'detestable', nameTelugu: 'అసహ్యకరమైన' }
        ]
      },
      {
        id: 'repelled',
        nameTelugu: 'తిప్పికొట్టారు',
        level3Emotions: [
          { id: 'horrified', nameTelugu: 'భీతిల్లింది' },
          { id: 'hesitant', nameTelugu: 'సంశయం' }
        ]
      }
    ]
  },
  {
    id: 'angry',
    nameTelugu: 'కోపంగా',
    color: '#DC143C',
    angle: 135,
    level2Emotions: [
      {
        id: 'let-down',
        nameTelugu: 'లెట్ డౌన్',
        level3Emotions: [
          { id: 'betrayed', nameTelugu: 'ద్రోహం చేశారు' },
          { id: 'resentful', nameTelugu: 'ఆగ్రహంతో' }
        ]
      },
      {
        id: 'humiliated',
        nameTelugu: 'అవమానపరిచారు',
        level3Emotions: [
          { id: 'disrespected', nameTelugu: 'అగౌరవపరిచారు' },
          { id: 'ridiculed', nameTelugu: 'ఎగతాళి చేశారు' }
        ]
      },
      {
        id: 'bitter',
        nameTelugu: 'చేదు',
        level3Emotions: [
          { id: 'indignant', nameTelugu: 'ఆగ్రహంతో' },
          { id: 'violated', nameTelugu: 'ఉల్లంఘించారు' }
        ]
      },
      {
        id: 'mad',
        nameTelugu: 'పిచ్చి',
        level3Emotions: [
          { id: 'furious', nameTelugu: 'కోపంతో' },
          { id: 'jealous', nameTelugu: 'అసూయ' }
        ]
      },
      {
        id: 'aggressive',
        nameTelugu: 'దూకుడు',
        level3Emotions: [
          { id: 'provoked', nameTelugu: 'రెచ్చిపోయారు' },
          { id: 'hostile', nameTelugu: 'శత్రుత్వం' }
        ]
      },
      {
        id: 'frustrated',
        nameTelugu: 'విసుగు చెందారు',
        level3Emotions: [
          { id: 'infuriated', nameTelugu: 'చిరచిరలాడడ' },
          { id: 'annoyed', nameTelugu: 'చిరాకు' }
        ]
      },
      {
        id: 'distant',
        nameTelugu: 'దూరం',
        level3Emotions: [
          { id: 'withdrawn', nameTelugu: 'ఉపసంహరించుకున్నారు' },
          { id: 'numb', nameTelugu: 'తిమ్మిరి' }
        ]
      },
      {
        id: 'critical',
        nameTelugu: 'క్లిష్టమైన',
        level3Emotions: [
          { id: 'sceptical', nameTelugu: 'సందేహాస్పదమైనది' },
          { id: 'dismissive', nameTelugu: 'నిరాకరణ' }
        ]
      }
    ]
  },
  {
    id: 'fearful',
    nameTelugu: 'భయంగా',
    color: '#9370DB',
    angle: 180,
    level2Emotions: [
      {
        id: 'scared',
        nameTelugu: 'భయపడ్డాను',
        level3Emotions: [
          { id: 'helpless', nameTelugu: 'నిస్సహాయుడు' },
          { id: 'frightened', nameTelugu: 'భయపడ్డాను' }
        ]
      },
      {
        id: 'anxious',
        nameTelugu: 'ఆత్రుత',
        level3Emotions: [
          { id: 'overwhelmed-fear', nameTelugu: 'పొంగిపోయింది' },
          { id: 'worried', nameTelugu: 'ఆందోళన చెందారు' }
        ]
      },
      {
        id: 'insecure',
        nameTelugu: 'అభద్రత',
        level3Emotions: [
          { id: 'inadequate', nameTelugu: 'సరిపోదు' },
          { id: 'inferior-fear', nameTelugu: 'నాసిరకం' }
        ]
      },
      {
        id: 'weak',
        nameTelugu: 'బలహీనమైనది',
        level3Emotions: [
          { id: 'worthless', nameTelugu: 'విలువలేనిది' },
          { id: 'insignificant', nameTelugu: 'అప్రధానమైనది' }
        ]
      },
      {
        id: 'rejected',
        nameTelugu: 'తిరస్కరించబడింది',
        level3Emotions: [
          { id: 'excluded', nameTelugu: 'మినహాయించబడింది' },
          { id: 'persecuted', nameTelugu: 'పీడించబడ్డాడు' }
        ]
      },
      {
        id: 'threatened',
        nameTelugu: 'బెదిరించారు',
        level3Emotions: [
          { id: 'nervous', nameTelugu: 'నాడీ' },
          { id: 'exposed', nameTelugu: 'బహిర్గతమైంది' }
        ]
      }
    ]
  },
  {
    id: 'bad',
    nameTelugu: 'చెడ్డది',
    color: '#808080',
    angle: 225,
    level2Emotions: [
      {
        id: 'bored',
        nameTelugu: 'బోర్ కొట్టింది',
        level3Emotions: [
          { id: 'indifferent', nameTelugu: 'ఉదాసీనం' },
          { id: 'apathetic', nameTelugu: 'విరక్తి' }
        ]
      },
      {
        id: 'busy',
        nameTelugu: 'బిజీ',
        level3Emotions: [
          { id: 'pressured', nameTelugu: 'ఒత్తిడి చేశారు' },
          { id: 'rushed', nameTelugu: 'పరుగెత్తింది' }
        ]
      },
      {
        id: 'stressed',
        nameTelugu: 'ఒత్తిడికి లోనయ్యారు',
        level3Emotions: [
          { id: 'overwhelmed-bad', nameTelugu: 'పొంగిపోయింది' },
          { id: 'out-of-control', nameTelugu: 'అదుపు తప్పింది' }
        ]
      },
      {
        id: 'tired',
        nameTelugu: 'అలసిపోయింది',
        level3Emotions: [
          { id: 'sleepy', nameTelugu: 'నిద్ర పోతున్నది' },
          { id: 'unfocused', nameTelugu: 'దృష్టి పెట్టలేదు' }
        ]
      }
    ]
  },
  {
    id: 'surprised',
    nameTelugu: 'ఆశ్చర్యపోయాను',
    color: '#FF6347',
    angle: 270,
    level2Emotions: [
      {
        id: 'startled',
        nameTelugu: 'స్టార్డ్',
        level3Emotions: [
          { id: 'shocked', nameTelugu: 'షాక్ అయ్యాను' },
          { id: 'dismayed', nameTelugu: 'విస్తుపోయారు' }
        ]
      },
      {
        id: 'confused',
        nameTelugu: 'అయోమయంలో పడ్డారు',
        level3Emotions: [
          { id: 'disillusioned', nameTelugu: 'భ్రమపడ్డాడు' },
          { id: 'perplexed', nameTelugu: 'ప్రీప్లెక్స్డ్' }
        ]
      },
      {
        id: 'amazed',
        nameTelugu: 'ఆశ్చర్యపోయాడు',
        level3Emotions: [
          { id: 'astonished', nameTelugu: 'ఆశ్చర్యపోయాడు' },
          { id: 'awe', nameTelugu: 'విస్మయం' }
        ]
      },
      {
        id: 'excited',
        nameTelugu: 'నిష్క్రమించారు',
        level3Emotions: [
          { id: 'eager', nameTelugu: 'ఆత్రుత' },
          { id: 'energetic', nameTelugu: 'ఎనర్జిటిక్' }
        ]
      }
    ]
  }
];
