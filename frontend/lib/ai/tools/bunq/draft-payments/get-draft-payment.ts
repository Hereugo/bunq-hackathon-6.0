import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const getDraftPayment = tool({
  description:
    'Retrieve details of a specific draft payment using the bunq API',
  parameters: z.object({
    draftPaymentId: z
      .number()
      .describe('The ID of the draft payment to retrieve'),
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account to fetch draft payment from',
      ),
  }),
  execute: async ({ draftPaymentId, monetaryAccountId }) => {
    let url = `${fastApiUrl}/draft_payments/${draftPaymentId}`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error fetching:', errorData);
      return errorData;
    }

    const draftPayment = await response.json();
    return draftPayment;
  },
});
