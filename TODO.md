# TODO:

- **Integration with Bunq API**:

  - [ ] Implement POST payment creation
  - [ ] Receiving payments on your website using bunq.me (possibly could be integrated)
  - [ ] Implement OAuth for authentication (currently getting API KEY is not production way of doing stuff)
    - [ ] this allows for handling multiple users not just one with API KEY
  - [ ] Chatbot access to editting user settings
  - **API ENDPOINTS**:
    - [x] GET /primary-monetary-account
    - [x] GET /user
    - [ ] ~~GET /transactions~~
    - [ ] ~~[https://doc.bunq.com/api-reference/bunqme] BUNQME STUFF (i.e. QR CODE STUFF)~~
    - [x] [https://doc.bunq.com/api-reference/billing-contract-subscription] GET /billing_subscriptions
    - [ ] [https://doc.bunq.com/content-and-exports, https://doc.bunq.com/exports]
    - [ ] [https://doc.bunq.com/currency-conversion]
    - [ ] [https://doc.bunq.com/customer-statements]
    - [x] [https://doc.bunq.com/draft-payment] POST /payment
    - [ ] [https://doc.bunq.com/ideal-merchant-transaction]
    - [ ] [https://doc.bunq.com/insights]
    - [ ] [https://doc.bunq.com/invoice]
    - [ ] [https://doc.bunq.com/invoice-export] GET /invoice_export
    - [x] [https://doc.bunq.com/monetary-account] GET, POST /monetary_account (A way to read / create different types of monetary accounts based on user preference)
    - [x] [https://doc.bunq.com/notification-filter/notification-filter-email] this can be useful for users who want to change their settings
    - [x] [https://doc.bunq.com/request] Requesting inquery stuff
    - [x] [https://doc.bunq.com/schedule] create scheduled payments

- **Other**:

  - [ ] Integrate S3 bucket to save images / files locally
  - [ ] Restrict chatbot from performing unintended actions (i.e. generation of code, ...)
  - [ ] Functionality test: see if chatbot can scan receipt and create a inquery request
  - [ ] Create a confirmation popup for user consent
  - [ ] host on AWS

**Submission Requirements**

See [Submission File](SUBMISSION.md)

- **NOTES**:
- Users have pain in setting up proper card structure (Ask Nurlan if such optimal card structure exists)

## Officially Written Down As User Stories

```
Users have pain in changing settings (if settings section is very unintuitive), easier to ask LLM to change it for you.
```

```
Aid in Budgetting Decisions (this can be generalized where you describe the situation to the AI and it gives you a possible solution)

Pain: Dining out without knowing how much a meal will impact budget.

AI Benefit: Scans menu, gives financial impact forecast, and alerts user if going over budget.
```

```
Automatic Budget Impact Warning

Pain: People overspend without real-time awareness.

AI Benefit: Before any transaction is completed (scanned or typed), AI shows its impact on your weekly/monthly budget.
```

```
Example: You can take a photo of a check for a dinner where the financial assistant will send the bill to the friend too.
```
