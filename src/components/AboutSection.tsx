
import React from 'react';
import { Card } from '@/components/ui/card';
import { Lightbulb, Users, Target } from 'lucide-react';

interface AboutSectionProps {
  language: string;
}

const AboutSection: React.FC<AboutSectionProps> = ({ language }) => {
  const features = [
    {
      icon: <Lightbulb className="w-8 h-8" />,
      title: language === 'en' ? 'Understanding Emotions' : 'భావోద్వేగాలను అర్థం చేసుకోవడం',
      description: language === 'en' 
        ? 'Learn about the complex relationships between different emotions and how they influence our daily lives.'
        : 'వివిధ భావోద్వేగాల మధ్య సంక్లిష్ట సంబంధాలు మరియు అవి మన దైనందిన జీవితాన్ని ఎలా ప్రభావితం చేస్తాయో తెలుసుకోండి.'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: language === 'en' ? 'Cultural Awareness' : 'సాంస్కృతిక అవగాహన',
      description: language === 'en'
        ? 'Explore emotions across cultures with multilingual support, making emotional literacy accessible to diverse communities.'
        : 'బహుభాషా మద్దతుతో సంస్కృతుల అంతటా భావోద్వేగాలను అన్వేషించండి, వైవిధ్యమైన సమాజాలకు భావోద్వేగ అక్షరాస్యతను అందుబాటులో ఉంచండి.'
    },
    {
      icon: <Target className="w-8 h-8" />,
      title: language === 'en' ? 'Personal Growth' : 'వ్యక్తిగత అభివృద్ధి',
      description: language === 'en'
        ? 'Use this tool for self-reflection, therapy, education, or simply to better understand yourself and others.'
        : 'స్వీయ ప్రతిబింబం, చికిత్స, విద్య లేదా మిమ్మల్ని మరియు ఇతరులను బాగా అర్థం చేసుకోవడానికి ఈ సాధనాన్ని ఉపయోగించండి.'
    }
  ];

  return (
    <section id="about" className="py-20 bg-accent/5">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-playfair font-bold mb-6">
            {language === 'en' ? 'About the Emotion Wheel' : 'భావోద్వేగ చక్రం గురించి'}
          </h2>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            {language === 'en'
              ? 'The Emotion Wheel is based on psychological research that maps the spectrum of human emotions. Our interactive version helps you understand emotional relationships and develop emotional intelligence through visual exploration.'
              : 'భావోద్వేగ చక్రం మానవ భావోద్వేగాల వర్ణపటాన్ని మ్యాప్ చేసే మానసిక పరిశోధనపై ఆధారపడి ఉంటుంది. మా ఇంటరాక్టివ్ వర్షన్ మీకు భావోద్వేగ సంబంధాలను అర్థం చేసుకోవడంలో మరియు దృశ్య అన్వేషణ ద్వారా భావోద్వేగ మేధస్సును అభివృద్ధి చేయడంలో సహాయపడుతుంది.'
            }
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {features.map((feature, index) => (
            <Card key={index} className="p-8 text-center hover:shadow-lg transition-all duration-300 hover:scale-105 bg-card/50 backdrop-blur-sm">
              <div className="flex justify-center mb-4 text-primary">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-4 font-playfair">
                {feature.title}
              </h3>
              <p className="text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </Card>
          ))}
        </div>

        <div className="bg-card rounded-2xl p-8 md:p-12 border border-border">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl md:text-3xl font-playfair font-bold mb-6">
                {language === 'en' ? 'How It Works' : 'ఇది ఎలా పనిచేస్తుంది'}
              </h3>
              <div className="space-y-4">
                {[
                  {
                    step: '1',
                    title: language === 'en' ? 'Explore the Wheel' : 'చక్రాన్ని అన్వేషించండి',
                    desc: language === 'en' ? 'Click on different emotion segments to discover related feelings.' : 'సంబంధిత భావాలను కనుగొనడానికి వివిధ భావోద్వేగ విభాగాలపై క్లిక్ చేయండి.'
                  },
                  {
                    step: '2',
                    title: language === 'en' ? 'Learn Connections' : 'కనెక్షన్లను నేర్చుకోండి',
                    desc: language === 'en' ? 'Understand how emotions relate to each other in intensity and type.' : 'భావోద్వేగాలు తీవ్రత మరియు రకంలో ఒకదానితో ఒకటి ఎలా సంబంధం కలిగి ఉంటాయో అర్థం చేసుకోండి.'
                  },
                  {
                    step: '3',
                    title: language === 'en' ? 'Apply Insights' : 'అంతర్దృష్టులను వర్తింపజేయండి',
                    desc: language === 'en' ? 'Use your newfound understanding for better emotional awareness.' : 'మెరుగైన భావోద్వేగ అవగాహన కోసం మీ కొత్త అవగాహనను ఉపయోగించండి.'
                  }
                ].map((item) => (
                  <div key={item.step} className="flex items-start space-x-4">
                    <div className="flex-shrink-0 w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center font-bold text-sm">
                      {item.step}
                    </div>
                    <div>
                      <h4 className="font-semibold mb-1">{item.title}</h4>
                      <p className="text-sm text-muted-foreground">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="flex justify-center">
              <div className="relative">
                <div className="w-64 h-64 rounded-full bg-gradient-to-br from-emotion-joy via-emotion-trust via-emotion-fear via-emotion-surprise via-emotion-sadness via-emotion-disgust via-emotion-anger to-emotion-anticipation animate-wheel-rotate opacity-20"></div>
                <div className="absolute inset-8 rounded-full bg-gradient-to-br from-emotion-trust via-emotion-fear via-emotion-surprise via-emotion-sadness via-emotion-disgust via-emotion-anger via-emotion-anticipation to-emotion-joy animate-wheel-rotate opacity-30" style={{ animationDirection: 'reverse', animationDuration: '30s' }}></div>
                <div className="absolute inset-16 rounded-full bg-gradient-to-br from-emotion-fear via-emotion-surprise via-emotion-sadness via-emotion-disgust via-emotion-anger via-emotion-anticipation via-emotion-joy to-emotion-trust animate-wheel-rotate opacity-40" style={{ animationDuration: '25s' }}></div>
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-background rounded-full flex items-center justify-center border-2 border-border">
                  <span className="text-2xl">🧠</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
