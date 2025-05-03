import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const updateDraftPayment = tool({
  description: 'Update the status of a draft payment using the bunq API',
  parameters: z.object({
    draftPaymentId: z
      .number()
      .describe('The ID of the draft payment to update'),
    status: z
      .enum(['ACCEPTED', 'PENDING', 'REJECTED'])
      .describe('The new status to set for the draft payment'),
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account the draft payment belongs to',
      ),
  }),
  execute: async ({ draftPaymentId, status, monetaryAccountId }) => {
    let url = `${fastApiUrl}/draft_payments/`;

    const queryParams = new URLSearchParams();
    queryParams.append('draft_payment_id', draftPaymentId.toString());
    queryParams.append('status', status);

    if (monetaryAccountId) {
      queryParams.append('monetary_account_id', monetaryAccountId.toString());
    }

    url += `?${queryParams.toString()}`;

    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error fetching:', errorData);
      return errorData;
    }

    const result = await response.json();
    return result;
  },
});
