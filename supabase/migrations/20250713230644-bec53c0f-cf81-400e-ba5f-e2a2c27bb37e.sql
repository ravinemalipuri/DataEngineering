-- Create profiles table for user data
CREATE TABLE public.profiles (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create emotions reference table
CREATE TABLE public.emotions (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  category TEXT NOT NULL,
  color_hex TEXT DEFAULT '#6B7280',
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create emotion entries table for user's emotion records
CREATE TABLE public.emotion_entries (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  emotion_ids UUID[] NOT NULL,
  intensity INTEGER CHECK (intensity >= 1 AND intensity <= 10),
  note TEXT,
  recorded_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.emotions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.emotion_entries ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Profiles are viewable by owner" 
ON public.profiles 
FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own profile" 
ON public.profiles 
FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own profile" 
ON public.profiles 
FOR UPDATE 
USING (auth.uid() = user_id);

-- Emotions policies (readable by authenticated users)
CREATE POLICY "Emotions are viewable by authenticated users" 
ON public.emotions 
FOR SELECT 
TO authenticated
USING (true);

-- Emotion entries policies
CREATE POLICY "Users can view their own emotion entries" 
ON public.emotion_entries 
FOR SELECT 
USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own emotion entries" 
ON public.emotion_entries 
FOR INSERT 
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own emotion entries" 
ON public.emotion_entries 
FOR UPDATE 
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own emotion entries" 
ON public.emotion_entries 
FOR DELETE 
USING (auth.uid() = user_id);

-- Create function to update timestamps
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW
  EXECUTE FUNCTION public.update_updated_at_column();

-- Create function to handle new user signups
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (user_id, display_name)
  VALUES (NEW.id, NEW.raw_user_meta_data ->> 'display_name');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- Insert sample emotions
INSERT INTO public.emotions (name, category, color_hex) VALUES
  ('Joy', 'Primary', '#FDE047'),
  ('Sadness', 'Primary', '#3B82F6'),
  ('Anger', 'Primary', '#EF4444'),
  ('Fear', 'Primary', '#8B5CF6'),
  ('Love', 'Secondary', '#EC4899'),
  ('Surprise', 'Secondary', '#F97316'),
  ('Disgust', 'Secondary', '#84CC16'),
  ('Trust', 'Secondary', '#06B6D4'),
  ('Anticipation', 'Secondary', '#EAB308'),
  ('Shame', 'Complex', '#6B7280'),
  ('Guilt', 'Complex', '#64748B'),
  ('Pride', 'Complex', '#D97706'),
  ('Gratitude', 'Positive', '#10B981'),
  ('Hope', 'Positive', '#8B5CF6'),
  ('Contentment', 'Positive', '#059669'),
  ('Anxiety', 'Negative', '#DC2626'),
  ('Frustration', 'Negative', '#EA580C'),
  ('Loneliness', 'Negative', '#4338CA'),
  ('Confusion', 'Neutral', '#6B7280'),
  ('Curiosity', 'Neutral', '#0EA5E9');