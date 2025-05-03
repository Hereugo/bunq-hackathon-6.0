import { tool } from 'ai';
import { z } from 'zod';

export const getAllContacts = tool({
  description:
    'Get all the contacts that the user has. This includes all the contacts that the user has added to their bunq account.',
  parameters: z.object({}),
  execute: async () => {
    const contacts = [
      {
        name: 'Sugar Daddy',
        email: 'sugardaddy@bunq.com',
        iban: 'NL32BUNQ2025313705',
      },
      {
        name: 'Some Guy',
        email: 'test+43926918-db1c-4001-a756-4c31de5e41c0@bunq.com',
        phone: '+31611940590',
      },
      {
        name: 'Finn',
        phone: '+31619617699',
      },
      {
        name: 'Lebowski',
        email: '+31619626260',
      },
      {
        name: 'Land Lord',
        phone: '+31619633743',
      },
    ];
    return contacts;
  },
});
