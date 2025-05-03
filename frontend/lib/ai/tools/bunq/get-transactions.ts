import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const getTransactions = tool({
  description: 'Get the recent transactions of the user from the Bunq API',
  parameters: z.object({}),
  execute: async () => {
    try {
      const response = await fetch(`${fastApiUrl}/transactions`);
      const transactions = await response.json();
      return transactions;
    } catch (error) {
      console.error('Error fetching transactions:', error);
      return {
        error: 'Failed to fetch transactions',
        reason: JSON.stringify(error),
        url: `${fastApiUrl}/transactions`,
      };
    }
  },
});
