
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import Navigation from '@/components/Navigation';
import FeaturesSection from '@/components/FeaturesSection';
import StandaloneFeelingsJournal from '@/components/StandaloneFeelingsJournal';
import EmotionTracker from '@/components/EmotionTracker';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Language } from '@/translations';
import { LogIn, LogOut, Heart } from 'lucide-react';

const Index = () => {
  const { user, signOut, loading } = useAuth();
  const navigate = useNavigate();
  const [currentLanguage, setCurrentLanguage] = useState<Language>('en');

  useEffect(() => {
    // Get browser language or use saved preference if available
    const savedLanguage = localStorage.getItem('preferred-language');
    if (savedLanguage && ['en', 'te', 'es', 'ta'].includes(savedLanguage)) {
      setCurrentLanguage(savedLanguage as Language);
    } else {
      // Try to detect browser language
      const browserLang = navigator.language.split('-')[0];
      if (['en', 'te', 'es', 'ta'].includes(browserLang)) {
        setCurrentLanguage(browserLang as Language);
      }
    }
    
    document.documentElement.lang = currentLanguage;
  }, []);

  const handleLanguageChange = (lang: Language) => {
    setCurrentLanguage(lang);
    document.documentElement.lang = lang;
    // Save preference
    localStorage.setItem('preferred-language', lang);
  };

  const handleSignOut = async () => {
    await signOut();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Heart className="h-8 w-8 text-primary mx-auto mb-4 animate-pulse" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background font-inter">
      <Navigation 
        currentLanguage={currentLanguage} 
        onLanguageChange={handleLanguageChange} 
      />
      
      {/* Auth Section */}
      <div className="pt-16 bg-muted/30">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Heart className="h-6 w-6 text-primary" />
              <h1 className="text-2xl font-bold">My Feelings Journey</h1>
            </div>
            <div className="flex items-center gap-2">
              {user ? (
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">
                    Welcome, {user.email}
                  </span>
                  <Button variant="outline" onClick={handleSignOut}>
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign Out
                  </Button>
                </div>
              ) : (
                <Button onClick={() => navigate('/auth')}>
                  <LogIn className="mr-2 h-4 w-4" />
                  Sign In
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
      
      <main>
        {user ? (
          /* Authenticated User - Show Emotion Tracker */
          <section className="py-8">
            <div className="container mx-auto px-4">
              <EmotionTracker />
            </div>
          </section>
        ) : (
          /* Non-authenticated - Show Demo/Info */
          <section className="py-16">
            <div className="container mx-auto px-4 text-center">
              <Card className="max-w-md mx-auto">
                <CardHeader>
                  <CardTitle>Welcome to Your Feelings Journey</CardTitle>
                  <CardDescription>
                    Track and understand your emotions over time. Sign in to start recording your feelings.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button onClick={() => navigate('/auth')} className="w-full">
                    Get Started
                  </Button>
                </CardContent>
              </Card>
            </div>
          </section>
        )}
        
        <FeaturesSection language={currentLanguage} />
        
        {/* Standalone Feelings Journal Section */}
        <section className="py-16 bg-muted/50">
          <div className="container mx-auto px-4">
            <StandaloneFeelingsJournal language={currentLanguage} />
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;
