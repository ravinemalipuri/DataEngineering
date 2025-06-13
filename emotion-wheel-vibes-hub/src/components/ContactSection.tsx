
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Mail, MessageCircle, Heart } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface ContactSectionProps {
  language: string;
}

const ContactSection: React.FC<ContactSectionProps> = ({ language }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate form submission
    toast({
      title: language === 'en' ? 'Message Sent!' : 'సందేశం పంపబడింది!',
      description: language === 'en' 
        ? 'Thank you for your feedback. We will get back to you soon.'
        : 'మీ అభిప్రాయానికి ధన్యవాదాలు. మేము త్వరలో మీకు తిరిగి వస్తాము.',
    });
    setFormData({ name: '', email: '', message: '' });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <section id="contact" className="py-20 bg-gradient-to-br from-accent/10 to-primary/5">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-playfair font-bold mb-6">
            {language === 'en' ? 'Get in Touch' : 'సంప్రదించండి'}
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            {language === 'en'
              ? 'Have questions, feedback, or want to share your experience with the Emotion Wheel? We would love to hear from you.'
              : 'ప్రశ్నలు, అభిప్రాయాలు లేదా భావోద్వేగ చక్రంతో మీ అనుభవాన్ని పంచుకోవాలనుకుంటున్నారా? మేము మీ నుండి వినాలని అనుకుంటున్నాము.'
            }
          </p>
        </div>

        <div className="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Form */}
          <Card className="p-8">
            <div className="flex items-center mb-6">
              <MessageCircle className="w-6 h-6 text-primary mr-3" />
              <h3 className="text-xl font-playfair font-semibold">
                {language === 'en' ? 'Send us a message' : 'మాకు సందేశం పంపండి'}
              </h3>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium mb-2">
                  {language === 'en' ? 'Name' : 'పేరు'}
                </label>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder={language === 'en' ? 'Your name' : 'మీ పేరు'}
                  required
                />
              </div>
              
              <div>
                <label htmlFor="email" className="block text-sm font-medium mb-2">
                  {language === 'en' ? 'Email' : 'ఇమెయిల్'}
                </label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder={language === 'en' ? 'your@email.com' : 'మీ@ఇమెయిల్.com'}
                  required
                />
              </div>
              
              <div>
                <label htmlFor="message" className="block text-sm font-medium mb-2">
                  {language === 'en' ? 'Message' : 'సందేశం'}
                </label>
                <Textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  placeholder={language === 'en' ? 'Your message...' : 'మీ సందేశం...'}
                  rows={5}
                  required
                />
              </div>
              
              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-emotion-joy to-emotion-anticipation hover:from-emotion-trust hover:to-emotion-joy transition-all duration-300"
              >
                {language === 'en' ? 'Send Message' : 'సందేశం పంపండి'}
                <Mail className="ml-2 w-4 h-4" />
              </Button>
            </form>
          </Card>

          {/* Contact Info */}
          <div className="space-y-8">
            <Card className="p-8">
              <div className="flex items-center mb-4">
                <Heart className="w-6 h-6 text-primary mr-3" />
                <h3 className="text-xl font-playfair font-semibold">
                  {language === 'en' ? 'About This Project' : 'ఈ ప్రాజెక్ట్ గురించి'}
                </h3>
              </div>
              <p className="text-muted-foreground leading-relaxed">
                {language === 'en'
                  ? 'This interactive Emotion Wheel is designed to help people better understand and navigate their emotional experiences. Built with accessibility and multilingual support in mind.'
                  : 'ఈ ఇంటరాక్టివ్ భావోద్వేగ చక్రం వ్యక్తులు వారి భావోద్వేగ అనుభవాలను బాగా అర్థం చేసుకోవడంలో మరియు నావిగేట్ చేయడంలో సహాయపడటానికి రూపొందించబడింది. ప్రాప్యత మరియు బహుభాషా మద్దతును దృష్టిలో ఉంచుకుని నిర్మించబడింది.'
                }
              </p>
            </Card>

            <Card className="p-8">
              <h3 className="text-xl font-playfair font-semibold mb-4">
                {language === 'en' ? 'Features' : 'లక్షణాలు'}
              </h3>
              <ul className="space-y-3">
                {[
                  language === 'en' ? 'Interactive emotion exploration' : 'ఇంటరాక్టివ్ భావోద్వేగ అన్వేషణ',
                  language === 'en' ? 'Multilingual support (EN/TE)' : 'బహుభాషా మద్దతు (EN/TE)',
                  language === 'en' ? 'Mobile-responsive design' : 'మొబైల్-రెస్పాన్సివ్ డిజైన్',
                  language === 'en' ? 'Accessibility focused' : 'ప్రాప్యత కేంద్రీకృత',
                  language === 'en' ? 'Open-source technology' : 'ఓపెన్-సోర్స్ టెక్నాలజీ'
                ].map((feature, index) => (
                  <li key={index} className="flex items-center">
                    <div className="w-2 h-2 bg-primary rounded-full mr-3"></div>
                    <span className="text-muted-foreground">{feature}</span>
                  </li>
                ))}
              </ul>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;
