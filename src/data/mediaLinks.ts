
export interface MediaLink {
  id: string;
  title: string;
  url: string;
  type: 'youtube';
}

export const defaultMediaLinks: MediaLink[] = [
  {
    id: '1',
    title: 'Understanding Emotions',
    url: 'https://www.youtube.com/watch?v=gAMbkJk6gnE',
    type: 'youtube'
  },
  {
    id: '2',
    title: 'Emotional Intelligence',
    url: 'https://www.youtube.com/watch?v=Y7m9eNoB3NU',
    type: 'youtube'
  },
  {
    id: '3',
    title: 'Managing Emotions',
    url: 'https://www.youtube.com/watch?v=BHdBHM1FyWs',
    type: 'youtube'
  }
];

export const getYouTubeVideoId = (url: string): string | null => {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  return match && match[2].length === 11 ? match[2] : null;
};
