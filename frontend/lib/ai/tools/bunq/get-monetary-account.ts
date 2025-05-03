import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const getMonetaryAccount = tool({
  description:
    'Get the monetary account of the user. If the monetaryAccountId is not provided, it will return the primary monetary account.',
  parameters: z.object({}),
  execute: async () => {
    const response = await fetch(`${fastApiUrl}/monetary_account`);

    const monetaryAccount = await response.json();
    return monetaryAccount;
  },
});
