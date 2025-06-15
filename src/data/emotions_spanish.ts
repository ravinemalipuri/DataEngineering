
export interface EmotionLevel3Spanish {
  id: string;
  nameSpanish: string;
}

export interface EmotionLevel2Spanish {
  id: string;
  nameSpanish: string;
  level3Emotions: EmotionLevel3Spanish[];
}

export interface EmotionLevel1Spanish {
  id: string;
  nameSpanish: string;
  color: string;
  angle: number;
  level2Emotions: EmotionLevel2Spanish[];
}

export const emotionsDataSpanish: EmotionLevel1Spanish[] = [
  {
    id: 'happy',
    nameSpanish: 'Feliz',
    color: '#FFD700',
    angle: 0,
    level2Emotions: [
      {
        id: 'playful',
        nameSpanish: 'Juguetón',
        level3Emotions: [
          { id: 'aroused', nameSpanish: 'Excitado' },
          { id: 'cheeky', nameSpanish: 'Travieso' }
        ]
      },
      {
        id: 'content',
        nameSpanish: 'Contento',
        level3Emotions: [
          { id: 'free', nameSpanish: 'Libre' },
          { id: 'joyful', nameSpanish: 'Alegre' }
        ]
      },
      {
        id: 'interested',
        nameSpanish: 'Interesado',
        level3Emotions: [
          { id: 'curious', nameSpanish: 'Curioso' },
          { id: 'inquisitive', nameSpanish: 'Inquisitivo' }
        ]
      },
      {
        id: 'proud',
        nameSpanish: 'Orgulloso',
        level3Emotions: [
          { id: 'successful', nameSpanish: 'Exitoso' },
          { id: 'confident', nameSpanish: 'Confiado' }
        ]
      },
      {
        id: 'accepted',
        nameSpanish: 'Aceptado',
        level3Emotions: [
          { id: 'respected', nameSpanish: 'Respetado' },
          { id: 'valued', nameSpanish: 'Valorado' }
        ]
      },
      {
        id: 'powerful',
        nameSpanish: 'Poderoso',
        level3Emotions: [
          { id: 'courageous', nameSpanish: 'Valiente' },
          { id: 'creative', nameSpanish: 'Creativo' }
        ]
      },
      {
        id: 'peaceful',
        nameSpanish: 'Pacífico',
        level3Emotions: [
          { id: 'loving', nameSpanish: 'Amoroso' },
          { id: 'thankful', nameSpanish: 'Agradecido' }
        ]
      },
      {
        id: 'trusting',
        nameSpanish: 'Confiando',
        level3Emotions: [
          { id: 'sensitive', nameSpanish: 'Sensible' },
          { id: 'intimate', nameSpanish: 'Íntimo' }
        ]
      },
      {
        id: 'optimistic',
        nameSpanish: 'Optimista',
        level3Emotions: [
          { id: 'hopeful', nameSpanish: 'Esperanzado' },
          { id: 'inspired', nameSpanish: 'Inspirado' }
        ]
      }
    ]
  },
  {
    id: 'sad',
    nameSpanish: 'Triste',
    color: '#4682B4',
    angle: 45,
    level2Emotions: [
      {
        id: 'lonely',
        nameSpanish: 'Solitario',
        level3Emotions: [
          { id: 'isolated', nameSpanish: 'Aislado' },
          { id: 'abandoned', nameSpanish: 'Abandonado' }
        ]
      },
      {
        id: 'vulnerable',
        nameSpanish: 'Vulnerable',
        level3Emotions: [
          { id: 'victimised', nameSpanish: 'Victimizado' },
          { id: 'fragile', nameSpanish: 'Frágil' }
        ]
      },
      {
        id: 'despair',
        nameSpanish: 'Desesperación',
        level3Emotions: [
          { id: 'grief', nameSpanish: 'Dolor' },
          { id: 'powerless', nameSpanish: 'Impotente' }
        ]
      },
      {
        id: 'guilty',
        nameSpanish: 'Culpable',
        level3Emotions: [
          { id: 'ashamed', nameSpanish: 'Avergonzado' },
          { id: 'remorseful', nameSpanish: 'Arrepentido' }
        ]
      },
      {
        id: 'depressed',
        nameSpanish: 'Deprimido',
        level3Emotions: [
          { id: 'inferior', nameSpanish: 'Inferior' },
          { id: 'empty', nameSpanish: 'Vacío' }
        ]
      },
      {
        id: 'hurt',
        nameSpanish: 'Herido',
        level3Emotions: [
          { id: 'embarrassed', nameSpanish: 'Avergonzado' },
          { id: 'disappointed', nameSpanish: 'Decepcionado' }
        ]
      }
    ]
  },
  {
    id: 'disgusted',
    nameSpanish: 'Disgustado',
    color: '#9ACD32',
    angle: 90,
    level2Emotions: [
      {
        id: 'disapproving',
        nameSpanish: 'Desaprobando',
        level3Emotions: [
          { id: 'judgemental', nameSpanish: 'Crítico' },
          { id: 'embarrassed-disgust', nameSpanish: 'Avergonzado' }
        ]
      },
      {
        id: 'disappointed-disgust',
        nameSpanish: 'Decepcionado',
        level3Emotions: [
          { id: 'appalled', nameSpanish: 'Horrorizado' },
          { id: 'revolted', nameSpanish: 'Repugnado' }
        ]
      },
      {
        id: 'awful',
        nameSpanish: 'Horrible',
        level3Emotions: [
          { id: 'nauseated', nameSpanish: 'Nauseado' },
          { id: 'detestable', nameSpanish: 'Detestable' }
        ]
      },
      {
        id: 'repelled',
        nameSpanish: 'Repelido',
        level3Emotions: [
          { id: 'horrified', nameSpanish: 'Horrorizado' },
          { id: 'hesitant', nameSpanish: 'Vacilante' }
        ]
      }
    ]
  },
  {
    id: 'angry',
    nameSpanish: 'Enojado',
    color: '#DC143C',
    angle: 135,
    level2Emotions: [
      {
        id: 'let-down',
        nameSpanish: 'Decepcionado',
        level3Emotions: [
          { id: 'betrayed', nameSpanish: 'Traicionado' },
          { id: 'resentful', nameSpanish: 'Resentido' }
        ]
      },
      {
        id: 'humiliated',
        nameSpanish: 'Humillado',
        level3Emotions: [
          { id: 'disrespected', nameSpanish: 'Irrespetado' },
          { id: 'ridiculed', nameSpanish: 'Ridiculizado' }
        ]
      },
      {
        id: 'bitter',
        nameSpanish: 'Amargado',
        level3Emotions: [
          { id: 'indignant', nameSpanish: 'Indignado' },
          { id: 'violated', nameSpanish: 'Violado' }
        ]
      },
      {
        id: 'mad',
        nameSpanish: 'Loco',
        level3Emotions: [
          { id: 'furious', nameSpanish: 'Furioso' },
          { id: 'jealous', nameSpanish: 'Celoso' }
        ]
      },
      {
        id: 'aggressive',
        nameSpanish: 'Agresivo',
        level3Emotions: [
          { id: 'provoked', nameSpanish: 'Provocado' },
          { id: 'hostile', nameSpanish: 'Hostil' }
        ]
      },
      {
        id: 'frustrated',
        nameSpanish: 'Frustrado',
        level3Emotions: [
          { id: 'infuriated', nameSpanish: 'Enfurecido' },
          { id: 'annoyed', nameSpanish: 'Molesto' }
        ]
      },
      {
        id: 'distant',
        nameSpanish: 'Distante',
        level3Emotions: [
          { id: 'withdrawn', nameSpanish: 'Retraído' },
          { id: 'numb', nameSpanish: 'Entumecido' }
        ]
      },
      {
        id: 'critical',
        nameSpanish: 'Crítico',
        level3Emotions: [
          { id: 'sceptical', nameSpanish: 'Escéptico' },
          { id: 'dismissive', nameSpanish: 'Desdeñoso' }
        ]
      }
    ]
  },
  {
    id: 'fearful',
    nameSpanish: 'Temeroso',
    color: '#9370DB',
    angle: 180,
    level2Emotions: [
      {
        id: 'scared',
        nameSpanish: 'Asustado',
        level3Emotions: [
          { id: 'helpless', nameSpanish: 'Indefenso' },
          { id: 'frightened', nameSpanish: 'Asustado' }
        ]
      },
      {
        id: 'anxious',
        nameSpanish: 'Ansioso',
        level3Emotions: [
          { id: 'overwhelmed-fear', nameSpanish: 'Abrumado' },
          { id: 'worried', nameSpanish: 'Preocupado' }
        ]
      },
      {
        id: 'insecure',
        nameSpanish: 'Inseguro',
        level3Emotions: [
          { id: 'inadequate', nameSpanish: 'Inadecuado' },
          { id: 'inferior-fear', nameSpanish: 'Inferior' }
        ]
      },
      {
        id: 'weak',
        nameSpanish: 'Débil',
        level3Emotions: [
          { id: 'worthless', nameSpanish: 'Sin valor' },
          { id: 'insignificant', nameSpanish: 'Insignificante' }
        ]
      },
      {
        id: 'rejected',
        nameSpanish: 'Rechazado',
        level3Emotions: [
          { id: 'excluded', nameSpanish: 'Excluido' },
          { id: 'persecuted', nameSpanish: 'Perseguido' }
        ]
      },
      {
        id: 'threatened',
        nameSpanish: 'Amenazado',
        level3Emotions: [
          { id: 'nervous', nameSpanish: 'Nervioso' },
          { id: 'exposed', nameSpanish: 'Expuesto' }
        ]
      }
    ]
  },
  {
    id: 'bad',
    nameSpanish: 'Malo',
    color: '#808080',
    angle: 225,
    level2Emotions: [
      {
        id: 'bored',
        nameSpanish: 'Aburrido',
        level3Emotions: [
          { id: 'indifferent', nameSpanish: 'Indiferente' },
          { id: 'apathetic', nameSpanish: 'Apático' }
        ]
      },
      {
        id: 'busy',
        nameSpanish: 'Ocupado',
        level3Emotions: [
          { id: 'pressured', nameSpanish: 'Presionado' },
          { id: 'rushed', nameSpanish: 'Apurado' }
        ]
      },
      {
        id: 'stressed',
        nameSpanish: 'Estresado',
        level3Emotions: [
          { id: 'overwhelmed-bad', nameSpanish: 'Abrumado' },
          { id: 'out-of-control', nameSpanish: 'Fuera de control' }
        ]
      },
      {
        id: 'tired',
        nameSpanish: 'Cansado',
        level3Emotions: [
          { id: 'sleepy', nameSpanish: 'Somnoliento' },
          { id: 'unfocused', nameSpanish: 'Desenfocado' }
        ]
      }
    ]
  },
  {
    id: 'surprised',
    nameSpanish: 'Sorprendido',
    color: '#FF6347',
    angle: 270,
    level2Emotions: [
      {
        id: 'startled',
        nameSpanish: 'Sobresaltado',
        level3Emotions: [
          { id: 'shocked', nameSpanish: 'Conmocionado' },
          { id: 'dismayed', nameSpanish: 'Consternado' }
        ]
      },
      {
        id: 'confused',
        nameSpanish: 'Confundido',
        level3Emotions: [
          { id: 'disillusioned', nameSpanish: 'Desilusionado' },
          { id: 'perplexed', nameSpanish: 'Perplejo' }
        ]
      },
      {
        id: 'amazed',
        nameSpanish: 'Asombrado',
        level3Emotions: [
          { id: 'astonished', nameSpanish: 'Asombrado' },
          { id: 'awe', nameSpanish: 'Asombro' }
        ]
      },
      {
        id: 'excited',
        nameSpanish: 'Emocionado',
        level3Emotions: [
          { id: 'eager', nameSpanish: 'Ansioso' },
          { id: 'energetic', nameSpanish: 'Enérgico' }
        ]
      }
    ]
  }
];
