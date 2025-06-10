import React, { useState } from 'react';
import { emotionsData, getEmotionName, getAllLevel2Emotions, getAllLevel3Emotions, EmotionLevel1, EmotionLevel2 } from '@/data/emotions';

interface EmotionWheelProps {
  language: string;
}

const EmotionWheel: React.FC<EmotionWheelProps> = ({ language }) => {
  const [selectedEmotion, setSelectedEmotion] = useState<EmotionLevel1 | null>(null);
  const [hoveredEmotion, setHoveredEmotion] = useState<string | null>(null);

  const createEmotionSegment = (emotion: EmotionLevel1, radius: number, strokeWidth: number, intensity: number) => {
    const centerX = 200;
    const centerY = 200;
    const segmentAngle = 360 / emotionsData.length;
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

    const isHovered = hoveredEmotion === emotion.id;
    const isSelected = selectedEmotion?.id === emotion.id;
    
    // Calculate text position and rotation for radial alignment
    const textRadius = radius - strokeWidth / 2;
    const textAngle = emotion.angle;
    const textAngleRad = (textAngle * Math.PI) / 180;
    const textX = centerX + textRadius * Math.cos(textAngleRad);
    const textY = centerY + textRadius * Math.sin(textAngleRad);
    
    // Determine text rotation - keep text readable by avoiding upside-down text
    let textRotation = textAngle;
    if (textAngle > 90 && textAngle < 270) {
      textRotation = textAngle + 180;
    }
    
    return (
      <g key={`${emotion.id}-${intensity}`}>
        <path
          d={pathData}
          fill={emotion.color}
          fillOpacity={intensity + (isHovered ? 0.2 : 0)}
          stroke="white"
          strokeWidth="1"
          className={`transition-all duration-300 cursor-pointer ${isSelected ? 'drop-shadow-lg' : ''}`}
          onMouseEnter={() => setHoveredEmotion(emotion.id)}
          onMouseLeave={() => setHoveredEmotion(null)}
          onClick={() => setSelectedEmotion(selectedEmotion?.id === emotion.id ? null : emotion)}
        />
        {intensity === 1 && (
          <text
            x={textX}
            y={textY}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="white"
            fontSize="11"
            fontWeight="700"
            className="pointer-events-none font-inter"
            style={{ textShadow: '1px 1px 2px rgba(0,0,0,0.8)' }}
            transform={`rotate(${textRotation} ${textX} ${textY})`}
          >
            {getEmotionName(emotion, language as 'en' | 'te')}
          </text>
        )}
      </g>
    );
  };

  return (
    <div className="flex flex-col items-center space-y-8">
      <div className="relative">
        <svg width="400" height="400" viewBox="0 0 400 400" className="w-full max-w-lg">
          {/* Outer ring - Level 3 emotions */}
          {emotionsData.map(emotion => createEmotionSegment(emotion, 180, 60, 0.4))}
          
          {/* Middle ring - Level 2 emotions */}
          {emotionsData.map(emotion => createEmotionSegment(emotion, 120, 40, 0.7))}
          
          {/* Inner ring - Primary emotions */}
          {emotionsData.map(emotion => createEmotionSegment(emotion, 80, 40, 1))}
          
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
            {getEmotionName(selectedEmotion, language as 'en' | 'te')}
          </h3>
          
          <div className="space-y-3">
            <div>
              <h4 className="font-semibold text-sm text-muted-foreground mb-2">
                {language === 'en' ? 'Secondary Emotions:' : 'ద్వితీయ భావనలు:'}
              </h4>
              <div className="grid grid-cols-2 gap-1 text-sm">
                {getAllLevel2Emotions(selectedEmotion).map((emotion) => (
                  <span key={emotion.id} className="text-xs bg-accent/20 rounded px-2 py-1">
                    {getEmotionName(emotion, language as 'en' | 'te')}
                  </span>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-sm text-muted-foreground mb-2">
                {language === 'en' ? 'Detailed Emotions:' : 'వివరణాత్మక భావనలు:'}
              </h4>
              <div className="grid grid-cols-2 gap-1 text-sm">
                {getAllLevel3Emotions(selectedEmotion).map((emotion) => (
                  <span key={emotion.id} className="text-xs bg-primary/10 rounded px-2 py-1">
                    {getEmotionName(emotion, language as 'en' | 'te')}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
      
      <p className="text-sm text-muted-foreground text-center max-w-md">
        {language === 'en' 
          ? 'Click on any emotion segment to explore its related feelings and understand the emotional hierarchy.'
          : 'ఏదైనా భావోద్వేగ విభాగంపై క్లిక్ చేసి దాని సంబంధిత భావాలను అన్వేషించండి మరియు భావోద్వేగ క్రమబద్ధతను అర్థం చేసుకోండి.'
        }
      </p>
    </div>
  );
};

export default EmotionWheel;
