
import React, { useState } from 'react';
import { emotionsData, getEmotionName, getAllLevel2Emotions, getAllLevel3Emotions, EmotionLevel1, EmotionLevel2, EmotionLevel3 } from '@/data/emotions';

interface EmotionWheelProps {
  language: string;
}

const EmotionWheel: React.FC<EmotionWheelProps> = ({ language }) => {
  const [selectedEmotion, setSelectedEmotion] = useState<EmotionLevel1 | null>(null);
  const [hoveredEmotion, setHoveredEmotion] = useState<string | null>(null);

  const createLevel1Segment = (emotion: EmotionLevel1) => {
    const centerX = 250;
    const centerY = 250;
    const numPrimary = emotionsData.length;
    const segmentAngle = 360 / numPrimary;
    const startAngle = emotion.angle - segmentAngle / 2;
    const endAngle = emotion.angle + segmentAngle / 2;
    
    const startAngleRad = (startAngle * Math.PI) / 180;
    const endAngleRad = (endAngle * Math.PI) / 180;
    
    const innerRadius = 50;
    const outerRadius = 100;
    
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
    
    const textRadius = (innerRadius + outerRadius) / 2;
    const textAngle = emotion.angle;
    const textAngleRad = (textAngle * Math.PI) / 180;
    const textX = centerX + textRadius * Math.cos(textAngleRad);
    const textY = centerY + textRadius * Math.sin(textAngleRad);
    
    let textRotation = textAngle;
    if (textAngle > 90 && textAngle < 270) {
      textRotation = textAngle + 180;
    }
    
    return (
      <g key={emotion.id}>
        <path
          d={pathData}
          fill={emotion.color}
          fillOpacity={0.9 + (isHovered ? 0.1 : 0)}
          stroke="white"
          strokeWidth="2"
          className={`transition-all duration-300 cursor-pointer ${isSelected ? 'drop-shadow-lg' : ''}`}
          onMouseEnter={() => setHoveredEmotion(emotion.id)}
          onMouseLeave={() => setHoveredEmotion(null)}
          onClick={() => setSelectedEmotion(selectedEmotion?.id === emotion.id ? null : emotion)}
        />
        <text
          x={textX}
          y={textY}
          textAnchor="middle"
          dominantBaseline="middle"
          fill="white"
          fontSize="12"
          fontWeight="700"
          className="pointer-events-none font-inter"
          style={{ textShadow: '1px 1px 2px rgba(0,0,0,0.8)' }}
          transform={`rotate(${textRotation} ${textX} ${textY})`}
        >
          {getEmotionName(emotion, language as 'en' | 'te')}
        </text>
      </g>
    );
  };

  const createLevel2Segments = (primaryEmotion: EmotionLevel1) => {
    const centerX = 250;
    const centerY = 250;
    const numPrimary = emotionsData.length;
    const primarySegmentAngle = 360 / numPrimary;
    const primaryStartAngle = primaryEmotion.angle - primarySegmentAngle / 2;
    
    const level2Emotions = primaryEmotion.level2Emotions;
    const numLevel2 = level2Emotions.length;
    const level2SegmentAngle = primarySegmentAngle / numLevel2;
    
    return level2Emotions.map((emotion, index) => {
      const startAngle = primaryStartAngle + (index * level2SegmentAngle);
      const endAngle = primaryStartAngle + ((index + 1) * level2SegmentAngle);
      
      const startAngleRad = (startAngle * Math.PI) / 180;
      const endAngleRad = (endAngle * Math.PI) / 180;
      
      const innerRadius = 100;
      const outerRadius = 150;
      
      const x1 = centerX + innerRadius * Math.cos(startAngleRad);
      const y1 = centerY + innerRadius * Math.sin(startAngleRad);
      const x2 = centerX + outerRadius * Math.cos(startAngleRad);
      const y2 = centerY + outerRadius * Math.sin(startAngleRad);
      
      const x3 = centerX + outerRadius * Math.cos(endAngleRad);
      const y3 = centerY + outerRadius * Math.sin(endAngleRad);
      const x4 = centerX + innerRadius * Math.cos(endAngleRad);
      const y4 = centerY + innerRadius * Math.sin(endAngleRad);
      
      const largeArcFlag = level2SegmentAngle > 180 ? 1 : 0;
      
      const pathData = [
        `M ${x1} ${y1}`,
        `L ${x2} ${y2}`,
        `A ${outerRadius} ${outerRadius} 0 ${largeArcFlag} 1 ${x3} ${y3}`,
        `L ${x4} ${y4}`,
        `A ${innerRadius} ${innerRadius} 0 ${largeArcFlag} 0 ${x1} ${y1}`,
        'Z'
      ].join(' ');

      const textRadius = (innerRadius + outerRadius) / 2;
      const textAngle = startAngle + (level2SegmentAngle / 2);
      const textAngleRad = (textAngle * Math.PI) / 180;
      const textX = centerX + textRadius * Math.cos(textAngleRad);
      const textY = centerY + textRadius * Math.sin(textAngleRad);
      
      let textRotation = textAngle;
      if (textAngle > 90 && textAngle < 270) {
        textRotation = textAngle + 180;
      }
      
      return (
        <g key={`${primaryEmotion.id}-${emotion.id}`}>
          <path
            d={pathData}
            fill={primaryEmotion.color}
            fillOpacity={0.7}
            stroke="white"
            strokeWidth="1"
            className="cursor-pointer"
          />
          <text
            x={textX}
            y={textY}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="white"
            fontSize="9"
            fontWeight="600"
            className="pointer-events-none font-inter"
            style={{ textShadow: '1px 1px 2px rgba(0,0,0,0.8)' }}
            transform={`rotate(${textRotation} ${textX} ${textY})`}
          >
            {getEmotionName(emotion, language as 'en' | 'te')}
          </text>
        </g>
      );
    });
  };

  const createLevel3Segments = (primaryEmotion: EmotionLevel1) => {
    const centerX = 250;
    const centerY = 250;
    const numPrimary = emotionsData.length;
    const primarySegmentAngle = 360 / numPrimary;
    const primaryStartAngle = primaryEmotion.angle - primarySegmentAngle / 2;
    
    const level2Emotions = primaryEmotion.level2Emotions;
    const numLevel2 = level2Emotions.length;
    const level2SegmentAngle = primarySegmentAngle / numLevel2;
    
    const allLevel3Segments: JSX.Element[] = [];
    
    level2Emotions.forEach((level2Emotion, level2Index) => {
      const level2StartAngle = primaryStartAngle + (level2Index * level2SegmentAngle);
      const level3Emotions = level2Emotion.level3Emotions;
      const numLevel3 = level3Emotions.length;
      const level3SegmentAngle = level2SegmentAngle / numLevel3;
      
      level3Emotions.forEach((emotion, level3Index) => {
        const startAngle = level2StartAngle + (level3Index * level3SegmentAngle);
        const endAngle = level2StartAngle + ((level3Index + 1) * level3SegmentAngle);
        
        const startAngleRad = (startAngle * Math.PI) / 180;
        const endAngleRad = (endAngle * Math.PI) / 180;
        
        const innerRadius = 150;
        const outerRadius = 200;
        
        const x1 = centerX + innerRadius * Math.cos(startAngleRad);
        const y1 = centerY + innerRadius * Math.sin(startAngleRad);
        const x2 = centerX + outerRadius * Math.cos(startAngleRad);
        const y2 = centerY + outerRadius * Math.sin(startAngleRad);
        
        const x3 = centerX + outerRadius * Math.cos(endAngleRad);
        const y3 = centerY + outerRadius * Math.sin(endAngleRad);
        const x4 = centerX + innerRadius * Math.cos(endAngleRad);
        const y4 = centerY + innerRadius * Math.sin(endAngleRad);
        
        const largeArcFlag = level3SegmentAngle > 180 ? 1 : 0;
        
        const pathData = [
          `M ${x1} ${y1}`,
          `L ${x2} ${y2}`,
          `A ${outerRadius} ${outerRadius} 0 ${largeArcFlag} 1 ${x3} ${y3}`,
          `L ${x4} ${y4}`,
          `A ${innerRadius} ${innerRadius} 0 ${largeArcFlag} 0 ${x1} ${y1}`,
          'Z'
        ].join(' ');

        const textRadius = (innerRadius + outerRadius) / 2;
        const textAngle = startAngle + (level3SegmentAngle / 2);
        const textAngleRad = (textAngle * Math.PI) / 180;
        const textX = centerX + textRadius * Math.cos(textAngleRad);
        const textY = centerY + textRadius * Math.sin(textAngleRad);
        
        let textRotation = textAngle;
        if (textAngle > 90 && textAngle < 270) {
          textRotation = textAngle + 180;
        }
        
        allLevel3Segments.push(
          <g key={`${primaryEmotion.id}-${level2Emotion.id}-${emotion.id}`}>
            <path
              d={pathData}
              fill={primaryEmotion.color}
              fillOpacity={0.4}
              stroke="white"
              strokeWidth="1"
              className="cursor-pointer"
            />
            <text
              x={textX}
              y={textY}
              textAnchor="middle"
              dominantBaseline="middle"
              fill="white"
              fontSize="7"
              fontWeight="500"
              className="pointer-events-none font-inter"
              style={{ textShadow: '1px 1px 2px rgba(0,0,0,0.8)' }}
              transform={`rotate(${textRotation} ${textX} ${textY})`}
            >
              {getEmotionName(emotion, language as 'en' | 'te')}
            </text>
          </g>
        );
      });
    });
    
    return allLevel3Segments;
  };

  return (
    <div className="flex flex-col items-center space-y-8">
      <div className="relative">
        <svg width="500" height="500" viewBox="0 0 500 500" className="w-full max-w-2xl">
          {/* Level 3 segments (outermost) */}
          {emotionsData.map(emotion => createLevel3Segments(emotion))}
          
          {/* Level 2 segments (middle) */}
          {emotionsData.map(emotion => createLevel2Segments(emotion))}
          
          {/* Level 1 segments (innermost) */}
          {emotionsData.map(emotion => createLevel1Segment(emotion))}
          
          {/* Center circle */}
          <circle
            cx="250"
            cy="250"
            r="50"
            fill="url(#centerGradient)"
            stroke="white"
            strokeWidth="3"
          />
          
          <defs>
            <radialGradient id="centerGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#f0f0f0" stopOpacity="0.8" />
            </radialGradient>
          </defs>
          
          <text
            x="250"
            y="250"
            textAnchor="middle"
            dominantBaseline="middle"
            fill="#333"
            fontSize="16"
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
