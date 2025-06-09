
import React, { useState } from 'react';
import { emotionsData, translations } from '@/data/emotions';

interface EmotionWheelProps {
  language: string;
}

const EmotionWheel: React.FC<EmotionWheelProps> = ({ language }) => {
  const [selectedEmotion, setSelectedEmotion] = useState<string | null>(null);
  const [hoveredEmotion, setHoveredEmotion] = useState<string | null>(null);

  const getEmotionText = (emotionId: string, type: 'primary' | 'secondary' | 'tertiary') => {
    return translations[language]?.[emotionId]?.[type] || emotionsData.find(e => e.id === emotionId)?.[type] || '';
  };

  const createEmotionSegment = (emotion: any, radius: number, strokeWidth: number, type: 'primary' | 'secondary' | 'tertiary') => {
    const centerX = 200;
    const centerY = 200;
    const segmentAngle = 45; // 360 / 8 emotions
    const startAngle = emotion.angle - segmentAngle / 2;
    const endAngle = emotion.angle + segmentAngle / 2;
    
    const startAngleRad = (startAngle * Math.PI) / 180;
    const endAngleRad = (endAngle * Math.PI) / 180;
    
    const innerRadius = radius - strokeWidth;
    const outerRadius = radius;
    
    const x1 = centerX + innerRadius * Math.cos(startAngleRad);
    const y1 = centerY + innerRadius * Math.sin(startAngleRad);
    const x2 = centerX + outerRadius * Math.cos(startAngleRad);
    const y2 = centerY + outerRadius * Math.sin(startAngleRad);
    
    const x3 = centerX + outerRadius * Math.cos(endAngleRad);
    const y3 = centerY + outerRadius * Math.sin(endAngleRad);
    const x4 = centerX + innerRadius * Math.cos(endAngleRad);
    const y4 = centerY + innerRadius * Math.sin(endAngleRad);
    
    const largeArcFlag = segmentAngle > 180 ? 1 : 0;
    
    const pathData = [
      `M ${x1} ${y1}`,
      `L ${x2} ${y2}`,
      `A ${outerRadius} ${outerRadius} 0 ${largeArcFlag} 1 ${x3} ${y3}`,
      `L ${x4} ${y4}`,
      `A ${innerRadius} ${innerRadius} 0 ${largeArcFlag} 0 ${x1} ${y1}`,
      'Z'
    ].join(' ');

    const intensity = type === 'primary' ? 1 : type === 'secondary' ? 0.7 : 0.4;
    const isHovered = hoveredEmotion === emotion.id;
    const isSelected = selectedEmotion === emotion.id;
    
    return (
      <g key={`${emotion.id}-${type}`}>
        <path
          d={pathData}
          fill={emotion.color}
          fillOpacity={intensity + (isHovered ? 0.2 : 0)}
          stroke="white"
          strokeWidth="1"
          className={`transition-all duration-300 cursor-pointer ${isSelected ? 'drop-shadow-lg' : ''}`}
          onMouseEnter={() => setHoveredEmotion(emotion.id)}
          onMouseLeave={() => setHoveredEmotion(null)}
          onClick={() => setSelectedEmotion(selectedEmotion === emotion.id ? null : emotion.id)}
        />
        {type === 'primary' && (
          <text
            x={centerX + (radius - strokeWidth / 2) * Math.cos((emotion.angle * Math.PI) / 180)}
            y={centerY + (radius - strokeWidth / 2) * Math.sin((emotion.angle * Math.PI) / 180)}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="white"
            fontSize="12"
            fontWeight="600"
            className="pointer-events-none font-inter"
            style={{ textShadow: '1px 1px 2px rgba(0,0,0,0.7)' }}
          >
            {getEmotionText(emotion.id, 'primary')}
          </text>
        )}
      </g>
    );
  };

  return (
    <div className="flex flex-col items-center space-y-8">
      <div className="relative">
        <svg width="400" height="400" viewBox="0 0 400 400" className="w-full max-w-lg">
          {/* Outer ring - Primary emotions */}
          {emotionsData.map(emotion => createEmotionSegment(emotion, 180, 60, 'primary'))}
          
          {/* Middle ring - Secondary emotions */}
          {emotionsData.map(emotion => createEmotionSegment(emotion, 120, 40, 'secondary'))}
          
          {/* Inner ring - Tertiary emotions */}
          {emotionsData.map(emotion => createEmotionSegment(emotion, 80, 40, 'tertiary'))}
          
          {/* Center circle */}
          <circle
            cx="200"
            cy="200"
            r="40"
            fill="url(#centerGradient)"
            stroke="white"
            strokeWidth="2"
          />
          
          <defs>
            <radialGradient id="centerGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#f0f0f0" stopOpacity="0.8" />
            </radialGradient>
          </defs>
          
          <text
            x="200"
            y="200"
            textAnchor="middle"
            dominantBaseline="middle"
            fill="#333"
            fontSize="14"
            fontWeight="700"
            className="font-playfair"
          >
            {language === 'en' ? 'Emotions' : 'భావనలు'}
          </text>
        </svg>
      </div>

      {/* Emotion Details */}
      {selectedEmotion && (
        <div className="bg-card border border-border rounded-lg p-6 w-full max-w-md mx-auto animate-fade-in">
          <h3 className="text-xl font-playfair font-semibold mb-4 text-center">
            {getEmotionText(selectedEmotion, 'primary')}
          </h3>
          
          <div className="space-y-3">
            <div>
              <h4 className="font-semibold text-sm text-muted-foreground mb-1">
                {language === 'en' ? 'Secondary Emotions:' : 'ద్వితీయ భావనలు:'}
              </h4>
              <p className="text-sm">
                {getEmotionText(selectedEmotion, 'secondary').join(', ')}
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold text-sm text-muted-foreground mb-1">
                {language === 'en' ? 'Related Emotions:' : 'సంబంధిత భావనలు:'}
              </h4>
              <p className="text-sm">
                {getEmotionText(selectedEmotion, 'tertiary').join(', ')}
              </p>
            </div>
          </div>
        </div>
      )}
      
      <p className="text-sm text-muted-foreground text-center max-w-md">
        {language === 'en' 
          ? 'Click on any emotion segment to explore its related feelings and understand the spectrum of human emotions.'
          : 'ఏదైనా భావోద్వేగ విభాగంపై క్లిక్ చేసి దాని సంబంధిత భావాలను అన్వేషించండి మరియు మానవ భావోద్వేగాల వర్ణపటాన్ని అర్థం చేసుకోండి.'
        }
      </p>
    </div>
  );
};

export default EmotionWheel;
