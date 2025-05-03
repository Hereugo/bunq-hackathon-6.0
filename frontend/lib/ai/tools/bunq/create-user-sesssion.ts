import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const createUserSession = tool({
  description: 'Create a new user session in Bunq API',
  parameters: z.object({}),
  execute: async () => {
    const response = await fetch(`${fastApiUrl}/create_user_session`);

    const output = await response.json();
    return output;
  },
});
