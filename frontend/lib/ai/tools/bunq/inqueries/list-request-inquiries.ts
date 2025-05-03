import { fastApiUrl } from '@/lib/constants';
import { tool } from 'ai';
import { z } from 'zod';

export const listRequestInquiries = tool({
  description:
    'List all request inquiries for a monetary account using the bunq API',
  parameters: z.object({
    monetaryAccountId: z
      .number()
      .optional()
      .describe(
        'Optional ID of the monetary account to list request inquiries for',
      ),
  }),
  execute: async ({ monetaryAccountId }) => {
    let url = `${fastApiUrl}/request_inquiries/`;
    if (monetaryAccountId) {
      url += `?monetary_account_id=${monetaryAccountId}`;
    }

    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error fetching:', errorData);
      return errorData;
    }

    const inquiries = await response.json();
    return inquiries;
  },
});
