import { openai } from '@ai-sdk/openai';

export const runWebSearch = openai.tools.webSearchPreview({
  // optional configuration:
  searchContextSize: 'high',
  userLocation: {
    type: 'approximate',
    city: 'Amsterdam',
    region: 'Netherlands',
  },
});
