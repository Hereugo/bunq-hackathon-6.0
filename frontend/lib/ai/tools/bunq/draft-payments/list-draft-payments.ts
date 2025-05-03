import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const listDraftPayments = tool({
  description:
    'List all draft payments for a monetary account using the bunq API',
  parameters: z.object({
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account to list draft payments for',
      ),
  }),
  execute: async ({ monetaryAccountId }) => {
    let url = `${fastApiUrl}/draft_payments/`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error fetching:', errorData);
      return errorData;
    }

    const draftPayments = await response.json();
    return draftPayments;
  },
});
